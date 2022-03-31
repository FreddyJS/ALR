import numpy as np
import matplotlib.pyplot as plt



# Read file device output
f = open("deviceOnTop300.txt", "r")
# seconds = end - init
rssiValues= []
valorRef = 0
count = 0
medians =[]
time = []
for i in f:
    splt = i.split(' ')
    if("RSSI received:" in i):
        rssiValues.append(int(splt[2]))
        time.append(int(splt[3])/1000000)
        count=count+1
    if("Valor de referencia:" in i):
        valorRef = int(splt[3])
        timeRef = time[-1]
    if("Valor mediano calculado:" in i):
        # str="%s %s"%(count,splt[3])
        medians.append((int(splt[3]),time[-1]))
        
# medianValue = np.median(rssiValues)
title = 'RSSI values received for the total of %i samples when both moving over %i seconds'%(len(rssiValues),time[-1])
# time=np.linspace(0,rssiValues,num=int(len(rssiValues))) 
# print(time)
# title = 'RSSI values received for 3.089222338 second of scan when beacon moving away (%i samples)'%(len(rssiValues))
medianLabel = 'Valor de referencia: %i'%(valorRef)
fig, ax = plt.subplots()
rssiPlot = ax.plot(time,rssiValues, label='RSSI')
medianPlot = ax.axhline(valorRef,color='red',label=medianLabel)
plt.title(title)
for x,y in medians:
    s = plt.scatter(y,x,color="black")
ax.legend(handles=[rssiPlot[0],medianPlot])
plt.show()

# plt.plot(rssiValues)
# plt.axhline(medianValue,color='red')
# plt.legend(rssiPlot,medianplot)
