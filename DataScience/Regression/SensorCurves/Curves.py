import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.optimize import curve_fit
import random

def print_gas_table(gas_data, typ):
    print()
    if typ == 1:
        print("For New Curve (R² >= 0.9995):")
        print()
        print("for ppm = a*ratio^b:")
        print()
        print("Gas    | a       | b")
        for gas, (a, b) in gas_data1.items():
            print(f"{gas.ljust(7)}| {str(a).ljust(8)}| {str(b).ljust(7)}")
    if typ == 2:
        print("for ppm = 10^[(log10(ratio)-b)/m]:")
        print()
        print("Gas    | m       | b")
        for gas, (m, b) in gas_data2.items():
            print(f"{gas.ljust(7)}| {str(m).ljust(8)}| {str(b).ljust(7)}")
    if typ == 3:
        print()
        print("For Old Curve:")
        print()
        print("for ppm = a*ratio^b:")
        print()
        print("Gas    | a       | b")
        for gas, (a, b) in gas_data3.items():
            print(f"{gas.ljust(7)}| {str(a).ljust(8)}| {str(b).ljust(7)}")
    if typ == 4:
        print("for ppm = 10^[(log10(ratio)-b)/m]:")
        print()
        print("Gas    | m       | b")
        for gas, (m, b) in gas_data4.items():
            print(f"{gas.ljust(7)}| {str(m).ljust(8)}| {str(b).ljust(7)}")
            
sensor_name = input("Enter the type of your gas sensor like 'MQ-135': ")

gases = {}

gas_data1 = {}
gas_data2 = {}
gas_data3 = {}
gas_data4 = {}

colornum = ListNumber = 0

fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    specs=[[{"type": "scatter"}, {"type": "scatter"}]],
    subplot_titles=("New Curve", "Old Curve")
)


while True:
    gas_name = input("Enter the gas name (or press 'Enter' to finish): ")
    if gas_name == '':
        break
    else:
        ListNumber += 1

    values = []
    values_input = input(f"Enter (x, y) values for {gas_name} as [(x1, y1), (x2, y2), ...]: ")
    try:
        values = eval(values_input)
        x_values = [value[0] for value in values]
        y_values = [value[1] for value in values]

        x = np.array(x_values)
        y = np.array(y_values)

        def func(x, a, b):
            return a * np.power(x, b)

        popt, pcov = curve_fit(func, x, y)

        residuals = y - func(x, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - (ss_res / ss_tot)

        gases[gas_name] = {'a': popt[0], 'b': popt[1], 'R_squared': r_squared}
        a_rounded_no = round(popt[0], 4)
        b_rounded_no = round(popt[1], 4)
        b2_no = np.log10(popt[0])
        b2_rounded_no = round(b2_no, 4)

        if len(x_values) > 4 and r_squared >= 0.9995:
            print(f"R-squared value for {gas_name} is above 0.9995, plotting against first and last values.")
            x0, y0 = x[0], y[0]
            xn, yn = x[-1], y[-1]
            b = np.log10(yn/y0) / np.log10(xn/x0)
            a = np.power(10, (np.log10(yn) - b * np.log10(xn)))
            gases[gas_name] = {'a': a, 'b': b, 'R_squared': r_squared}
            b2 = np.log10(yn) - b * np.log10(xn)
            b2_rounded = round(b2, 4)
            a_rounded = round(a, 4)
            b_rounded = round(b, 4)
        else:
            a_rounded = a_rounded_no
            b_rounded = b_rounded_no
            b2_rounded = b2_rounded_no
            if r_squared >= 0.9995:
                print(f"R-squared value for {gas_name} is above 0.9995,")
                print(f"however, the number of points identified is not sufficient to fully prove that the curve is exponential,")
                print(f"plotting with default values.")
            elif len(x_values) > 4:
                print(f"R-squared value for {gas_name} is below 0.9995, plotting with default values.")
            else:
                print(f"R-squared value for {gas_name} is below 0.9995,")
                print(f"at the same time number of points identified is not sufficient to fully prove that the curve is exponential,")
                print(f"so plotting with default values.")

        gas_data1[gas_name] = (a_rounded, b_rounded)
        gas_data2[gas_name] = (b_rounded, b2_rounded)
        gas_data3[gas_name] = (a_rounded_no, b_rounded_no)
        gas_data4[gas_name] = (b_rounded_no, b2_rounded_no)

        print(f"logm for {gas_name}: {b_rounded} logb for {gas_name}: {b2_rounded}")
        print(f"valuea for {gas_name}: {a_rounded}, valueb for {gas_name}: {b_rounded}")
        print(f"R-squared for {gas_name}: {r_squared:.4f}")

        new_x = np.linspace(min(x_values), max(x_values), 100)
        new_y1 = a_rounded * np.power(new_x, b_rounded)
        new_y2 = a_rounded_no * np.power(new_x, b_rounded_no)

        colornum += 1

        match colornum:
            case 1: hexcolor = "#40E0D0"  # Turquoise
            case 2: hexcolor = "#87CEFA"  # Light Sky Blue
            case 3: hexcolor = "#007FFF"  # Vivid Sky Blue
            case 4: hexcolor = "#CCCCFF"  # Periwinkle
            case 5: hexcolor = "#87CEEB"  # Sky Blue
            case 6: hexcolor = "#6A5ACD"  # Slate Blue
            case 7: hexcolor = "#4B0082"  # Indigo
            case 8: hexcolor = "#FFA500"  # Orange
            case 9: hexcolor = "#4169E1"  # Royal Blue
            case 10: hexcolor = "#0F52BA" # Sapphire
            case _: hexcolor = "Unknown"
    
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=f'New Datas for {gas_name} (R²={r_squared:.4f})', marker=dict(color=hexcolor)), row=1, col=1)
        fig.add_trace(go.Scatter(x=new_x, y=new_y1, mode='lines', name=f'New Curve: y = {a_rounded} * x^{b_rounded}', marker=dict(color=hexcolor)), row=1, col=1)

        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=f'Old Datas for {gas_name}', marker=dict(color=hexcolor)), row=1, col=2)
        fig.add_trace(go.Scatter(x=new_x, y=new_y2, mode='lines', name=f'Old Curve: y = {a_rounded_no} * x^{b_rounded_no}', marker=dict(color=hexcolor)), row=1, col=2)
        
    except Exception as e:
        print("An error occurred:", e)
        print("Invalid input format. Please enter the values as [(x1, y1), (x2, y2), ...]")

print_gas_table(gas_data1, 1)
print_gas_table(gas_data2, 2)
print_gas_table(gas_data3, 3)
print_gas_table(gas_data4, 4)

fig.update_layout(
    title=f'Regression Curves for {sensor_name}',
    autosize=True,  
    template='plotly_white',
    showlegend=True
)

fig.update_xaxes(title_text="Ppm (y)", row=1, col=1)
fig.update_yaxes(title_text="Ratio (x)", row=1, col=1)
fig.update_xaxes(title_text="Ppm (y)", row=1, col=2)
fig.update_yaxes(title_text="Ratio (x)", row=1, col=2)

fig.show()
fig.write_html(f"{sensor_name}_gas_curves.html")

