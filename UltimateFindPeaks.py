#Design a program to handling extensive post-processing of data

from __future__ import print_function
import sys
import os
import csv
import glob
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.figure as fig
import pdb #for debug
"""Note: global variable, counter=Total number of elements"""
#menu
#access to file and retrieve the data, no parameters
def getData(csvDirectory):
    #access to file and retrieve the data
    inFile = open(csvDirectory, newline='') #open file
    readCSV = csv.reader(inFile) #stores all the data to readCSV
    data = [row for row in readCSV] #stores the data to data, row by row, strings
    xTime= data[0] #row 0 x time values
    yMagnitude= data[5] #row 6 y Impedance Magnitues values
    yPhase= data[6] #row 7 Impedance Phase values
    xTime1st=float(xTime[0])/(210*10**6) #this is used for time conversion
    global counter #declare variables
    counter =0
    global xTimes, yMagnitudes, yPhases #make them become a global variable, so others can use
    xTimes=[]
    yMagnitudes=[]
    yPhases=[]
    for i in xTime:
        counter = counter + 1 #to keep track of the total number of data
        xTimes.append(float(i)/(210*10**6)-xTime1st) #make the first time element as 0, and convert it to actual time
    for i in yMagnitude:
        yMagnitudes.append(float(i)) #ys for Magnitude
    for i in yPhase:
        yPhases.append(float(i)) #ys for Phase
    inFile.close()

#find the maxValue
def maxValue(aList):
    max=aList[0]
    for i in aList:
        if i>max:
            max=i
    return max

#find the minValue
def minValue(aList):
    min=aList[0]
    for i in aList:
        if i<min:
            min=i
    return min

#find the most frequentValue, a parameter=a List array
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

#define levelLine by the program automatically, one parameter=array, y data values
def autoLevelLine(aList):
    levelLine=[]
    baseLine=mostFreNum(aList)
    for i in range(counter):
        levelLine.append(baseLine)
    return levelLine

#define levelLine by the user
#def userLevelLine(aList):

#find the peaks, two parameters, y data values, and levelLine
def findPeaks(ys,yzero):
    count=0
    maxIndex=0
    maxIndexes=[]
    for i in range(counter-1):
        if (ys[i] <= yzero[i] and ys[i + 1] > yzero[i]):
            count = count + 1
            startPoint = i
        elif (ys[i] >= yzero[i] and ys[i + 1] < yzero[i] and count % 2 == 1):
            count = 0
            endPoint = i
            maxPeak4aRange = ys[startPoint]
            for j in range(startPoint, endPoint):
                if (ys[j] > maxPeak4aRange):
                    maxPeak4aRange = ys[j]
                    maxIndex = j
            maxIndexes.append(maxIndex)
    return maxIndexes

#print peaks based on minimum peak height, 4 parameters=val, Index array[],ys array[],levelLine array[]
def printPeaks(minPeakHeight,aList,ys,yzero):
    xpeaksH=[]
    ypeaksH=[]
    for i in aList:
        height=ys[i]-yzero[i]
        if (height > minPeakHeight):
            xpeaksH.append(xTimes[i])
            ypeaksH.append(ys[i])
    return xpeaksH,ypeaksH

#find the deeps, two parameters, y data values, and levelLine
def findDeeps(ys,yzero):
    count=0
    maxIndex=0
    maxIndexes=[]
    for i in range(counter-1):
        if (ys[i] >= yzero[i] and ys[i + 1] < yzero[i]):
            count = count + 1
            startPoint = i
        elif (ys[i] <= yzero[i] and ys[i + 1] > yzero[i] and count % 2 == 1):
            count = 0
            endPoint = i
            maxDeep4aRange = ys[startPoint]
            for j in range(startPoint, endPoint):
                if (ys[j] < maxDeep4aRange):
                    maxDeep4aRange = ys[j]
                    maxIndex = j
            maxIndexes.append(maxIndex)
    return maxIndexes

#print peaks based on minimum peak height, 4 parameters=val, Index array[],ys array[],levelLine array[]
def printDeeps(minDeepHeight,aList,ys,yzero):
    xDeepsH=[]
    yDeepsH=[]
    for i in aList:
        height=abs(ys[i]-yzero[i])
        if (height > minDeepHeight):
            xDeepsH.append(xTimes[i])
            yDeepsH.append(ys[i])
    return xDeepsH,yDeepsH

