import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline, UnivariateSpline
from scipy import odr
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore', ConvergenceWarning)

from sklearn.linear_model import (LinearRegression, ElasticNet, BayesianRidge, HuberRegressor, 
                                  Ridge, Lasso, TheilSenRegressor, RANSACRegressor, QuantileRegressor)
from sklearn.preprocessing import PolynomialFeatures, FunctionTransformer, SplineTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import KFold, TimeSeriesSplit, GridSearchCV
from sklearn.cluster import KMeans
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.structural import UnobservedComponents
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.exponential_smoothing.ets import ETSModel as StatsmodelsETSModel
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from pygam import LinearGAM, s

def calculate_r2(y, y_pred):
    y = np.array(y, dtype=np.float64)
    y_pred = np.array(y_pred, dtype=np.float64)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    if ss_tot == 0.0:
        return 0.0
    return 1.0 - (ss_res / ss_tot)

def get_seasonality(y):
    n = len(y)
    if n < 4:
        return 2
    y_d = y - np.linspace(y[0], y[-1], n)
    f = np.abs(np.fft.rfft(y_d))
    f[0] = 0
    freqs = np.fft.rfftfreq(n)
    dom = freqs[np.argmax(f)]
    s_val = int(1.0 / dom) if dom > 0 else 1
    return max(2, min(s_val, n // 2))

def _fourier_basis(x):
    return np.column_stack([np.sin(x), np.cos(x), np.sin(2*x), np.cos(2*x)])

class RegressionData:
    def __init__(self, t, y, t_surface, temp=None, rh=None):
        self.t = np.array(t, dtype=np.float64)
        self.y = np.array(y, dtype=np.float64)
        self.t_surface = np.array(t_surface, dtype=np.float64)
        
        self.temp = np.array(temp, dtype=np.float64) if temp is not None else np.zeros_like(self.t)
        self.rh = np.array(rh, dtype=np.float64) if rh is not None else np.zeros_like(self.t)
        
        if len(self.t) > 1:
            self.temp_s = np.interp(self.t_surface, self.t, self.temp)
            self.rh_s = np.interp(self.t_surface, self.t, self.rh)
        else:
            self.temp_s = np.zeros_like(self.t_surface)
            self.rh_s = np.zeros_like(self.t_surface)
            
        self.features = {
            't': self.t.reshape(-1, 1),
            'temp': self.temp.reshape(-1, 1),
            'rh': self.rh.reshape(-1, 1),
            't_temp': np.column_stack((self.t, self.temp)),
            't_rh': np.column_stack((self.t, self.rh)),
            'temp_rh': np.column_stack((self.temp, self.rh)),
            'all': np.column_stack((self.t, self.temp, self.rh)),
            't_s': self.t_surface.reshape(-1, 1),
            'temp_s': self.temp_s.reshape(-1, 1),
            'rh_s': self.rh_s.reshape(-1, 1),
            't_temp_s': np.column_stack((self.t_surface, self.temp_s)),
            't_rh_s': np.column_stack((self.t_surface, self.rh_s)),
            'temp_rh_s': np.column_stack((self.temp_s, self.rh_s)),
            'all_s': np.column_stack((self.t_surface, self.temp_s, self.rh_s))
        }

    def subset(self, indices):
        return RegressionData(
            self.t[indices], self.y[indices], self.t_surface,
            self.temp[indices], self.rh[indices]
        )

class BaseModel:
    def __init__(self, name, priority, cv_type='kfold'):
        self.name = name
        self.priority = priority
        self.cv_type = cv_type

    def fit(self, data):
        raise NotImplementedError

    def predict_eval(self, data_eval):
        raise NotImplementedError

    def predict_surface(self, full_data):
        raise NotImplementedError

class SklearnModel(BaseModel):
    def __init__(self, name, priority, estimator, param_grid, feat_key):
        super().__init__(name, priority, 'kfold')
        self.estimator = estimator
        self.param_grid = param_grid
        self.feat_key = feat_key
        self.best_estimator = None

    def fit(self, data):
        X = data.features[self.feat_key]
        y = data.y
        if self.param_grid:
            grid = GridSearchCV(self.estimator, self.param_grid, cv=2, scoring='r2')
            grid.fit(X, y)
            self.best_estimator = grid.best_estimator_
        else:
            self.best_estimator = self.estimator
            self.best_estimator.fit(X, y)

    def predict_eval(self, data_eval):
        return self.best_estimator.predict(data_eval.features[self.feat_key])

    def predict_surface(self, full_data):
        return self.best_estimator.predict(full_data.features[self.feat_key + '_s'])

class FGLSModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.beta = None
        
    def fit(self, data):
        X = data.features['t']
        y = data.y
        try:
            beta = np.linalg.pinv(X.T @ X) @ X.T @ y
        except Exception:
            beta = np.zeros(X.shape[1])
        for _ in range(5):
            res = y - X @ beta
            log_res2 = np.log(np.clip(res**2, 1e-12, None))
            try:
                alpha = np.linalg.pinv(X.T @ X) @ X.T @ log_res2
            except Exception:
                break
            var_est = np.exp(np.clip(X @ alpha, -50, 50))
            W = np.diag(1.0 / np.clip(var_est, 1e-12, None))
            try:
                beta_new = np.linalg.pinv(X.T @ W @ X) @ X.T @ W @ y
            except Exception:
                break
            if np.linalg.norm(beta - beta_new) < 1e-4:
                beta = beta_new
                break
            beta = beta_new
        self.beta = beta
        
    def predict_eval(self, data_eval):
        return data_eval.features['t'] @ self.beta
        
    def predict_surface(self, full_data):
        return full_data.features['t_s'] @ self.beta

class StateSpaceModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        best_aic = float('inf')
        for lvl in ['local level', 'local linear trend']:
            try:
                m = UnobservedComponents(data.y, level=lvl).fit(disp=False)
                if m.aic < best_aic:
                    best_aic = m.aic
                    self.model_res = m
            except Exception:
                pass
        if self.model_res is None:
            self.model_res = UnobservedComponents(data.y, level='local level').fit(disp=False)

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class SARIMAModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        y = data.y
        s_val = get_seasonality(y)
        best_aic = float('inf')
        best_order = (1, 0, 0)
        best_seasonal = (0, 0, 0, 0)
        for p in [0, 1]:
            for d in [0, 1]:
                for q in [0, 1]:
                    try:
                        m = SARIMAX(y, order=(p,d,q), seasonal_order=(0,0,0,s_val)).fit(disp=False)
                        if m.aic < best_aic:
                            best_aic = m.aic
                            best_order = (p,d,q)
                    except Exception:
                        pass
        self.model_res = SARIMAX(y, order=best_order, seasonal_order=best_seasonal).fit(disp=False)

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class ARIMAModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        best_aic = float('inf')
        best_order = (1, 1, 1)
        for p in [0, 1, 2]:
            for d in [0, 1]:
                for q in [0, 1, 2]:
                    try:
                        m = ARIMA(data.y, order=(p, d, q)).fit()
                        if m.aic < best_aic:
                            best_aic = m.aic
                            best_order = (p, d, q)
                    except:
                        pass
        self.model_res = ARIMA(data.y, order=best_order).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class ETSModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        y = np.clip(data.y, 1e-5, None)
        s_val = get_seasonality(y)
        best_aic = float('inf')
        for t_type in ['add', None]:
            for s_type in ['add', None]:
                try:
                    m = ExponentialSmoothing(y, trend=t_type, seasonal=s_type, seasonal_periods=s_val).fit()
                    if m.aic < best_aic:
                        best_aic = m.aic
                        self.model_res = m
                except Exception:
                    pass
            if self.model_res is None:
                self.model_res = ExponentialSmoothing(y).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class ODRModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.res = None
        
    def fit(self, data):
        def f(B, x): return B[0]*x + B[1]
        m = odr.Model(f)
        wd = 1.0 / max(np.var(data.t), 1e-12)
        we = 1.0 / max(np.var(data.y), 1e-12)
        d = odr.Data(data.t, data.y, wd=wd, we=we)
        o = odr.ODR(d, m, beta0=[1.0, 1.0])
        self.res = o.run()
        
    def predict_eval(self, data_eval):
        return self.res.beta[0]*data_eval.t + self.res.beta[1]
        
    def predict_surface(self, full_data):
        return self.res.beta[0]*full_data.t_surface + self.res.beta[1]

class TLSModel(BaseModel):
    def __init__(self, name, priority, feat_key='t'):
        super().__init__(name, priority, 'kfold')
        self.beta = None
        self.feat_key = feat_key

    def fit(self, data):
        X = np.column_stack((np.ones(len(data.y)), data.features[self.feat_key]))
        y = data.y.reshape(-1, 1)
        Z = np.hstack((X, y))
        _, _, V = np.linalg.svd(Z, full_matrices=False)
        Vxy = V[-1, :-1]
        Vyy = V[-1, -1]
        self.beta = -Vxy / (Vyy + 1e-12)

    def predict_eval(self, data_eval):
        X = np.column_stack((np.ones(len(data_eval.y)), data_eval.features[self.feat_key]))
        return X @ self.beta

    def predict_surface(self, full_data):
        X_s = np.column_stack((np.ones(len(full_data.t_surface)), full_data.features[self.feat_key + '_s']))
        return X_s @ self.beta

class DemingModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.b0 = 0
        self.b1 = 1

    def fit(self, data):
        x = data.t
        y = data.y
        x_m = np.mean(x)
        y_m = np.mean(y)
        s_xx = np.sum((x - x_m)**2)
        s_yy = np.sum((y - y_m)**2)
        s_xy = np.sum((x - x_m)*(y - y_m))
        if s_xy == 0:
            self.b1 = 0
        else:
            self.b1 = (s_yy - s_xx + np.sqrt((s_yy - s_xx)**2 + 4*s_xy**2)) / (2*s_xy + 1e-12)
        self.b0 = y_m - self.b1 * x_m

    def predict_eval(self, data_eval):
        return self.b0 + self.b1 * data_eval.t

    def predict_surface(self, full_data):
        return self.b0 + self.b1 * full_data.t_surface

class LOESSModelSource1(BaseModel):
    def __init__(self, name, priority, deg=1):
        super().__init__(name, priority, 'kfold')
        self.best_alpha = 0.5
        self.best_deg = deg
        self.t_train = None
        self.y_train = None

    def fit(self, data):
        t, y = data.t, data.y
        best_mse = float('inf')
        n = len(t)
        for alpha in [0.4, 0.7]:
            k = min(n - 1, max(2, int(n * alpha)))
            idx = k - 1
            errs = []
            for i in range(min(n, 10)):
                tr_idx = np.arange(n) != i
                t_tr, y_tr = t[tr_idx], y[tr_idx]
                dists = np.abs(t_tr - t[i])
                h = np.partition(dists, idx)[idx] + 1e-10
                u = dists / h
                w = np.where(u <= 1.0, (1.0 - u**3)**3, 0.0)
                if np.sum(w) == 0: continue
                W = np.diag(w)
                if self.best_deg == 1:
                    X = np.column_stack((np.ones_like(t_tr), t_tr - t[i]))
                else:
                    X = np.column_stack((np.ones_like(t_tr), t_tr - t[i], (t_tr - t[i])**2))
                try:
                    c = np.linalg.pinv(X.T @ W @ X) @ X.T @ W @ y_tr
                    errs.append((y[i] - c[0])**2)
                except Exception:
                    pass
            if errs and np.mean(errs) < best_mse:
                best_mse = np.mean(errs)
                self.best_alpha = alpha
        self.t_train = t
        self.y_train = y

    def _predict_single(self, x0):
        dists = np.abs(self.t_train - x0)
        n = len(self.t_train)
        k = min(n - 1, max(2, int(n * self.best_alpha)))
        idx = k - 1
        h = np.partition(dists, idx)[idx] + 1e-10
        u = dists / h
        w = np.where(u <= 1.0, (1.0 - u**3)**3, 0.0)
        if np.sum(w) == 0: return np.mean(self.y_train)
        W = np.diag(w)
        if self.best_deg == 1:
            X = np.column_stack((np.ones_like(self.t_train), self.t_train - x0))
        else:
            X = np.column_stack((np.ones_like(self.t_train), self.t_train - x0, (self.t_train - x0)**2))
        try:
            return (np.linalg.pinv(X.T @ W @ X) @ X.T @ W @ self.y_train)[0]
        except Exception:
            return np.mean(self.y_train)

    def predict_eval(self, data_eval):
        return np.array([self._predict_single(x) for x in data_eval.t])

    def predict_surface(self, full_data):
        return np.array([self._predict_single(x) for x in full_data.t_surface])

class GAMModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.model = None

    def fit(self, data):
        X = data.features['t']
        self.model = LinearGAM(s(0)).gridsearch(X, data.y, progress=False)

    def predict_eval(self, data_eval):
        return self.model.predict(data_eval.features['t'])

    def predict_surface(self, full_data):
        return self.model.predict(full_data.features['t_s'])

class TPSModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.w = None
        self.a = None
        self.X_train = None

    def fit(self, data):
        X = data.features['t']
        y = data.y
        n = len(y)
        dists = np.sqrt(np.sum((X[:, None, :] - X[None, :, :])**2, axis=2))
        K = np.zeros((n, n))
        m = dists > 1e-10
        K[m] = (dists[m]**2) * np.log(dists[m])
        P = np.column_stack((np.ones(n), X))
        L = np.zeros((n + 2, n + 2))
        L[:n, :n] = K + 1e-4 * np.eye(n)
        L[:n, n:] = P
        L[n:, :n] = P.T
        params = np.linalg.pinv(L) @ np.concatenate([y, np.zeros(2)])
        self.w, self.a = params[:n], params[n:]
        self.X_train = X

    def predict_eval(self, data_eval):
        X_new = data_eval.features['t']
        dists = np.sqrt(np.sum((X_new[:, None, :] - self.X_train[None, :, :])**2, axis=2))
        K = np.zeros((len(X_new), len(self.X_train)))
        m = dists > 1e-10
        K[m] = (dists[m]**2) * np.log(dists[m])
        P = np.column_stack((np.ones(len(X_new)), X_new))
        return K @ self.w + P @ self.a

    def predict_surface(self, full_data):
        X_new = full_data.features['t_s']
        dists = np.sqrt(np.sum((X_new[:, None, :] - self.X_train[None, :, :])**2, axis=2))
        K = np.zeros((len(X_new), len(self.X_train)))
        m = dists > 1e-10
        K[m] = (dists[m]**2) * np.log(dists[m])
        P = np.column_stack((np.ones(len(X_new)), X_new))
        return K @ self.w + P @ self.a

class SplineModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.cs = None

    def fit(self, data):
        t, y = data.t, data.y
        t_unique, inverse = np.unique(t, return_inverse=True)
        y_unique = np.zeros_like(t_unique, dtype=np.float64)
        np.add.at(y_unique, inverse, y)
        count = np.bincount(inverse)
        y_unique /= count
        t_s, y_s = t_unique, y_unique
        if len(t_s) < 4:
            self.cs = CubicSpline(t_s, y_s, bc_type='natural', extrapolate=True)
            return
        best_err = float('inf')
        best_bc = 'natural'
        kf_spline = KFold(n_splits=min(2, len(t_s)), shuffle=True, random_state=42)
        for bc in ['natural', 'not-a-knot']:
            fold_errs = []
            for tr_idx, te_idx in kf_spline.split(t_s):
                t_tr, y_tr = t_s[tr_idx], y_s[tr_idx]
                t_te, y_te = t_s[te_idx], y_s[te_idx]
                if len(t_tr) < 3:
                    continue
                tr_sorted = np.argsort(t_tr)
                t_tr_s, y_tr_s = t_tr[tr_sorted], y_tr[tr_sorted]
                try:
                    cs_test = CubicSpline(t_tr_s, y_tr_s, bc_type=bc, extrapolate=True)
                    preds = cs_test(t_te)
                    fold_errs.append(np.mean((y_te - preds)**2))
                except Exception:
                    pass
            if fold_errs and np.mean(fold_errs) < best_err:
                best_err = np.mean(fold_errs)
                best_bc = bc
        self.cs = CubicSpline(t_s, y_s, bc_type=best_bc, extrapolate=True)

    def predict_eval(self, data_eval):
        return self.cs(data_eval.t)

    def predict_surface(self, full_data):
        return self.cs(full_data.t_surface)

class NaturalCubicSplineModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.lr = LinearRegression()
        self.knots = None

    def _get_basis(self, t):
        X = np.column_stack([np.ones_like(t), t])
        k = self.knots
        kK = k[-1]
        kK1 = k[-2]
        for j in range(len(k) - 2):
            kj = k[j]
            dj = (np.maximum(0, t - kj)**3 - np.maximum(0, t - kK)**3) / (kK - kj)
            dK1 = (np.maximum(0, t - kK1)**3 - np.maximum(0, t - kK)**3) / (kK - kK1)
            X = np.column_stack([X, dj - dK1])
        return X

    def fit(self, data):
        self.knots = np.percentile(data.t, [10, 33, 66, 90])
        X = self._get_basis(data.t)
        self.lr.fit(X, data.y)

    def predict_eval(self, data_eval):
        return self.lr.predict(self._get_basis(data_eval.t))

    def predict_surface(self, full_data):
        return self.lr.predict(self._get_basis(full_data.t_surface))

class BSplineRegressionModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.pipe = Pipeline([('spline', SplineTransformer(n_knots=4, degree=3, extrapolation='linear')), ('lr', LinearRegression(fit_intercept=True))])

    def fit(self, data):
        self.pipe.fit(data.t.reshape(-1, 1), data.y)

    def predict_eval(self, data_eval):
        return self.pipe.predict(data_eval.t.reshape(-1, 1))

    def predict_surface(self, full_data):
        return self.pipe.predict(full_data.t_surface.reshape(-1, 1))

class SmoothingSplineModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.spline = None

    def fit(self, data):
        t, y = data.t, data.y
        idx = np.argsort(t)
        ts, ys = t[idx], y[idx]
        ts_uniq, inv = np.unique(ts, return_inverse=True)
        ys_uniq = np.zeros_like(ts_uniq)
        np.add.at(ys_uniq, inv, ys)
        ys_uniq /= np.bincount(inv)
        best_s = 1.0
        best_r2 = -np.inf
        for s_val in np.logspace(-2, 2, 5):
            try:
                spl = UnivariateSpline(ts_uniq, ys_uniq, s=s_val)
                preds = spl(t)
                r2 = calculate_r2(y, preds)
                if r2 > best_r2:
                    best_r2 = r2
                    best_s = s_val
            except:
                pass
        self.spline = UnivariateSpline(ts_uniq, ys_uniq, s=best_s)

    def predict_eval(self, data_eval):
        return self.spline(data_eval.t)

    def predict_surface(self, full_data):
        return self.spline(full_data.t_surface)

class PSplineModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.st = SplineTransformer(n_knots=10, degree=3, extrapolation='linear')
        self.beta = None

    def fit(self, data):
        B = self.st.fit_transform(data.t.reshape(-1, 1))
        m = B.shape[1]
        D = np.zeros((m-2, m))
        for i in range(m-2):
            D[i, i] = 1; D[i, i+1] = -2; D[i, i+2] = 1
        P = D.T @ D
        BTB = B.T @ B
        BTy = B.T @ data.y
        best_gcv = float('inf')
        best_beta = None
        n = len(data.y)
        for lam in np.logspace(-3, 3, 5):
            A = BTB + lam * P
            try:
                beta = np.linalg.pinv(A) @ BTy
                df = np.trace(np.linalg.pinv(A) @ BTB)
                res2 = np.sum((data.y - B @ beta)**2)
                denom = (1.0 - df/n)**2
                if denom > 0 and (res2/n)/denom < best_gcv:
                    best_gcv = (res2/n)/denom
                    best_beta = beta
            except:
                pass
        self.beta = best_beta if best_beta is not None else np.linalg.pinv(BTB) @ BTy

    def predict_eval(self, data_eval):
        B = self.st.transform(data_eval.t.reshape(-1, 1))
        return B @ self.beta

    def predict_surface(self, full_data):
        B = self.st.transform(full_data.t_surface.reshape(-1, 1))
        return B @ self.beta

class PiecewiseLinearModelSource1(BaseModel):
    def __init__(self, name, priority, poly_deg=1):
        super().__init__(name, priority, 'kfold')
        self.best_bp = []
        self.best_coef = None
        self.poly_deg = poly_deg

    def fit(self, data):
        t, y = data.t, data.y
        ts = np.sort(t)
        best_rss = float('inf')
        q_idx = np.linspace(1, len(t)-2, min(5, len(t)-2)).astype(int)
        bps_1 = ts[q_idx]
        for bp1 in bps_1:
            X = self._build_X(t, [bp1])
            try:
                c, r, _, _ = np.linalg.lstsq(X, y, rcond=None)
                rss = r[0] if len(r) > 0 else np.sum((y - X@c)**2)
                if rss < best_rss:
                    best_rss, self.best_bp, self.best_coef = rss, [bp1], c
            except: pass
        if self.best_coef is None:
            self.best_bp = []
            self.best_coef = np.linalg.pinv(self._build_X(t, [])) @ y

    def _build_X(self, t, bps):
        X = [np.ones_like(t)]
        if self.poly_deg > 0:
            X.append(t)
        if self.poly_deg > 1:
            for d in range(2, self.poly_deg + 1):
                X.append(t**d)
        for bp in bps:
            X.append(np.maximum(0, t - bp)**self.poly_deg)
        return np.column_stack(X)

    def predict_eval(self, data_eval):
        return self._build_X(data_eval.t, self.best_bp) @ self.best_coef

    def predict_surface(self, full_data):
        return self._build_X(full_data.t_surface, self.best_bp) @ self.best_coef

class CurveModelSource1(BaseModel):
    def __init__(self, name, priority, func, p0_func, bounds_func=None):
        super().__init__(name, priority, 'kfold')
        self.func = func
        self.p0_func = p0_func
        self.bounds_func = bounds_func
        self.p = None
        self.fallback_mean = 0

    def fit(self, data):
        self.fallback_mean = np.mean(data.y)
        p0 = self.p0_func(data)
        bounds = self.bounds_func(data) if self.bounds_func else (-np.inf, np.inf)
        try:
            self.p, _ = curve_fit(self.func, data.t, data.y, p0=p0, bounds=bounds, maxfev=5000)
        except Exception:
            self.p = p0

    def predict_eval(self, data_eval):
        try:
            return self.func(data_eval.t, *self.p)
        except:
            return np.full_like(data_eval.t, self.fallback_mean)

    def predict_surface(self, full_data):
        try:
            return self.func(full_data.t_surface, *self.p)
        except:
            return np.full_like(full_data.t_surface, self.fallback_mean)

class KernelRegressionModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'kfold')
        self.bandwidth = 1.0
        self.t_train = None
        self.y_train = None

    def fit(self, data):
        self.t_train = data.t
        self.y_train = data.y
        std_t = np.std(data.t) if np.std(data.t) > 1e-8 else 1e-8
        h_silverman = std_t * (4 / (3 * len(data.t)))**(1/5)
        best_h = h_silverman
        best_score = float('inf')
        for factor in [0.5, 1.0, 2.0]:
            h = h_silverman * factor
            score = 0
            for i in range(min(len(data.t), 10)):
                mask = np.arange(len(data.t)) != i
                w = np.exp(-0.5 * ((data.t[mask] - data.t[i]) / h)**2)
                sw = np.sum(w)
                pred = np.sum(w * data.y[mask]) / sw if sw > 0 else np.mean(data.y[mask])
                score += (data.y[i] - pred)**2
            if score < best_score:
                best_score = score
                best_h = h
        self.bandwidth = best_h

    def _predict(self, X):
        preds = []
        for x0 in X:
            weights = np.exp(-0.5 * ((self.t_train - x0) / self.bandwidth)**2)
            sum_w = np.sum(weights)
            preds.append(np.sum(weights * self.y_train) / sum_w if sum_w > 0 else np.mean(self.y_train))
        return np.array(preds)

    def predict_eval(self, data_eval):
        return self._predict(data_eval.t)

    def predict_surface(self, full_data):
        return self._predict(full_data.t_surface)

class MovingAverageRegressionModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        best_aic = float('inf')
        best_q = 1
        for q in [1, 2]:
            try:
                m = ARIMA(data.y, order=(0, 0, q)).fit()
                if m.aic < best_aic:
                    best_aic = m.aic
                    best_q = q
            except:
                pass
        self.model_res = ARIMA(data.y, order=(0, 0, best_q)).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class PureExponentialSmoothingModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        self.model_res = ExponentialSmoothing(data.y, trend=None, seasonal=None).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class HoltLinearTrendModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        self.model_res = ExponentialSmoothing(data.y, trend='add', seasonal=None).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class HoltWintersModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        s_val = get_seasonality(data.y)
        best_aic = float('inf')
        for stype in ['add', 'mul']:
            if stype == 'mul' and np.any(data.y <= 0):
                continue
            try:
                m = ExponentialSmoothing(data.y, trend='add', seasonal=stype, seasonal_periods=s_val).fit()
                if m.aic < best_aic:
                    best_aic = m.aic
                    self.model_res = m
            except:
                pass
        if self.model_res is None:
            self.model_res = ExponentialSmoothing(data.y, trend='add', seasonal='add', seasonal_periods=s_val).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class PureARModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        best_aic = float('inf')
        best_p = 1
        for p in [1, 2, 3]:
            try:
                m = ARIMA(data.y, order=(p, 0, 0)).fit()
                if m.aic < best_aic:
                    best_aic = m.aic
                    best_p = p
            except:
                pass
        self.model_res = ARIMA(data.y, order=(best_p, 0, 0)).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class PureARMAModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        best_aic = float('inf')
        best_order = (1, 0, 1)
        for p in [1, 2]:
            for q in [1, 2]:
                try:
                    m = ARIMA(data.y, order=(p, 0, q)).fit()
                    if m.aic < best_aic:
                        best_aic = m.aic
                        best_order = (p, 0, q)
                except:
                    pass
        self.model_res = ARIMA(data.y, order=best_order).fit()

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class ComprehensiveETSModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.model_res = None

    def fit(self, data):
        y_clip = np.clip(data.y, 1e-5, None)
        s_val = get_seasonality(y_clip)
        best_aic = float('inf')
        for e in ['add', 'mul']:
            for t in ['add', None]:
                for s in ['add', None]:
                    try:
                        m = StatsmodelsETSModel(y_clip, error=e, trend=t, seasonal=s, seasonal_periods=s_val if s else None).fit(disp=False)
                        if m.aic < best_aic:
                            best_aic = m.aic
                            self.model_res = m
                    except:
                        pass
        if self.model_res is None:
            self.model_res = StatsmodelsETSModel(y_clip, error='add', trend=None, seasonal=None).fit(disp=False)

    def predict_eval(self, data_eval):
        return self.model_res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.model_res.forecast(steps=len(full_data.t_surface))

class DynamicLinearModel(BaseModel):
    def __init__(self, name, priority):
        super().__init__(name, priority, 'ts')
        self.res = None

    def fit(self, data):
        self.res = UnobservedComponents(data.y, level='local linear trend', cycle=True, stochastic_cycle=True).fit(disp=False)

    def predict_eval(self, data_eval):
        return self.res.forecast(steps=len(data_eval.y))

    def predict_surface(self, full_data):
        return self.res.forecast(steps=len(full_data.t_surface))

class StateSpaceRegressionModel(BaseModel):
    def __init__(self, name, priority, feat_key='all'):
        super().__init__(name, priority, 'ts')
        self.feat_key = feat_key
        self.res = None

    def fit(self, data):
        X = data.features[self.feat_key]
        self.res = UnobservedComponents(data.y, level='local level', exog=X).fit(disp=False)

    def predict_eval(self, data_eval):
        X_eval = data_eval.features[self.feat_key]
        return self.res.forecast(steps=len(data_eval.y), exog=X_eval)

    def predict_surface(self, full_data):
        X_surf = full_data.features[self.feat_key + '_s']
        return self.res.forecast(steps=len(full_data.t_surface), exog=X_surf)

class KalmanFilterRegressionModel(BaseModel):
    def __init__(self, name, priority, feat_key='all'):
        super().__init__(name, priority, 'kfold')
        self.feat_key = feat_key
        self.beta_final = None

    def fit(self, data):
        X = np.column_stack((np.ones(len(data.y)), data.features[self.feat_key]))
        y = data.y
        m = X.shape[1]
        beta = np.zeros(m)
        P = np.eye(m) * 100.0
        Q = np.eye(m) * 1e-4
        R = 1.0
        for i in range(len(y)):
            beta_pred = beta
            P_pred = P + Q
            xi = X[i, :]
            y_pred = np.dot(xi, beta_pred)
            v = y[i] - y_pred
            S = np.dot(xi, np.dot(P_pred, xi)) + R
            K = np.dot(P_pred, xi) / S
            beta = beta_pred + K * v
            P = P_pred - np.outer(K, xi) @ P_pred
        self.beta_final = beta

    def predict_eval(self, data_eval):
        X = np.column_stack((np.ones(len(data_eval.y)), data_eval.features[self.feat_key]))
        return X @ self.beta_final

    def predict_surface(self, full_data):
        X_s = np.column_stack((np.ones(len(full_data.t_surface)), full_data.features[self.feat_key + '_s']))
        return X_s @ self.beta_final

class RBFNetworkModel(BaseModel):
    def __init__(self, name, priority, n_centers=5):
        super().__init__(name, priority, 'kfold')
        self.n_centers = n_centers
        self.centers = None
        self.gamma = 1.0
        self.lr = LinearRegression()

    def _rbf_basis(self, X):
        dists = np.sqrt(np.sum((X[:, None, :] - self.centers[None, :, :])**2, axis=2))
        return np.exp(-self.gamma * (dists**2))

    def fit(self, data):
        X = data.features['all']
        n_samples = len(X)
        actual_centers = min(self.n_centers, n_samples)
        km = KMeans(n_clusters=actual_centers, random_state=42, n_init=5)
        km.fit(X)
        self.centers = km.cluster_centers_
        dists = np.sqrt(np.sum((self.centers[:, None, :] - self.centers[None, :, :])**2, axis=2))
        max_dist = np.max(dists)
        self.gamma = 1.0 / (2 * (max_dist / np.sqrt(2 * actual_centers))**2 + 1e-8)
        G = self._rbf_basis(X)
        self.lr.fit(G, data.y)

    def predict_eval(self, data_eval):
        G = self._rbf_basis(data_eval.features['all'])
        return self.lr.predict(G)

    def predict_surface(self, full_data):
        G = self._rbf_basis(full_data.features['all_s'])
        return self.lr.predict(G)

class ModelRunner:
    def __init__(self, data):
        self.data = data
        self.models = self._build_models()

    def _build_models(self):
        models = [
            SklearnModel("Multi-Variable Regression (Time + Temperature + Relative Humidity)", 1, LinearRegression(), None, 'all'),
            SklearnModel("Multi-Variable Regression (Temperature + Relative Humidity)", 2, LinearRegression(), None, 'temp_rh'),
            SklearnModel("Multi-Variable Regression (Time + Temperature)", 3, LinearRegression(), None, 't_temp'),
            SklearnModel("Multi-Variable Regression (Time + Relative Humidity)", 4, LinearRegression(), None, 't_rh'),
            SklearnModel("Full Quadratic Surface Regression", 5, Pipeline([('poly', PolynomialFeatures(degree=2)), ('lr', LinearRegression())]), None, 'all'),
            SklearnModel("Multi-Variable Quadratic Regression", 6, Pipeline([('poly', PolynomialFeatures(degree=2)), ('lr', LinearRegression())]), None, 't_temp'),
            SklearnModel("Temperature × Humidity Interaction Regression", 7, Pipeline([('poly', PolynomialFeatures(degree=2, interaction_only=True)), ('lr', LinearRegression())]), None, 'temp_rh'),
            SklearnModel("Temperature Linear Regression", 8, LinearRegression(), None, 'temp'),
            SklearnModel("Humidity Linear Regression", 9, LinearRegression(), None, 'rh'),
            SklearnModel("Temperature Inverse Regression", 10, Pipeline([('inv', FunctionTransformer(lambda x: 1.0/(x+1e-8))), ('lr', LinearRegression())]), None, 'temp'),
            SklearnModel("Humidity Inverse Regression", 11, Pipeline([('inv', FunctionTransformer(lambda x: 1.0/(x+1e-8))), ('lr', LinearRegression())]), None, 'rh'),
            SklearnModel("Linear Regression", 12, LinearRegression(), None, 't'),
            FGLSModel("Weighted Linear Regression", 13),
            SklearnModel("Robust Regression (Huber)", 14, HuberRegressor(), None, 't'),
            SklearnModel("Theil–Sen Regression", 15, TheilSenRegressor(random_state=42), None, 't'),
            SklearnModel("RANSAC Regression", 16, RANSACRegressor(random_state=42), None, 't'),
            SklearnModel("Ridge Regression", 17, Ridge(random_state=42), {'alpha': [0.1, 1.0]}, 't'),
            SklearnModel("Lasso Regression", 18, Lasso(random_state=42), {'alpha': [0.1, 1.0]}, 't'),
            SklearnModel("Elastic Net Regression", 19, ElasticNet(random_state=42), {'alpha': [0.1, 1.0], 'l1_ratio': [0.5]}, 't'),
            SklearnModel("Bayesian Linear Regression", 20, BayesianRidge(), None, 't'),
            SklearnModel("Bayesian Polynomial Regression", 21, Pipeline([('poly', PolynomialFeatures(degree=3)), ('br', BayesianRidge())]), None, 't'),
            ODRModel("Orthogonal Distance Regression (ODR)", 22),
            TLSModel("Total Least Squares (TLS)", 23),
            DemingModel("Deming Regression", 24),
            SklearnModel("2nd Degree Polynomial Regression", 25, Pipeline([('poly', PolynomialFeatures(degree=2)), ('lr', LinearRegression())]), None, 't'),
            SklearnModel("3rd Degree Polynomial Regression", 26, Pipeline([('poly', PolynomialFeatures(degree=3)), ('lr', LinearRegression())]), None, 't'),
            SklearnModel("4th Degree Polynomial Regression", 27, Pipeline([('poly', PolynomialFeatures(degree=4)), ('lr', LinearRegression())]), None, 't'),
            CurveModelSource1("Exponential Regression", 28, lambda x, a, b, c: a * np.exp(np.clip(b * x, -50, 50)) + c, lambda d: [1.0, 0.01, np.min(d.y)]),
            CurveModelSource1("Logarithmic Regression", 29, lambda x, a, b: a * np.log(np.clip(x, 1e-8, None)) + b, lambda d: [1.0, np.mean(d.y)]),
            CurveModelSource1("Power Regression", 30, lambda x, a, b, c: a * np.power(np.clip(x, 1e-8, None), b) + c, lambda d: [1.0, 1.0, 0.0], lambda d: ([-np.inf, -5, -np.inf], [np.inf, 5, np.inf])),
            CurveModelSource1("Gaussian Regression", 31, lambda x, a, b, c, d_c: a * np.exp(-(x - b)**2 / (2 * c**2 + 1e-8)) + d_c, lambda d: [np.max(d.y)-np.min(d.y), d.t[np.argmax(d.y)], max(np.std(d.t), 1e-5), np.min(d.y)], lambda d: ([0, -np.inf, 1e-5, -np.inf], [np.inf, np.inf, np.inf, np.inf])),
            CurveModelSource1("Rational Function Regression", 32, lambda x, a, b, c, d_p: (a * x + b) / (c * x + d_p + 1e-8), lambda d: [1.0, 1.0, 1.0, 1.0]),
            CurveModelSource1("Hyperbolic Regression", 33, lambda x, a, b, c: a + b / (x + c + 1e-8), lambda d: [np.mean(d.y), 1.0, 1.0]),
            SklearnModel("Reciprocal Polynomial Regression", 34, Pipeline([('inv', FunctionTransformer(lambda x: 1.0/(x+1e-8))), ('poly', PolynomialFeatures(degree=2)), ('lr', LinearRegression())]), None, 't'),
            CurveModelSource1("Padé Approximation Regression", 35, lambda x, a0, a1, b1: (a0 + a1 * x) / (1.0 + b1 * x + 1e-8), lambda d: [np.mean(d.y), 0.1, 0.1]),
            PiecewiseLinearModelSource1("Piecewise Regression", 36, poly_deg=0),
            PiecewiseLinearModelSource1("Piecewise Linear Regression", 37, poly_deg=1),
            PiecewiseLinearModelSource1("Piecewise Polynomial Regression", 38, poly_deg=2),
            LOESSModelSource1("LOESS (LOWESS) Regression", 39, deg=1),
            LOESSModelSource1("Local Polynomial Regression", 40, deg=2),
            KernelRegressionModel("Kernel Regression (Nadaraya–Watson)", 41),
            GAMModel("Generalized Additive Model (GAM)", 42),
            SklearnModel("Quantile Regression", 43, QuantileRegressor(alpha=0.0, solver='highs'), None, 't'),
            SplineModel("Cubic Spline Regression", 44),
            NaturalCubicSplineModel("Natural Cubic Spline Regression", 45),
            BSplineRegressionModel("B-Spline Regression", 46),
            SmoothingSplineModel("Smoothing Spline Regression", 47),
            PSplineModel("Penalized Spline Regression (P-Spline)", 48),
            TPSModel("Thin Plate Spline Regression", 49),
            SklearnModel("2nd Degree Fourier Series", 50, Pipeline([('fourier', FunctionTransformer(_fourier_basis)), ('lr', LinearRegression())]), None, 't'),
            CurveModelSource1("Sinusoidal Regression", 51, lambda x, a, w, phi, c: a * np.sin(w * x + phi) + c, lambda d: [np.std(d.y), 2.0*np.pi/max(1e-5, np.max(d.t)-np.min(d.t)), 0.0, np.mean(d.y)]),
            MovingAverageRegressionModel("Moving Average Regression", 52),
            PureExponentialSmoothingModel("Exponential Smoothing", 53),
            HoltLinearTrendModel("Holt Linear Trend", 54),
            HoltWintersModel("Holt-Winters Method", 55),
            PureARModel("Autoregressive (AR) Model", 56),
            PureARMAModel("Autoregressive Moving Average (ARMA)", 57),
            ARIMAModel("Autoregressive Integrated Moving Average (ARIMA)", 58),
            SARIMAModel("Seasonal ARIMA (SARIMA)", 59),
            ComprehensiveETSModel("Error–Trend–Seasonality (ETS)", 60),
            DynamicLinearModel("Dynamic Linear Model (DLM)", 61),
            StateSpaceRegressionModel("State Space Regression", 62, feat_key='all'),
            KalmanFilterRegressionModel("Kalman Filter Regression", 63, feat_key='all'),
            SklearnModel("Support Vector Regression (SVR)", 64, SVR(), {'C': [1, 10], 'epsilon': [0.1]}, 't'),
            SklearnModel("Decision Tree Regression", 65, DecisionTreeRegressor(random_state=42), None, 't'),
            SklearnModel("Random Forest Regression", 66, RandomForestRegressor(random_state=42, n_jobs=1, n_estimators=50), None, 't'),
            SklearnModel("Extra Trees Regression", 67, ExtraTreesRegressor(random_state=42, n_jobs=1, n_estimators=50), None, 't'),
            SklearnModel("Gradient Boosting Regression", 68, GradientBoostingRegressor(random_state=42, n_estimators=50), None, 't'),
            SklearnModel("AdaBoost Regression", 69, AdaBoostRegressor(random_state=42, n_estimators=50), None, 't'),
            SklearnModel("Extreme Gradient Boosting (XGBoost)", 70, XGBRegressor(random_state=42, n_jobs=1, n_estimators=50), None, 't'),
            SklearnModel("Light Gradient Boosting Machine (LightGBM)", 71, LGBMRegressor(random_state=42, n_jobs=1, n_estimators=50, verbose=-1), None, 't'),
            SklearnModel("CatBoost Regression", 72, CatBoostRegressor(verbose=0, random_state=42, thread_count=1, iterations=50), None, 't'),
            SklearnModel("k-Nearest Neighbors Regression (kNN)", 73, KNeighborsRegressor(), {'n_neighbors': [3, 5]}, 't'),
            SklearnModel("Gaussian Process Regression (GPR)", 74, GaussianProcessRegressor(random_state=42), None, 't'),
            SklearnModel("Artificial Neural Network (ANN)", 75, MLPRegressor(max_iter=500, random_state=42), None, 'all'),
            SklearnModel("Multi-Layer Perceptron (MLP)", 76, MLPRegressor(max_iter=500, random_state=42), None, 'all'),
            RBFNetworkModel("Radial Basis Function Neural Network (RBF Network)", 77)
        ]
        
        models.sort(key=lambda m: m.priority)
        return models

    def run(self):
        statuses = {}
        best_cv_r2 = -np.float64(np.inf)
        best_y_surface = np.full_like(self.data.t_surface, np.mean(self.data.y), dtype=np.float64)
        best_name = "Average Value (Fallback)"
        best_priority = float('inf')
        
        kf = KFold(n_splits=2, shuffle=True, random_state=42)
        tscv = TimeSeriesSplit(n_splits=2)

        for model in self.models:
            try:
                cv_preds = np.zeros_like(self.data.y)
                splitter = tscv if model.cv_type == 'ts' else kf
                
                for tr_idx, te_idx in splitter.split(self.data.t):
                    data_tr = self.data.subset(tr_idx)
                    data_te = self.data.subset(te_idx)
                    model.fit(data_tr)
                    cv_preds[te_idx] = model.predict_eval(data_te)
                
                if model.cv_type == 'ts':
                    scores = []
                    for tr_idx, te_idx in tscv.split(self.data.t):
                        scores.append(calculate_r2(self.data.y[te_idx], cv_preds[te_idx]))
                    cv_r2 = np.mean(scores)
                else:
                    m_mask = ~np.isnan(cv_preds) & ~np.isinf(cv_preds)
                    if np.sum(m_mask) < len(cv_preds) * 0.5:
                        raise ValueError("Too many invalid predictions")
                    cv_r2 = calculate_r2(self.data.y[m_mask], cv_preds[m_mask])

                model.fit(self.data)
                y_surf = model.predict_surface(self.data)
                
                statuses[model.name] = {"Status": "Success", "CV_R2": round(float(cv_r2), 4)}
                
                if cv_r2 > best_cv_r2:
                    best_cv_r2 = cv_r2
                    best_y_surface = y_surf
                    best_name = model.name
                    best_priority = model.priority
                elif np.abs(cv_r2 - best_cv_r2) < 1e-12:
                    if model.priority < best_priority:
                        best_cv_r2 = cv_r2
                        best_y_surface = y_surf
                        best_name = model.name
                        best_priority = model.priority
            except Exception as e:
                statuses[model.name] = {"Status": f"Failed: {str(e)[:40]}", "CV_R2": None}

        if best_cv_r2 < -100 or np.isinf(best_cv_r2) or np.isnan(best_cv_r2):
            best_cv_r2 = 0.0
            best_y_surface = np.full_like(self.data.t_surface, np.mean(self.data.y), dtype=np.float64)
            best_name = "Average Value (Fallback)"
            
        return round(float(best_cv_r2), 4), best_y_surface, best_name, statuses

def get_best_fit(t, y, t_surface, temp=None, rh=None):
    data = RegressionData(t, y, t_surface, temp, rh)
    runner = ModelRunner(data)
    cv_r2, best_y_surface, best_name, statuses = runner.run()
    
    print("\n" + "="*50)
    print("MODEL R^2 SCORES")
    print("="*50)
    for m_name, info in statuses.items():
        if info['Status'] == 'Success':
            print(f"{m_name:<50} : {info['CV_R2']}")
        else:
            print(f"{m_name:<50} : FAILED")
    print("-" * 50)
    print(f"BEST MODEL SELECTED: {best_name}")
    print(f"BEST R^2 SCORE     : {cv_r2}")
    print("="*50 + "\n")
    
    return cv_r2, best_y_surface, best_name
