
from labjack import ljm
import u3
import Logic
import time

d = u3.U3()



"""
PID = Logic.PID()
PID.setPoint(20.0)
current_point = 20.0

for i in range(0, 1000):
    if i == 10:
        PID.setPoint(50.0)
    value = PID.update(current_point)
    current_point = current_point + value/28
    print(i, current_point)
    time.sleep(.05)
"""