#auto main loop
def autoMain(cellCount,rowPlot,colPlot,plotPos,writeFile):
    #auto first
    plt.subplot(rowPlot,colPlot,plotPos)#plt.subplot(rows, columns, positioning)
    plt.title('Cell(s) '+str(cellCount))
    plt.plot(xTimes,yMagnitudes)
    print('Cell(s) '+str(cellCount))
    print('==================================================================')#Impedance Mag. Section
    ryMagnitudes=[]
    for i in yMagnitudes:
        ryMagnitudes.append(round(i,6))
    magLv=autoLevelLine(ryMagnitudes)
    plt.plot(xTimes,magLv,'r--')
    largestValueMag=maxValue(yMagnitudes)
    modifyMagLv=(largestValueMag-magLv[0])*0.05+magLv[0]
    lvMag=[modifyMagLv for i in xTimes]
    print('Level line for magnitude peaks is: ',lvMag[0])
    plt.plot(xTimes, lvMag,'y--')
    maxIndexesMag=findPeaks(yMagnitudes,lvMag)
    # Magnitude Deeps Section
    minimumValueMag = minValue(yMagnitudes)
    # Nagnitude Peaks Section
    if abs(minimumValueMag-magLv[0])> abs(largestValueMag-magLv[0]):    #default min peak height for impedance magnitude
        minPeakHeight=(abs(minimumValueMag-magLv[0]))*0.1
    else:
        minPeakHeight=(largestValueMag-magLv[0])*0.1
    xpeaksH, ypeaksH=printPeaks(minPeakHeight, maxIndexesMag, yMagnitudes, lvMag)
    count=0
    for i in ypeaksH:
        count=count+1
        print('Peak {} is at ({},{})'.format(count, xpeaksH[count-1], ypeaksH[count-1]))
        plt.plot(xpeaksH[count-1], ypeaksH[count-1], 'ro')
    #Magnitude Deeps Section
    modifyMagLv1 = (minimumValueMag - magLv[0]) * 0.05 + magLv[0]
    lvMag1 = [modifyMagLv1 for i in xTimes]
    print('Level line for magnitude deeps is: ', lvMag1[0])
    plt.plot(xTimes, lvMag1, 'y--')
    maxIndexesMag1 = findDeeps(yMagnitudes, lvMag1)
    xdeepsH,ydeepsH=printDeeps(minPeakHeight,maxIndexesMag1,yMagnitudes,lvMag1)
    count = 0
    for i in ydeepsH:
        count = count + 1
        print('Deep {} is at ({},{})'.format(count, xdeepsH[count - 1], ydeepsH[count - 1]))
        plt.plot(xdeepsH[count - 1], ydeepsH[count - 1], 'ro')
    plt.xlabel('Time')
    plt.ylabel('Magnitude')
    print('------------------------------------------------------------------')  # Impedance Phase Section
    plotPos=plotPos+1
    plt.subplot(rowPlot,colPlot,plotPos)
    plt.plot(xTimes, yPhases)
    ryPhases=[]
    for i in yPhases:
        ryPhases.append(round(i,6))
    phaseLv=autoLevelLine(ryPhases)
    print('Level line for phase is: ',phaseLv[0])
    plt.plot(xTimes, phaseLv, 'r--')
    largestValuePha = maxValue(yPhases)
    modifyPhaLv = (largestValuePha - phaseLv[0]) * 0.05 + phaseLv[0]
    lvPha=[modifyPhaLv for i in xTimes]
    print('Level line for phase peaks is: ',lvPha[0])
    plt.plot(xTimes, lvPha,'y--')
    maxIndexesPha=findPeaks(yPhases,lvPha)
    # Phase Deeps Section
    minimumValuePha = minValue(yPhases)
    # Phase Peaks Section
    if abs(minimumValuePha-phaseLv[0])> abs(largestValuePha-phaseLv[0]):    #default min peak height for impedance phase
        minPeakHeight2=(abs(minimumValuePha-phaseLv[0]))*0.1
    else:
        minPeakHeight2=(largestValuePha-phaseLv[0])*0.1
    xpeaksH2, ypeaksH2=printPeaks(minPeakHeight2,maxIndexesPha, yPhases, lvPha)
    count = 0
    for i in ypeaksH2:
        count = count + 1
        print('Peak {} is at ({},{})'.format(count, xpeaksH2[count-1], ypeaksH2[count-1]))
        plt.plot(xpeaksH2[count-1], ypeaksH2[count-1], 'ro')
    #Phase Deeps Section
    modifyPhaLv1 = (minimumValuePha - phaseLv[0]) * 0.05 + phaseLv[0]
    lvPha1 = [modifyPhaLv1 for i in xTimes]
    print('Level line for phase deeps is: ', lvPha1[0])
    plt.plot(xTimes, lvPha1, 'y--')
    maxIndexesPha2 = findDeeps(yPhases, lvPha1)
    xdeepsH2, ydeepsH2 = printDeeps(minPeakHeight2, maxIndexesPha2, yPhases, lvPha1)
    count = 0
    for i in ydeepsH2:
        count = count + 1
        print('Deep {} is at ({},{})'.format(count, xdeepsH2[count - 1], ydeepsH2[count - 1]))
        plt.plot(xdeepsH2[count - 1], ydeepsH2[count - 1], 'ro')
    print('==================================================================')#End of Section
    plt.xlabel('Time')
    plt.ylabel('Phase')
    #outFileFormat
    writeFile.writerow(['Cell(s) '+ str(cellCount)])
    writeFile.writerow(['Central Level Line for Impedance Magnitude(s):',magLv[0]])
    writeFile.writerow(['LevelLine for Magnitude Peaks:', lvMag[0]])
    writeFile.writerow(['TimeMag Peaks(second):']+ xpeaksH)
    writeFile.writerow(['Magnitude Peaks:']+ypeaksH)
    writeFile.writerow(['LevelLine for Magnitude Deeps:', lvMag1[0]])
    writeFile.writerow(['TimeMag Deeps(second):']+ xdeepsH)
    writeFile.writerow(['Magnitude Deeps:']+ydeepsH)
    writeFile.writerow(['Central Level Line for Impedance Phase(s):',phaseLv[0]])
    writeFile.writerow(['LevelLine for Phase Peaks:', lvPha[0]])
    writeFile.writerow(['TimePha Peaks(second):']+ xpeaksH2)    
    writeFile.writerow(['Phase Peaks:']+ypeaksH2)
    writeFile.writerow(['LevelLine for Phase Deeps:', lvPha1[0]])
    writeFile.writerow(['TimePha Deeps(second):']+ xdeepsH2)
    writeFile.writerow(['Phase Deeps:']+ydeepsH2)

