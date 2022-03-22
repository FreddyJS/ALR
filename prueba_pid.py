from simple_pid import PID
import random
import time

pid = PID(1, 0.1, 0.05, setpoint=50)
pid.output_limits = (-100, 100)
pid.sample_time = (0.1) # por defecto 0.01



randomlist = []
for i in range(0,10):
    n = random.randint(1,100)
    randomlist.append(n)


randomlist.clear()
#randomlist = [23, 96, 40, 53, 85, 86, 76, 85, 55, 96]
randomlist = [23, 35, 50, 55, 40, 75, 80, 20, 50, 50, 50]
print(randomlist)


for element in randomlist:
    control = pid(element)
    print (control)
    time.sleep(0.25)
