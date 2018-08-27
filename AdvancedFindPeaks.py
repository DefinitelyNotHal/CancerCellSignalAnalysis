from __future__ import print_function
import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import peakutils
import pdb #for debug
import fractions
#access to the file, and retrive the data
'''
formatedLines=[]
inFile=open('input.csv')
for lines in inFile:
    formatedLine=lines.strip().split(',')
    formatedLines.append(formatedLine)
#formatedLine.remove(formatedLine[0])
formatedLines.remove(formatedLines[0])
print(formatedLines[1])
'''
#Welcome Screen
print('''
         ==========
         = Program=
         ==========
         ''')
#File open, and retrieve data
#inFile= open('69696_diff_231_Run6_19_13_31_Demod8.csv',newline='')
#inFile= open('696_Blood_231_Run16_16_11_00_Demod2.csv',newline='')
#inFile= open('69696_231_Run34_21_41_36_Demod6.csv',newline='')
inFile= open('C:/Users/Hal/Desktop/For HAL/Run34/696_PBS_231_Run34_18_06_40_Demod1.csv',newline='')

#Global Variables
readCSV=csv.reader(inFile)
data=[row for row in readCSV]
xs=[]
ys=[]
x=data[0]
lol=float(x[0])/(210*10**6)
y=data[5]
yzero=[]
yzero4Peak=[]
yzero4Deep=[]
counter=0
#time conversion, xs and ys
for i in x:
    counter=counter+1
    xs.append(float(i)/(210*10**6)-lol)
#plot the graph from x and y values
for i in y:
    ys.append(float(i))
points=np.column_stack((xs,ys))
plt.plot(xs, ys)
plt.savefig('figure1')
print('Figure has been saved in the current folder.')
#determine the baseline
def mostFreNum(aList):
    #find the most frequent number in a list.
    countMost={} #store the count number for each element that has appeared in the list
    maxCount=0
    for i in aList:
        if i in countMost:
            countMost[i]=countMost[i]+1
        else:
            countMost[i]=1
        if countMost[i]>maxCount:
            maxCount=countMost[i]
            mostEle=i
    return mostEle

#baseline=mostFreNum(ys)
# newYSS=[]
# newS=[]
# for i in ys:
#     newYSS.append(round(i, 6))
# print(mostFreNum(ys))
# print(mostFreNum(newYSS))
# baseline=mostFreNum(newYSS)

#print(baseline)
point=plt.ginput(1)
yaxis=point[0][1]
baseline=yaxis
print(yaxis)
#baseline=float(input("Base on the graph, please enter a y value to set up your baseline: "))
amplitudeBase=float(input("please input minimum peak amplitude(the height from your input baseline): "))
for i in range(counter):
    yzero.append(baseline)
for i in range(counter):
    yzero4Peak.append(xs[i]*0+baseline)
for i in range(counter):
    yzero4Deep.append(xs[i]*0+baseline)
plt.plot(xs, yzero,'r--')

#find the peak
count=0
startPoint=0
endPoint=0
starttoend=0
newys=[]
dupys=list(ys)
maxarray=[]
dupysDeeps=list(ys)
countDeeps=0
for i in range(counter):
    if(ys[i]<yzero4Peak[i]):
        dupys[i]=yzero4Peak[i]
#plt.plot(xs,dupys) #this is used for checking on the levelline graph

counter1=0
jcount=0
xPeaks = []
yPeaks = []
for i in range(counter-1):
    if(ys[i]<=yzero[i] and ys[i+1]>yzero[i]):
            #count=count+1
            startPoint=i
            count=count+1
            #print(startPoint)
    elif(ys[i]>=yzero[i] and ys[i+1]<yzero[i] and count%2==1):
                count=0
                endPoint=i
                print(startPoint)
                print(endPoint)
                #starttoend=endPoint-startPoint
                max=ys[startPoint]
                for j in range(startPoint, endPoint):
                    if (ys[j]>max):
                         max=ys[j]
                         jcount = j
                xPeaks.append(xs[jcount])
                yPeaks.append(ys[jcount])
                comp=max-ys[startPoint]

                if(comp>amplitudeBase):
                    counter1=counter1+1
                    print('Peak {} is at ({},{})'.format(counter1,xs[jcount],ys[jcount]))
                    plt.plot(xs[jcount], ys[jcount], 'ro')  # plot the peaks
                        #newys.append(ys[j])
                    #print(peak(newys,starttoend))

print("===============================================================================")
#find the deeps
indexesStartPoint=[]
indexesEndPoint=[]
counter1=0
for i in range(counter):
    if(ys[i]>yzero4Deep[i]):
        dupysDeeps[i]=yzero4Deep[i]
#plt.plot(xs,dupysDeeps) #this is used for checking on the levelline graph
for i in range(counter-1):
    if(dupysDeeps[i]==yzero4Deep[i] and dupysDeeps[i+1]<yzero4Deep[i]):
            startPoint=i
            countDeeps=countDeeps+1
            #print(startPoint)

    elif(dupysDeeps[i]==yzero4Deep[i] and dupysDeeps[i-1]<yzero4Deep[i]):
                countDeeps=0
                endPoint=i

                starttoend=endPoint-startPoint
                max=ys[startPoint]
                for j in range(startPoint, endPoint):
                    if (ys[j]<max):
                         max=ys[j]
                         jcount = j
                comp=abs(max-ys[startPoint])
                if(comp>amplitudeBase):
                    counter1 = counter1 + 1
                    print(startPoint)
                    print(endPoint)
                    print('Deep {} is at ({},{})'.format(counter1, xs[jcount], ys[jcount]))
                    plt.plot(xs[jcount], ys[jcount], 'ro')  # plot the peaks
                    plt.annotate(counter1,(xs[jcount], ys[jcount]),color='black', va='top')
                    indexesStartPoint.append(startPoint)
                    indexesEndPoint.append(endPoint)
                        #newys.append(ys[j])
                    #print(peak(newys,starttoend))
plt.show()
plt.close()
print(indexesStartPoint)
print(indexesEndPoint)
plt.plot(xs, ys)
twoPoints=plt.ginput(2)
print(twoPoints)
print(twoPoints[0][0])
print(twoPoints[1][0])
inSP=0
enSP=0
for i in range(len(xs)):
     if xs[i]==twoPoints[0][0] or (xs[i]<twoPoints[0][0] and xs[i+1]>twoPoints[0][0]):
         inSP=i
     elif xs[i]==twoPoints[1][0] or (xs[i]<twoPoints[1][0] and xs[i+1]>twoPoints[1][0]):
         enSP=i
yrange=[]
for j in range(inSP, enSP):
    yrange.append(ys[j])
def minValue(aList):
    min=aList[0]
    for i in aList:
        if i<min:
            min=i
    return min
yrangePeak=minValue(yrange)
for i in range(len(ys)):
    if ys[i]==yrangePeak:
        print(xs[i],ys[i])
        plt.plot(xs[i],ys[i],'ro')
plt.show()
outFile=open('testing.csv','w',newline='')
writeFile=csv.writer(outFile)
writeFile.writerow(['cell'])
writeFile.writerow(['LevelLine for Impedance Magnitude:',baseline])
writeFile.writerow(['TimeMag (second):']+xs)
writeFile.writerow(['Impedance Magnitude:'])
writeFile.writerow(['Level Line for Impedance Phase:',])
writeFile.writerow(['TimePha (second):'])
writeFile.writerow(['Impedance Phase:'])
outFile.close()