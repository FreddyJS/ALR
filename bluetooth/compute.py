# CURRENT FILES :
# deviceOntop.txt : 230 samples of rssi received when beacon emitting at 0dbm
#  deviceOntop_-7dbm.txt: 190 samples of rssi received when beacon emitting at -7dbm (the package is defined for -7dbm but when we click on transmit it sets to 0)
# deviceOntopMeasureTime.txt: 10 samples over 1 second when transmitting at 0dbm
import numpy as np
import matplotlib.pyplot as plt



# Read file device output
f = open("deviceOnTop.txt", "r")
init = 1647956251
end = 1647956289
seconds = end - init
rssiValues= []
valorRef = 0
count = 0
medians =[]
for i in f:
    splt = i.split(' ')
    if("RSSI received:" in i):
        rssiValues.append(int(splt[2]))
        count=count+1
    if("Valor de referencia:" in i):
        valorRef = int(splt[3])
    if("Valor mediano calculado:" in i):
        # str="%s %s"%(count,splt[3])
        medians.append((int(count),int(splt[3])))
# medianValue = np.median(rssiValues)
title = 'RSSI values received for the total of %i samples when both moving over %i seconds'%(len(rssiValues),seconds)
time=np.linspace(0,seconds,num=int(len(rssiValues))) 
# print(time)
# title = 'RSSI values received for 3.089222338 second of scan when beacon moving away (%i samples)'%(len(rssiValues))
medianLabel = 'Valor de referencia: %i'%(valorRef)
fig, ax = plt.subplots()
rssiPlot = ax.plot(rssiValues, label='RSSI')
medianPlot = ax.axhline(valorRef,color='red',label=medianLabel)
# ax.legend(handles=[rssiPlot,medianPlot])
plt.title(title)
for x,y in medians:
    plt.scatter(x,y,color="black")
plt.show()
# plt.plot(rssiValues)
# plt.axhline(medianValue,color='red')
# plt.legend(rssiPlot,medianplot)