def main():
    #Auto
    #directory=path+fileName="C:/Users/Hal/Desktop/For HAL/Run34/69696_231_Run34_21_41_36_Demod1.csv"
    #path=input("Please input the file path:")
    # while os.path.exists(path)!=True:
    #     path=input('Incorrect Path, please input the path again.\n')
    path = "C:/Users/Hal/Desktop/For HAL/Run34/"
    fileNameorNot=input("Open a single csv file(y/n)?\nOtherwise, it will open and load all the csv files in the folder.")
    print(fileNameorNot)
    if fileNameorNot=='yes' or fileNameorNot=='Yes' or fileNameorNot=='Y' or fileNameorNot=='YES' or fileNameorNot=='y':
        # fileName=input("Please input the file name(.csv at the end): ")
        # while os.path.isfile(path + fileName) != True:
        #     print('File is not found!')
        #     fileName=input("Please input the file name(.csv at the end): ")
        fileName='69696_231_Run23_20_58_13_Demod3.csv'
        singleCSVFile=path+fileName
        getData(singleCSVFile)
        plt.figure(1)
        totalRowPlot=2
        totalColPlot=2
        totalPlotPos=1
        cellCounter=1
        outFile = open('output'+fileName, 'w', newline='')
        writeFile = csv.writer(outFile)
        autoMain(cellCounter,totalRowPlot,totalColPlot,totalPlotPos,writeFile)
        outFile.close()
        plt.show()
    elif fileNameorNot=='no' or fileNameorNot=='No' or fileNameorNot=='N' or fileNameorNot=='NO' or fileNameorNot=='n':
        files = glob.glob(path + "*.csv")
        cellCounter=0
        totalRowPlot=0
        plt.figure(1)
        for fileDirectory in files:
            totalRowPlot=totalRowPlot+1
        totalColPlot = 2
        totalPlotPos = 1
        pathHolder = path.split("/")
        outFile = open('output'+pathHolder[5]+'.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter=cellCounter+1
            getData(fileDirectory)
            autoMain(cellCounter,totalRowPlot,totalColPlot,totalPlotPos,writeFile)
            totalPlotPos = totalPlotPos + 2
        outFile.close()
        plt.show()
    else:
        print("Proceeding to the User Interface.")
    #User's Interface
 #   userChoice=input("Do you want to modify any graphs? if so, please input the cell(s) number: ")
if __name__ == '__main__':
    main()