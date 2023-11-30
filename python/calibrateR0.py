RSR0MQAir = int(input("Define your MQAir RS/R0: ")) # RS/R0 VALUE

"""
---RS/R0 VALUE---
MQ-2: 9.83
MQ-3: 60
MQ-4: 4.4
MQ-5: 6.5
MQ-6: 10
MQ-7: 27.5
MQ-8: 70
MQ-9: 9.6
MQ-131: 15
MQ-135: 3.6
MQ-136: 3.6
MQ-303A: 1
MQ-309A: 11
"""

Rload =  int(input("Define your resistor value (kΩ): ")) # Define your Rload

percentile = int(input("Define the percentile you want to calibrate %0-100: "))

def calculateR0VeryEasy(defpercentile):
    RS = (100 * Rload / defpercentile) - Rload
    R0 = RS / RSR0MQAir
    return R0

MyR0value = calculateR0VeryEasy(percentile) 

print("Your R0 value is:")
print(MyR0value)
