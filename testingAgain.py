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
    xTime= data[0]
    yMagnitude= data[5]
    yPhase= data[6]
    xTime1st=float(xTime[0])/(210*10**6) #this is used for time conversion
    global counter #declare variables
    counter =0
    global xTimes, yMagnitudes, yPhases,pointsTimePha,pointsTimeMag #make them become a global variable, so others can use
    xTimes=[]
    yMagnitudes=[]
    yPhases=[]
    for i in xTime:
        counter = counter + 1
        xTimes.append(float(i)/(210*10**6)-xTime1st) #make the first time element as 0, and convert it to actual time
    for i in yMagnitude:
        yMagnitudes.append(float(i))
    for i in yPhase:
        yPhases.append(float(i))
    pointsTimeMag=np.column_stack((xTimes,yMagnitudes)) #tuple for Magnitude over Time
    pointsTimePha=np.column_stack((xTimes,yPhases)) #tuple for Phase over Time

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
#testing
#find the peaks, two parameters, y data values, and levelLine
def sefindPeaks(ys,yzero,minPeakHeight):
    count=0
    indexesStart=[]
    indexesEnd=[]
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
            height=maxPeak4aRange-yzero[startPoint]
            if (height>minPeakHeight):
                indexesStart.append(startPoint)
                indexesEnd.append(endPoint)
    return indexesStart, indexesEnd
def peakHeight(ys, startList,endList):
    heightList=[]
    jpeakindexes=[]
    jpeakindex=0
    for i in range(len(startList)):
        maxPeakinaRange=ys[startList[i]]
        for j in range(startList[i], endList[i]):
            if(ys[j]>maxPeakinaRange):
                maxPeakinaRange=ys[j]
                jpeakindex=j
        jpeakindexes.append(jpeakindex)
        heightList.append(maxPeakinaRange-ys[startList[i]])
    return heightList,jpeakindexes
def sefindDeeps(ys,yzero,minDeepHeight):
    count=0
    indexesStart=[]
    indexesEnd=[]
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
            height=abs(maxDeep4aRange-yzero[startPoint])
            if (height > minDeepHeight):
                indexesStart.append(startPoint)
                indexesEnd.append(endPoint)
    return indexesStart, indexesEnd
def deepHeight(ys, startList,endList):
    absheightList=[]
    heightList=[]
    jpeakindexes=[]
    jpeakindex=0
    for i in range(len(startList)):
        maxPeakinaRange=ys[startList[i]]
        for j in range(startList[i], endList[i]):
            if(ys[j]<maxPeakinaRange):
                maxPeakinaRange=ys[j]
                jpeakindex=j
        jpeakindexes.append(jpeakindex)
        absheightList.append(abs(maxPeakinaRange-ys[startList[i]]))
        heightList.append(maxPeakinaRange-ys[startList[i]])
    return heightList,absheightList,jpeakindexes
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
    modifyMagLv=(largestValueMag-magLv[0])*0.025+magLv[0]
    lvMag=[modifyMagLv for i in xTimes]
    print('Level line for magnitude peaks is: ',lvMag[0])
    plt.plot(xTimes, lvMag,'y--')
    maxIndexesMag=findPeaks(yMagnitudes,lvMag)
    # Magnitude Deeps Section
    minimumValueMag = minValue(yMagnitudes)
    # Nagnitude Peaks Section
    if abs(minimumValueMag-magLv[0])> abs(largestValueMag-magLv[0]):    #default min peak height for impedance magnitude
        minPeakHeight=(abs(minimumValueMag-magLv[0]))*0.05
    else:
        minPeakHeight=(largestValueMag-magLv[0])*0.05
    xpeaksH, ypeaksH=printPeaks(minPeakHeight, maxIndexesMag, yMagnitudes, lvMag)
    count=0
    for i in ypeaksH:
        count=count+1
        print('Peak {} is at ({},{})'.format(count, xpeaksH[count-1], ypeaksH[count-1]))
        plt.plot(xpeaksH[count-1], ypeaksH[count-1], 'ro')
    #Magnitude Deeps Section
    modifyMagLv1 = (minimumValueMag - magLv[0]) * 0.025 + magLv[0]
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
    modifyPhaLv = (largestValuePha - phaseLv[0]) * 0.025 + phaseLv[0]
    lvPha=[modifyPhaLv for i in xTimes]
    print('Level line for magnitude peaks is: ',lvPha[0])
    plt.plot(xTimes, lvPha,'y--')
    maxIndexesPha=findPeaks(yPhases,lvPha)
    # Phase Deeps Section
    minimumValuePha = minValue(yPhases)
    # Phase Peaks Section
    if abs(minimumValuePha-phaseLv[0])> abs(largestValuePha-phaseLv[0]):    #default min peak height for impedance phase
        minPeakHeight2=(abs(minimumValuePha-phaseLv[0]))*0.05
    else:
        minPeakHeight2=(largestValuePha-phaseLv[0])*0.05
    xpeaksH2, ypeaksH2=printPeaks(minPeakHeight2,maxIndexesPha, yPhases, lvPha)
    count = 0
    for i in ypeaksH2:
        count = count + 1
        print('Peak {} is at ({},{})'.format(count, xpeaksH2[count-1], ypeaksH2[count-1]))
        plt.plot(xpeaksH2[count-1], ypeaksH2[count-1], 'ro')
    #Phase Deeps Section
    modifyPhaLv1 = (minimumValuePha - phaseLv[0]) * 0.025 + phaseLv[0]
    lvPha1 = [modifyPhaLv1 for i in xTimes]
    print('Level line for magnitude deeps is: ', lvPha1[0])
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
    #user section
    #minPeakHeight = float(input("please input minimum peak amplitude(the height from your input baseline): "))
    #printPeaks(minPeakHeight,)

#User main loop
def autoMain2(cellCount,rowPlot,colPlot,plotPos,writeFile):
    # auto first
    plt.subplot(rowPlot, colPlot, plotPos)  # plt.subplot(rows, columns, positioning)
    plt.plot(xTimes, yMagnitudes)
    print('=====================Impedance Mag. Section============================')  # Impedance Mag. Section
    ryMagnitudes = []
    for i in yMagnitudes:
        ryMagnitudes.append(round(i, 6))
    magLv = autoLevelLine(ryMagnitudes)
    plt.plot(xTimes, magLv, 'r--')
    largestValueMag = maxValue(yMagnitudes)
    modifyMagLv = (largestValueMag - magLv[0]) * 0.021 + magLv[0]
    lvMag = [modifyMagLv for i in xTimes]
    print('Level line: ',magLv[0]) #central level line
    #print('Level line for magnitude peaks is: ', lvMag[0]) #level line assistant
    plt.plot(xTimes, lvMag, 'r--')
    maxIndexesMag = findPeaks(yMagnitudes, lvMag)
    # Magnitude Deeps Section
    minimumValueMag = minValue(yMagnitudes)
    # Nagnitude Peaks Section
    if abs(minimumValueMag - magLv[0]) > abs(largestValueMag - magLv[0]):  # default min peak height for impedance magnitude
        minPeakHeight = (abs(minimumValueMag - magLv[0])) * 0.08
    else:
        minPeakHeight = (largestValueMag - magLv[0]) * 0.08
    xpeaksH, ypeaksH = printPeaks(minPeakHeight, maxIndexesMag, yMagnitudes, lvMag)
    startPointsMagP, endPointsMagP=sefindPeaks(yMagnitudes,lvMag, minPeakHeight)
    count = 0
    for i in ypeaksH:
        count = count + 1
        print('Peak {} is at ({},{})'.format(count, xpeaksH[count - 1], ypeaksH[count - 1]))
        plt.plot(xpeaksH[count - 1], ypeaksH[count - 1], 'ro')
    # Magnitude Deeps Section
    modifyMagLv1 = (minimumValueMag - magLv[0]) * 0.021 + magLv[0]
    lvMag1 = [modifyMagLv1 for i in xTimes]
    #print('Level line for magnitude deeps is: ', lvMag1[0]) #level line assistant
    plt.plot(xTimes, lvMag1, 'r--')
    maxIndexesMag1 = findDeeps(yMagnitudes, lvMag1)
    xdeepsH, ydeepsH = printDeeps(minPeakHeight, maxIndexesMag1, yMagnitudes, lvMag1)
    startPointsMagD,endPointsMagD=sefindDeeps(yMagnitudes, lvMag1,minPeakHeight)
    global startPointsMag, endPointsMag
    startPointsMag=[]
    endPointsMag=[]
    if ((not startPointsMagD) or (not endPointsMagD)) or (len(startPointsMagD)<len(startPointsMagP)):
        startPointsMag=list(startPointsMagP)
        endPointsMag=list(endPointsMagP)
    else:
        startPointsMag=list(startPointsMagD)
        endPointsMag=list(endPointsMagD)

    count = 0
    for i in ydeepsH:
        count = count + 1
        print('Deep {} is at ({},{})'.format(count, xdeepsH[count - 1], ydeepsH[count - 1]))
        plt.plot(xdeepsH[count - 1], ydeepsH[count - 1], 'ro')
    plt.xlabel('Time')
    plt.ylabel('Magnitude '+ str(cellCount))
    print('-------------------Impedance Phase Section------------------------')  # Impedance Phase Section
    plotPos = plotPos + 1
    plt.subplot(rowPlot, colPlot, plotPos)
    plt.plot(xTimes, yPhases)
    ryPhases = []
    for i in yPhases:
        ryPhases.append(round(i, 6))
    phaseLv = autoLevelLine(ryPhases)
    print('Level line for phase is: ', phaseLv[0])
    plt.plot(xTimes, phaseLv, 'r--')
    largestValuePha = maxValue(yPhases)
    modifyPhaLv = (largestValuePha - phaseLv[0]) * 0.021 + phaseLv[0]
    lvPha = [modifyPhaLv for i in xTimes]
    #print('Level line for phase peaks is: ', lvPha[0]) #Level line assistant
    plt.plot(xTimes, lvPha, 'r--')
    maxIndexesPha = findPeaks(yPhases, lvPha)
    # Phase Deeps Section
    minimumValuePha = minValue(yPhases)
    # Phase Peaks Section
    if abs(minimumValuePha - phaseLv[0]) > abs(largestValuePha - phaseLv[0]):  # default min peak height for impedance phase
        minPeakHeight2 = (abs(minimumValuePha - phaseLv[0])) * 0.08
    else:
        minPeakHeight2 = (largestValuePha - phaseLv[0]) * 0.08
    xpeaksH2, ypeaksH2 = printPeaks(minPeakHeight2, maxIndexesPha, yPhases, lvPha)
    startPointsPhaP, endPointsPhaP = sefindPeaks(yPhases, lvPha, minPeakHeight2)

    count = 0
    for i in ypeaksH2:
        count = count + 1
        print('Peak {} is at ({},{})'.format(count, xpeaksH2[count - 1], ypeaksH2[count - 1]))
        plt.plot(xpeaksH2[count - 1], ypeaksH2[count - 1], 'ro')
    # Phase Deeps Section
    modifyPhaLv1 = (minimumValuePha - phaseLv[0]) * 0.021 + phaseLv[0]
    lvPha1 = [modifyPhaLv1 for i in xTimes]
    #print('Level line for phase deeps is: ', lvPha1[0])
    plt.plot(xTimes, lvPha1, 'r--')
    maxIndexesPha2 = findDeeps(yPhases, lvPha1)
    xdeepsH2, ydeepsH2 = printDeeps(minPeakHeight2, maxIndexesPha2, yPhases, lvPha1)
    startPointsPhaD, endPointsPhaD = sefindDeeps(yPhases, lvPha1, minPeakHeight2)

    global startPointsPha,endPointsPha
    startPointsPha= []
    endPointsPha = []

    if (not startPointsPhaD) or (not endPointsPhaD) or (len(startPointsPhaD)<len(startPointsPhaP)):
        startPointsPha=list(startPointsPhaP)
        endPointsPha=list(endPointsPhaP)
    else:
        startPointsPha=list(startPointsPhaD)
        endPointsPha=list(endPointsPhaD)

    count = 0
    for i in ydeepsH2:
        count = count + 1
        print('Deep {} is at ({},{})'.format(count, xdeepsH2[count - 1], ydeepsH2[count - 1]))
        plt.plot(xdeepsH2[count - 1], ydeepsH2[count - 1], 'ro')
    print('====================== End of Section================================')  # End of Section
    plt.xlabel('Time')
    plt.ylabel('Phase '+ str(cellCount))
    # outFileFormat
    writeFile.writerow(['Cell(s) ' + str(cellCount)])
    writeFile.writerow(['Central Level Line for Impedance Magnitude(s):', magLv[0]])
    #writeFile.writerow(['LevelLine for Magnitude Peaks:', lvMag[0]])
    writeFile.writerow(['TimeMag Peaks(second):'] + xpeaksH)
    writeFile.writerow(['Magnitude Peaks:'] + ypeaksH)
    #writeFile.writerow(['LevelLine for Magnitude Deeps:', lvMag1[0]])
    writeFile.writerow(['TimeMag Deeps(second):'] + xdeepsH)
    writeFile.writerow(['Magnitude Deeps:'] + ydeepsH)
    writeFile.writerow(['Central Level Line for Impedance Phase(s):', phaseLv[0]])
    #writeFile.writerow(['LevelLine for Phase Peaks:', lvPha[0]])
    writeFile.writerow(['TimePha Peaks(second):'] + xpeaksH2)
    writeFile.writerow(['Phase Peaks:'] + ypeaksH2)
    #writeFile.writerow(['LevelLine for Phase Deeps:', lvPha1[0]])
    writeFile.writerow(['TimePha Deeps(second):'] + xdeepsH2)
    writeFile.writerow(['Phase Deeps:'] + ydeepsH2)
def autoMain3(cellCount,rowPlot,colPlot,plotPos,writeFile):
    # auto first
    plt.subplot(rowPlot, colPlot, plotPos)  # plt.subplot(rows, columns, positioning)
    plt.plot(xTimes, yMagnitudes)
    print('==================================================================')  # Impedance Mag. Section
    magHeight,indexesMagP=peakHeight(yMagnitudes,startPointsMag,endPointsMag)
    magHeight1,absmagHeight1, indexesMagD=deepHeight(yMagnitudes,startPointsMag,endPointsMag)
    phaHeight, indexesPhaP=peakHeight(yPhases,startPointsMag,endPointsMag)
    phaHeight1, absphaHeight1, indexesPhaD=deepHeight(yPhases,startPointsMag,endPointsMag)
    global xpeak, ypeak, xdeep, ydeep, xpeakP, ypeakP, xdeepP, ydeepP
    xpeak=[]
    ypeak=[]
    xdeep=[]
    ydeep=[]
    xpeakP=[]
    ypeakP=[]
    xdeepP=[]
    ydeepP=[]
    for i in startPointsMag:
        plt.plot(xTimes[i],yMagnitudes[i],'o', color='orange')
        #plt.plot(xTimes[i],yPhases[i],'o',color='orange')
    for i in endPointsMag:
        plt.plot(xTimes[i],yMagnitudes[i],'o', color='orange')
        #plt.plot(xTimes[i],yPhases[i],'o',color='orange')
    if max(magHeight)>max(absmagHeight1):
        for i in indexesMagP:
            plt.plot(xTimes[i],yMagnitudes[i],'yo')
            xpeak.append(xTimes[i])
            ypeak.append(yMagnitudes[i])
        writeFile.writerow(['Impedance Peaks' + str(cellCount) + ':']+ ypeak)
        writeFile.writerow(['Height' + str(cellCount) + ':']+magHeight)
    elif max(magHeight)<max(absmagHeight1):
        for i in indexesMagD:
            plt.plot(xTimes[i],yMagnitudes[i],'ro')
            xdeep.append(xTimes[i])
            ydeep.append(yMagnitudes[i])
        writeFile.writerow(['Impedance Deeps' + str(cellCount) + ':']+ydeep)
        writeFile.writerow(['Height' + str(cellCount) + ':']+ magHeight1)
    plt.xlabel('Time')
    plt.ylabel('Magnitude ' +  str(cellCount))
    print('------------------------------------------------------------------')  # Impedance Phase Section
    plotPos = plotPos + 1
    plt.subplot(rowPlot, colPlot, plotPos)
    plt.plot(xTimes, yPhases)
    if max(phaHeight)>max(absphaHeight1):
        count=0
        for i in indexesPhaP:
            count=count+1
            plt.plot(xTimes[i], yPhases[i], 'yo')
            xpeakP.append(xTimes[i])
            ypeakP.append(yPhases[i])
            print('Peak {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
        writeFile.writerow(['Phase Peaks'+str(cellCount)+':']+ypeakP)
        writeFile.writerow(['Height'+str(cellCount)+':']+phaHeight)
    elif max(phaHeight)<max(absphaHeight1):
        count=0
        for i in indexesPhaD:
            count=count+1
            plt.plot(xTimes[i], yPhases[i], 'ro')
            xdeepP.append(xTimes[i])
            ydeepP.append(yPhases[i])
            print('Deep {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
        writeFile.writerow(['Phase Deeps'+str(cellCount)+':']+ydeepP)
        writeFile.writerow(['Height' + str(cellCount) + ':']+phaHeight1)
    print('==================================================================')  # End of Section
    plt.xlabel('Time')
    plt.ylabel('Phase '+ str(cellCount))
def autoMain4(cellCount,rowPlot,colPlot,plotPos,writeFile):
    # auto first
    plt.subplot(rowPlot, colPlot, plotPos)  # plt.subplot(rows, columns, positioning)
    plt.plot(xTimes, yMagnitudes)
    print('==================================================================')  # Impedance Mag. Section
    magHeight,indexesMagP=peakHeight(yMagnitudes,startPointsMag,endPointsMag)
    magHeight1,absmagHeight1, indexesMagD=deepHeight(yMagnitudes,startPointsMag,endPointsMag)
    phaHeight, indexesPhaP=peakHeight(yPhases,startPointsMag,endPointsMag)
    phaHeight1, absphaHeight1, indexesPhaD=deepHeight(yPhases,startPointsMag,endPointsMag)
    xpeak=[]
    ypeak=[]
    xdeep=[]
    ydeep=[]
    xpeakP=[]
    ypeakP=[]
    xdeepP=[]
    ydeepP=[]
    count=0
    for i in indexesMagP:
        if xTimes[i] != 0:
            if yMagnitudes[i - 1] < yMagnitudes[i] and yMagnitudes[i] > yMagnitudes[i + 1]:
                count = count + 1
                plt.plot(xTimes[i],yMagnitudes[i],'yo')
                plt.annotate(count, (xTimes[i], yMagnitudes[i]), color='black', va='top')
                xpeak.append(xTimes[i])
                ypeak.append(yMagnitudes[i])
    writeFile.writerow(['Impedance Peaks' + str(cellCount) + ':']+ ypeak)
    writeFile.writerow(['Height' + str(cellCount) + ':']+magHeight)
    count = 0
    for i in indexesMagD:
        if xTimes[i] != 0:
            if (yMagnitudes[i - 1] > yMagnitudes[i] and yMagnitudes[i] < yMagnitudes[i + 1]):
                count = count + 1
                plt.plot(xTimes[i],yMagnitudes[i],'ro')
                plt.annotate(count, (xTimes[i], yMagnitudes[i]), color='black', va='top')
                xdeep.append(xTimes[i])
                ydeep.append(yMagnitudes[i])
    writeFile.writerow(['Impedance Deeps' + str(cellCount) + ':']+ydeep)
    writeFile.writerow(['Height' + str(cellCount) + ':']+ magHeight1)
    plt.xlabel('Time')
    plt.ylabel('Magnitude ' +  str(cellCount))
    print('------------------------------------------------------------------')  # Impedance Phase Section
    plotPos = plotPos + 1
    plt.subplot(rowPlot, colPlot, plotPos)
    plt.plot(xTimes, yPhases)

    count=0
    for i in indexesPhaP:
        if xTimes[i] !=0:
            if (yPhases[i - 1] < yPhases[i] and yPhases[i] > yPhases[i + 1]):
                count=count+1
                plt.plot(xTimes[i], yPhases[i], 'yo')
                plt.annotate(count, (xTimes[i], yPhases[i]), color='black', va='top')
                xpeakP.append(xTimes[i])
                ypeakP.append(yPhases[i])
                print('Peak {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
    writeFile.writerow(['Phase Peaks'+str(cellCount)+':']+ypeakP)
    writeFile.writerow(['Height'+str(cellCount)+':']+phaHeight)
    count=0
    for i in indexesPhaD:
        if xTimes[i] !=0:
            if (yPhases[i - 1] > yPhases[i] and yPhases[i] < yPhases[i + 1]):
                count=count+1
                plt.plot(xTimes[i], yPhases[i], 'ro')
                plt.annotate(count, (xTimes[i], yPhases[i]), color='black', va='top')
                xdeepP.append(xTimes[i])
                ydeepP.append(yPhases[i])
                print('Deep {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
    writeFile.writerow(['Phase Deeps'+str(cellCount)+':']+ydeepP)
    writeFile.writerow(['Height' + str(cellCount) + ':']+phaHeight1)
    print('==================================================================')  # End of Section
    plt.xlabel('Time')
    plt.ylabel('Phase '+ str(cellCount))
def autoMain5(cellCount,rowPlot,colPlot,plotPos,writeFile):
    # auto first
    plt.subplot(rowPlot, colPlot, plotPos)  # plt.subplot(rows, columns, positioning)
    plt.plot(xTimes, yMagnitudes)
    print('==================================================================')  # Impedance Mag. Section
    magHeight,indexesMagP=peakHeight(yMagnitudes,startPointsMag,endPointsMag)
    magHeight1,absmagHeight1, indexesMagD=deepHeight(yMagnitudes,startPointsMag,endPointsMag)
    phaHeight, indexesPhaP=peakHeight(yPhases,startPointsMag,endPointsMag)
    phaHeight1, absphaHeight1, indexesPhaD=deepHeight(yPhases,startPointsMag,endPointsMag)
    global xpeak,ypeak,xdeep,ydeep,xpeakP,ypeakP,xdeepP,ydeepP, indexesPeak,indexesDeep,indexesPeakP,indexesDeepP
    xpeak=[]
    ypeak=[]
    xdeep=[]
    ydeep=[]
    indexesPeak=[]
    indexesDeep=[]
    xpeakP=[]
    ypeakP=[]
    indexesPeakP=[]
    xdeepP=[]
    ydeepP=[]
    indexesDeepP=[]
    count=0
    for i in indexesMagP:
        if xTimes[i] != 0:
            if yMagnitudes[i - 1] < yMagnitudes[i] and yMagnitudes[i] > yMagnitudes[i + 1]:
                count = count + 1
                plt.plot(xTimes[i],yMagnitudes[i],'yo')
                plt.annotate(count, (xTimes[i], yMagnitudes[i]), color='black', va='top')
                xpeak.append(xTimes[i])
                ypeak.append(yMagnitudes[i])
                indexesPeak.append(i)
    writeFile.writerow(['Impedance Peaks' + str(cellCount) + ':']+ ypeak)
    writeFile.writerow(['Height' + str(cellCount) + ':']+magHeight)
    count = 0
    for i in indexesMagD:
        if xTimes[i] != 0:
            if (yMagnitudes[i - 1] > yMagnitudes[i] and yMagnitudes[i] < yMagnitudes[i + 1]):
                count = count + 1
                plt.plot(xTimes[i],yMagnitudes[i],'ro')
                plt.annotate(count, (xTimes[i], yMagnitudes[i]), color='black', va='top')
                xdeep.append(xTimes[i])
                ydeep.append(yMagnitudes[i])
                indexesDeep.append(i)
    writeFile.writerow(['Impedance Deeps' + str(cellCount) + ':']+ydeep)
    writeFile.writerow(['Height' + str(cellCount) + ':']+ magHeight1)
    plt.xlabel('Time')
    plt.ylabel('Magnitude ' +  str(cellCount))
    print('------------------------------------------------------------------')  # Impedance Phase Section
    plotPos = plotPos + 1
    plt.subplot(rowPlot, colPlot, plotPos)
    plt.plot(xTimes, yPhases)

    count=0
    for i in indexesPhaP:
        if xTimes[i] !=0:
            if (yPhases[i - 1] < yPhases[i] and yPhases[i] > yPhases[i + 1]):
                count=count+1
                plt.plot(xTimes[i], yPhases[i], 'yo')
                plt.annotate(count, (xTimes[i], yPhases[i]), color='black', va='top')
                xpeakP.append(xTimes[i])
                ypeakP.append(yPhases[i])
                indexesPeakP.append(i)
                print('Peak {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
    writeFile.writerow(['Phase Peaks'+str(cellCount)+':']+ypeakP)
    writeFile.writerow(['Height'+str(cellCount)+':']+phaHeight)
    count=0
    for i in indexesPhaD:
        if xTimes[i] !=0:
            if (yPhases[i - 1] > yPhases[i] and yPhases[i] < yPhases[i + 1]):
                count=count+1
                plt.plot(xTimes[i], yPhases[i], 'ro')
                plt.annotate(count, (xTimes[i], yPhases[i]), color='black', va='top')
                xdeepP.append(xTimes[i])
                ydeepP.append(yPhases[i])
                indexesDeepP.append(i)
                print('Deep {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
    writeFile.writerow(['Phase Deeps'+str(cellCount)+':']+ydeepP)
    writeFile.writerow(['Height' + str(cellCount) + ':']+phaHeight1)
    print('==================================================================')  # End of Section
    plt.xlabel('Time')
    plt.ylabel('Phase '+ str(cellCount))
def ultimateAutoMain(cellCount,rowPlot,colPlot,plotPos,writeFile,startPoints,endPoints):
    # auto first
    plt.subplot(rowPlot, colPlot, plotPos)  # plt.subplot(rows, columns, positioning)
    plt.plot(xTimes, yMagnitudes)
    print('======================Impedance Mag. Section=========================')  # Impedance Mag. Section
    magHeight,indexesMagP=peakHeight(yMagnitudes,startPoints,endPoints)
    magHeight1,absmagHeight1, indexesMagD=deepHeight(yMagnitudes,startPoints,endPoints)
    phaHeight, indexesPhaP=peakHeight(yPhases,startPoints,endPoints)
    phaHeight1, absphaHeight1, indexesPhaD=deepHeight(yPhases,startPoints,endPoints)
    global xpeak,ypeak,xdeep,ydeep,xpeakP,ypeakP,xdeepP,ydeepP, indexesPeak,indexesDeep,indexesPeakP,indexesDeepP
    xpeak=[]
    ypeak=[]
    xdeep=[]
    ydeep=[]
    indexesPeak=[]
    indexesDeep=[]
    xpeakP=[]
    ypeakP=[]
    indexesPeakP=[]
    xdeepP=[]
    ydeepP=[]
    indexesDeepP=[]
    count=0
    if max(magHeight) > max(absmagHeight1):
        for i in indexesMagP:
            if xTimes[i] != 0:
                if yMagnitudes[i - 1] < yMagnitudes[i] and yMagnitudes[i] > yMagnitudes[i + 1]:
                    count = count + 1
                    plt.plot(xTimes[i],yMagnitudes[i],'yo')
                    plt.annotate(count, (xTimes[i], yMagnitudes[i]), color='black', va='top')
                    xpeak.append(xTimes[i])
                    ypeak.append(yMagnitudes[i])
                    indexesPeak.append(i)
                    print('Peak {} is at ({},{})'.format(count, xTimes[i], yMagnitudes[i]))
        writeFile.writerow(['Impedance Peaks' + str(cellCount) + ':']+ ypeak)
        writeFile.writerow(['Height' + str(cellCount) + ':']+magHeight)
    elif max(magHeight) < max(absmagHeight1):
        #count = 0
        for i in indexesMagD:
            if xTimes[i] != 0:
                if (yMagnitudes[i - 1] > yMagnitudes[i] and yMagnitudes[i] < yMagnitudes[i + 1]):
                    count = count + 1
                    plt.plot(xTimes[i],yMagnitudes[i],'ro')
                    plt.annotate(count, (xTimes[i], yMagnitudes[i]), color='black', va='top')
                    xdeep.append(xTimes[i])
                    ydeep.append(yMagnitudes[i])
                    indexesDeep.append(i)
                    print('Deep {} is at ({},{})'.format(count, xTimes[i], yMagnitudes[i]))
        writeFile.writerow(['Impedance Deeps' + str(cellCount) + ':']+ydeep)
        writeFile.writerow(['Height' + str(cellCount) + ':']+ magHeight1)
    plt.xlabel('Time')
    plt.ylabel('Magnitude ' +  str(cellCount))
    print('-----------------------Impedance Phase Section-------------------------')  # Impedance Phase Section
    plotPos = plotPos + 1
    plt.subplot(rowPlot, colPlot, plotPos)
    plt.plot(xTimes, yPhases)

    count=0
    if max(phaHeight) > max(absphaHeight1):
        for i in indexesPhaP:
            if xTimes[i] !=0:
                if (yPhases[i - 1] < yPhases[i] and yPhases[i] > yPhases[i + 1]):
                    count=count+1
                    plt.plot(xTimes[i], yPhases[i], 'yo')
                    plt.annotate(count, (xTimes[i], yPhases[i]), color='black', va='top')
                    xpeakP.append(xTimes[i])
                    ypeakP.append(yPhases[i])
                    indexesPeakP.append(i)
                    print('Peak {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
        writeFile.writerow(['Phase Peaks'+str(cellCount)+':']+ypeakP)
        writeFile.writerow(['Height'+str(cellCount)+':']+phaHeight)
    elif max(phaHeight) <= max(absphaHeight1):
        count=0
        for i in indexesPhaD:
            if xTimes[i] !=0:
                if (yPhases[i - 1] > yPhases[i] and yPhases[i] < yPhases[i + 1]):
                    count=count+1
                    plt.plot(xTimes[i], yPhases[i], 'ro')
                    plt.annotate(count, (xTimes[i], yPhases[i]), color='black', va='top')
                    xdeepP.append(xTimes[i])
                    ydeepP.append(yPhases[i])
                    indexesDeepP.append(i)
                    print('Deep {} is at ({},{})'.format(count, xTimes[i], yPhases[i]))
        writeFile.writerow(['Phase Deeps'+str(cellCount)+':']+ydeepP)
        writeFile.writerow(['Height' + str(cellCount) + ':']+phaHeight1)
    print('==================================================================')  # End of Section
    plt.xlabel('Time')
    plt.ylabel('Phase '+ str(cellCount))
def main():
    #Auto
    #directory=path+fileName="C:/Users/Hal/Desktop/For HAL/Run34/69696_231_Run34_21_41_36_Demod1.csv"
    #path=input("Please input the file path:")
    # while os.path.exists(path)!=True:
    #     path=input('Incorrect Path, please input the path again.\n')
    path = "C:/Users/Hal/Desktop/run 4/"
    global listsxTimes, listsMag, listsPha, xlistsMagPeak, ylistsMagPeak, xlistsMagDeep, ylistsMagDeep, xlistsPhaPeak, ylistsPhaPeak, xlistsPhaDeep, ylistsPhaDeep
    print("===============================================")
    print("1: Analyze only one excel file")
    print("2. Define baseline and find peaks for all excel files that is contained in a folder")
    print("3. Select one of the baseline and used it start and end point for finding peaks for the other graph")
    print("4. Print both peaks and deeps")
    print("5. Same as 4, but it allows the user to select one of the graph, and enlarge it")
    print("6. Subtract one graph to the other")
    fileNameorNot=input("Open a single csv file(y/n)? ")
    if fileNameorNot=='yes' or fileNameorNot=='Yes' or fileNameorNot=='Y' or fileNameorNot=='YES' or fileNameorNot=='y':
        # fileName=input("Please input the file name(.csv at the end): ")
        # while os.path.isfile(path + fileName) != True:
        #     print('File is not found!')
        #     fileName=input("Please input the file name(.csv at the end): ")
        fileName='69696_231_Run23_20_58_13_Demod1.csv'
        singleCSVFile=path+fileName
        getData(singleCSVFile)
        plt.figure(1)
        totalRowPlot=2
        totalColPlot=2
        totalPlotPos=1
        cellCounter=1
        outFile = open('testing.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        autoMain(cellCounter,totalRowPlot,totalColPlot,totalPlotPos,writeFile)
        outFile.close()
        plt.show()
        modifyorNot=input("Not satisfied with the current result, modify the result?")
        # if modifyorNot=='yes' or modifyorNot=='Yes'or modifyorNot=='YES'or modifyorNot=='Y'or modifyorNot=='y':

    elif fileNameorNot=='no' or fileNameorNot=='No' or fileNameorNot=='N' or fileNameorNot=='NO' or fileNameorNot=='n':
        files = glob.glob(path + "*.csv")
        cellCounter=0
        totalRowPlot=0
        plt.figure(1)

        for fileDirectory in files:
            totalRowPlot=totalRowPlot+1
        totalColPlot = 2
        totalPlotPos = 1
        outFile = open('testing.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter=cellCounter+1
            getData(fileDirectory)
            autoMain(cellCounter,totalRowPlot,totalColPlot,totalPlotPos,writeFile)
            totalPlotPos = totalPlotPos + 2
        outFile.close()
        plt.show()
    elif fileNameorNot=='3':
        print("Proceeding to the User Interface.")
        files = glob.glob(path + "*.csv")
        cellCounter = 0
        totalRowPlot = 0
        plt.figure(1)
        plt.suptitle('Cell Analysis')
        for fileDirectory in files:
            totalRowPlot=totalRowPlot+1
        totalColPlot = 2
        totalPlotPos = 1
        outFile = open('testing2.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter = cellCounter + 1
            getData(fileDirectory)
            if cellCounter==1:
                autoMain2(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
            elif cellCounter>1:
                autoMain3(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
        outFile.close()
        plt.show()
    elif fileNameorNot=='4':
        print("Proceeding to the User Interface.")
        files = glob.glob(path + "*.csv")
        cellCounter = 0
        totalRowPlot = 0
        plt.figure(1)
        plt.suptitle('Cell Analysis')
        for fileDirectory in files:
            totalRowPlot = totalRowPlot + 1
        totalColPlot = 2
        totalPlotPos = 1
        outFile = open('testing2.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter = cellCounter + 1
            getData(fileDirectory)
            if cellCounter == 1:
                autoMain2(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
            elif cellCounter > 1:
                autoMain4(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
        outFile.close()
        figSize=plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.show()
    elif fileNameorNot=='5':
        print("Proceeding to the User Interface.")
        files = glob.glob(path + "*.csv")
        cellCounter = 0
        totalRowPlot = 0
        plt.figure(1)
        plt.suptitle('Cell Analysis')
        global listsxTimes,listsMag,listsPha,xlistsMagPeak,ylistsMagPeak,xlistsMagDeep,ylistsMagDeep,xlistsPhaPeak,ylistsPhaPeak,xlistsPhaDeep,ylistsPhaDeep
        listsxTimes=[]
        listsMag=[]
        listsPha=[]
        xlistsMagPeak=[]
        ylistsMagPeak=[]
        xlistsMagDeep=[]
        ylistsMagDeep=[]
        xlistsPhaPeak=[]
        ylistsPhaPeak=[]
        xlistsPhaDeep=[]
        ylistsPhaDeep=[]
        listsindexesPeak=[]
        listsindexesDeep=[]
        listsindexesPeakP=[]
        listsindexesDeepP=[]
        for fileDirectory in files:
            totalRowPlot = totalRowPlot + 1
        totalColPlot = 2
        totalPlotPos = 1
        outFile = open('testing2.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter = cellCounter + 1
            getData(fileDirectory)
            if cellCounter == 1:
                autoMain2(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
            elif cellCounter > 1:
                autoMain5(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
                listsxTimes.append(xTimes)
                listsMag.append(yMagnitudes)
                listsPha.append(yPhases)
                xlistsMagPeak.append(xpeak)
                ylistsMagPeak.append(ypeak)
                xlistsMagDeep.append(xdeep)
                ylistsMagDeep.append(ydeep)
                xlistsPhaPeak.append(xpeakP)
                ylistsPhaPeak.append(ypeakP)
                xlistsPhaDeep.append(xdeepP)
                ylistsPhaDeep.append(ydeepP)
                listsindexesPeak.append(indexesPeak)
                listsindexesDeep.append(indexesDeep)
                listsindexesPeakP.append(indexesPeakP)
                listsindexesDeepP.append(indexesDeepP)
        outFile.close()
        figSize=plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.draw()
        plt.pause(0.001)
        selectGraph=input("Which file you want to open?")
        plt.figure(2)
        plt.plot(listsxTimes[int(selectGraph)-2],listsMag[int(selectGraph)-2])
        plt.plot(xlistsMagPeak[int(selectGraph)-2],ylistsMagPeak[int(selectGraph)-2],'ro')
        plt.plot(xlistsMagDeep[int(selectGraph)-2],ylistsMagDeep[int(selectGraph)-2],'o',color='orange')
        temp=0
        temp2=0
        temp3=0
        for i in range(len(startPointsPha)):
            count=0 #each time the j move to the new domain, it resets the count to 0
            for j in range(startPointsPha[i],endPointsPha[i]):
                if j in listsindexesPeak[int(selectGraph)-2] or j in listsindexesDeep[int(selectGraph)-2]:
                    count=count+1
                    if count==1:
                        temp=j
                    elif count!=0 and count%2==0:
                        temp2=j
                        #temp3=(listsMag[int(selectGraph)-2][temp]+listsMag[int(selectGraph)-2][temp2])/2
                        count1 = 0
                        for l in range(temp, temp2):
                            if listsMag[int(selectGraph)-2][l-1]>=listsMag[int(selectGraph)-2][startPointsPha[i]-175]>listsMag[int(selectGraph)-2][l+1]:
                                count1=count1+1
                                if count1==1:
                                    count1=count1+1
                                    plt.plot(listsxTimes[int(selectGraph)-2][l],listsMag[int(selectGraph)-2][l],'yo')

        plt.show()
    elif fileNameorNot=='6':
        print("Proceeding to the User Interface.")
        files = glob.glob(path + "*.csv")
        cellCounter = 0
        totalRowPlot = 0
        plt.figure(1)
        plt.suptitle('Cell Analysis')
        listsxTimes = []
        listsMag = []
        listsPha = []
        xlistsMagPeak = []
        ylistsMagPeak = []
        xlistsMagDeep = []
        ylistsMagDeep = []
        xlistsPhaPeak = []
        ylistsPhaPeak = []
        xlistsPhaDeep = []
        ylistsPhaDeep = []
        listsindexesPeak = []
        listsindexesDeep = []
        listsindexesPeakP = []
        listsindexesDeepP = []
        for fileDirectory in files:
            totalRowPlot = totalRowPlot + 1
        totalColPlot = 2
        totalPlotPos = 1
        outFile = open('testing2.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter = cellCounter + 1
            getData(fileDirectory)
            if cellCounter == 1:
                autoMain2(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
                listsxTimes.append(xTimes)
                listsMag.append(yMagnitudes)
                listsPha.append(yPhases)
            elif cellCounter > 1:
                autoMain5(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
                totalPlotPos = totalPlotPos + 2
                listsxTimes.append(xTimes)
                listsMag.append(yMagnitudes)
                listsPha.append(yPhases)
                xlistsMagPeak.append(xpeak)
                ylistsMagPeak.append(ypeak)
                xlistsMagDeep.append(xdeep)
                ylistsMagDeep.append(ydeep)
                xlistsPhaPeak.append(xpeakP)
                ylistsPhaPeak.append(ypeakP)
                xlistsPhaDeep.append(xdeepP)
                ylistsPhaDeep.append(ydeepP)
                listsindexesPeak.append(indexesPeak)
                listsindexesDeep.append(indexesDeep)
                listsindexesPeakP.append(indexesPeakP)
                listsindexesDeepP.append(indexesDeepP)
        outFile.close()
        figSize = plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        newYss=[]
        newYss1=[]
        newYss2=[]
        newYss3=[]
        newYss4=[]
        newYss5=[]
        for i in range(len(listsMag[0])):
            newYss.append(listsMag[4][i]-listsMag[0][i])
            newYss1.append(listsMag[5][i]-listsMag[1][i])
            newYss2.append(listsMag[6][i]-listsMag[2][i])
            newYss3.append(listsPha[5][i]-listsPha[1][i])
            newYss4.append(listsPha[6][i]-listsPha[2][i])
            newYss5.append(listsPha[7][i]-listsPha[3][i])
        plt.figure(2)
        plt.ylabel('Mag5-1')
        plt.plot(listsxTimes[2],newYss)
        plt.figure(3)
        plt.ylabel('Mag6-2')
        plt.plot(listsxTimes[2], newYss1)
        plt.figure(4)
        plt.ylabel('Mag7-3')
        plt.plot(listsxTimes[2], newYss2)
        plt.figure(5)
        plt.ylabel('Pha6-2')
        plt.plot(listsxTimes[2], newYss3)
        plt.figure(6)
        plt.ylabel('Pha7-3')
        plt.plot(listsxTimes[2], newYss4)
        plt.figure(7)
        plt.ylabel('Pha8-4')
        plt.plot(listsxTimes[2], newYss5)
        plt.show()
    else:#ultimate Main
        # For example: directory=path+fileName="C:/Users/Hal/Desktop/For HAL/Run34/69696_231_Run34_21_41_36_Demod1.csv"
        # path=input("Please input the file path:")
        # while os.path.exists(path)!=True:
        #     path=input('Incorrect Path, please input the path again.\n')
        path = "C:/Users/Hal/Desktop/run 4/"
        files = glob.glob(path + "*.csv")
        #Variables
        listsxTimes = []
        listsMag = []
        listsPha = []
        listsIndexStartPointMag=[]
        listsIndexEndPointMag=[]
        listsIndexStartPointPha=[]
        listsIndexEndPointPha=[]
        listsindexesPeak=[]
        listsindexesDeep=[]
        listsindexesPeakP=[]
        listsindexesDeepP=[]




        #Obtain figure 1, xTimes, yMags, yPhases, indexes of start and end points
        cellCounter = 0
        totalRowPlot = 0
        plt.figure(1)
        plt.suptitle('Cell Analysis')
        for fileDirectory in files:
            totalRowPlot = totalRowPlot + 1
        totalColPlot = 2
        totalPlotPos = 1
        pathHolder = path.split("/")
        print(pathHolder)
        outFile = open('output' + pathHolder[4] + '.csv', 'w', newline='')
        writeFile = csv.writer(outFile)
        for fileDirectory in files:
            cellCounter = cellCounter + 1
            getData(fileDirectory)
            autoMain2(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile)
            totalPlotPos = totalPlotPos + 2
            listsxTimes.append(xTimes)
            listsMag.append(yMagnitudes)
            listsPha.append(yPhases)
            listsIndexStartPointMag.append(startPointsMag)
            listsIndexEndPointMag.append(endPointsMag)
            listsIndexStartPointPha.append(startPointsPha)
            listsIndexEndPointPha.append(endPointsPha)
        figSize = plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.draw()
        plt.pause(0.001)
        #Select a graph, use its startPoints and endPoints to determine peaks and deeps for all graphs
        print("Select the best graph, use it to determine the start and end points for the other graph, else exit the program")
        magorpha=input("First, select Magnitude graph, enter 1; or select Phase graph, enter 2: ")
        defineSE=input("Next, enter Magnitude or Phase number: ")

        if magorpha=='2':
            defineSE = int(defineSE)
            startPoints=list(listsIndexStartPointPha[defineSE-1])
            endPoints=list(listsIndexEndPointPha[defineSE-1])
        elif magorpha=='1':
            defineSE = int(defineSE)
            startPoints=list(listsIndexStartPointMag[defineSE-1])
            endPoints=list(listsIndexEndPointMag[defineSE-1])
        else:
            exit(0)


        #Figure 2
        cellCounter = 0
        totalRowPlot = 0
        plt.figure(2)
        plt.suptitle('Cell Analysis')
        for fileDirectory in files:
            totalRowPlot = totalRowPlot + 1
        totalColPlot = 2
        totalPlotPos = 1
        for fileDirectory in files:
            cellCounter = cellCounter + 1
            getData(fileDirectory)
            ultimateAutoMain(cellCounter, totalRowPlot, totalColPlot, totalPlotPos, writeFile, startPoints,endPoints)
            totalPlotPos = totalPlotPos + 2
            listsindexesPeak.append(indexesPeak)
            listsindexesDeep.append(indexesDeep)
            listsindexesPeakP.append(indexesPeakP)
            listsindexesDeepP.append(indexesDeepP)

        figSize = plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.draw()
        plt.pause(0.001)

        #Figure 3
        newxTimes=[]
        newYss=[]

        plt.figure(3)
        print('Select two graphs, the former ys will minus the later ys and form a new graph. Else, exit.')
        magorpha1=input("Select first graph, Magnitude graph, enter 1; or select Phase graph, enter 2: ")
        selectGraph1=input("Enter first Magnitude or Phase number: ")
        selectGraph2 = input("Enter second Magnitude or Phase number: ")
        if magorpha1=='1':
            selectGraph1 = int(selectGraph1)
            selectGraph2 = int(selectGraph2)
            newxTimes=list(listsxTimes[selectGraph1-1])
            for i in range(len(listsxTimes[selectGraph1-1])):
                newYss.append(listsMag[selectGraph1-1][i]-listsMag[selectGraph2-1][i])
        elif magorpha1=='2':
            selectGraph1 = int(selectGraph1)
            selectGraph2 = int(selectGraph2)
            newxTimes = list(listsxTimes[selectGraph1-1])
            for i in range(len(listsxTimes[selectGraph1 - 1])):
                newYss.append(listsPha[selectGraph1 - 1][i] - listsPha[selectGraph2 - 1][i])
        else:
            exit(0)

        plt.xlabel('Time')
        plt.ylabel(str(selectGraph1) + "-" + str(selectGraph2))
        plt.plot(newxTimes,newYss)

        #determine the start points and end points
        newStartPoints=[]
        newEndPoints=[]
        tempStartPgraph3 = []
        tempEndPgraph3 = []
        tempStartPgraph4 = []
        tempEndPgraph4 = []
        #the size of the selectGraph3 must be smaller than or equal to selectGraph4
        print('Select two graphs with the best start and end points. Else, exit.')
        magorpha2=input("Select Magnitude graph, enter 1; or select Phase graph, enter 2: ")
        selectGraph3=input("Enter first Magnitude or Phase number: ")
        selectGraph4 = input("Enter second Magnitude or Phase number: ")
        if magorpha2=='1':
            selectGraph3 = int(selectGraph3)
            selectGraph4 = int(selectGraph4)
            for i in range(len(listsIndexStartPointMag[selectGraph3-1])):  # this number should be changed manually each time
                if listsIndexStartPointMag[selectGraph3-1][i] > listsIndexStartPointMag[selectGraph4-1][i]:
                    newStartPoints.append(listsIndexStartPointMag[selectGraph4-1][i])
                else:
                    newStartPoints.append(listsIndexStartPointMag[selectGraph3-1][i])
            for i in range(len(listsIndexEndPointMag[selectGraph3-1])):  # this number should be changed manually each time
                if listsIndexEndPointMag[selectGraph3-1][i] < listsIndexEndPointMag[selectGraph4-1][i]:
                    newEndPoints.append(listsIndexEndPointMag[selectGraph4-1][i])
                else:
                    newEndPoints.append(listsIndexEndPointMag[selectGraph3-1][i])

            #checking the startpoint and end point, green and blue, orange and yellow
            tempStartPgraph3 = list(listsIndexStartPointMag[selectGraph3 - 1])
            tempEndPgraph3 = list(listsIndexEndPointMag[selectGraph3 - 1])
            tempStartPgraph4 = list(listsIndexStartPointMag[selectGraph4 - 1])
            tempEndPgraph4 = list(listsIndexEndPointMag[selectGraph4 - 1])
            count = 0
            for i in listsIndexStartPointMag[selectGraph3-1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='green')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
            count = 0
            for i in listsIndexEndPointMag[selectGraph3-1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='blue')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (xTimes[i], newYss[i]), color='black', va='top')
            count = 0
            for i in listsIndexStartPointMag[selectGraph4-1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='orange')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
            count = 0
            for i in listsIndexEndPointMag[selectGraph4-1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='yellow')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')

        elif magorpha2=='2':
            selectGraph3 = int(selectGraph3)
            selectGraph4 = int(selectGraph4)
            for i in range(len(listsIndexStartPointPha[selectGraph3-1])):  # this number should be changed manually each time
                if listsIndexStartPointPha[selectGraph3-1][i] > listsIndexStartPointPha[selectGraph4-1][i]:
                    newStartPoints.append(listsIndexStartPointPha[selectGraph4-1][i])
                else:
                    newStartPoints.append(listsIndexStartPointPha[selectGraph3-1][i])
            for i in range(len(listsIndexEndPointPha[selectGraph3-1])):  # this number should be changed manually each time
                if listsIndexEndPointPha[selectGraph3-1][i] < listsIndexEndPointPha[selectGraph4-1][i]:
                    newEndPoints.append(listsIndexEndPointPha[selectGraph4-1][i])
                else:
                    newEndPoints.append(listsIndexEndPointPha[selectGraph3-1][i])

            # checking the startpoint and end point, green and blue, orange and yellow
            tempStartPgraph3 = list(listsIndexStartPointPha[selectGraph3 - 1])
            tempEndPgraph3 = list(listsIndexEndPointPha[selectGraph3 - 1])
            tempStartPgraph4 = list(listsIndexStartPointPha[selectGraph4 - 1])
            tempEndPgraph4 = list(listsIndexEndPointPha[selectGraph4 - 1])
            count = 0
            for i in listsIndexStartPointPha[selectGraph3 - 1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='green')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
            count = 0
            for i in listsIndexEndPointPha[selectGraph3 - 1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='blue')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (xTimes[i], newYss[i]), color='black', va='top')
            count = 0
            for i in listsIndexStartPointPha[selectGraph4 - 1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='orange')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
            count = 0
            for i in listsIndexEndPointPha[selectGraph4 - 1]:
                count = count + 1
                plt.plot(newxTimes[i], newYss[i], 'o', color='yellow')
                # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
                plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
        else:
            exit(0)

        magHeightNY, indexesNewYssP = peakHeight(newYss, newStartPoints, newEndPoints)
        magHeightNY1, absNewYssHeight1, indexesNewYssD = deepHeight(newYss, newStartPoints, newEndPoints)

        for i in indexesNewYssP:
            plt.plot(newxTimes[i],newYss[i],'ro')
        for i in indexesNewYssD:
            plt.plot(newxTimes[i],newYss[i],'ro')

        figSize = plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.draw()
        plt.pause(0.001)

        #Figure 4 modify the graph
        plt.figure(4)
        for j in range(len(tempStartPgraph4)):
            for i in range(len(tempStartPgraph3)):
                if tempStartPgraph3[i]>tempStartPgraph4[i-1] and tempEndPgraph3[i]<tempEndPgraph4[i-1]:
                    del tempStartPgraph3[i]
                    del tempEndPgraph3[i]
                    break
                elif tempStartPgraph3[i] > tempEndPgraph4[i] and tempEndPgraph3[i] > tempEndPgraph4[i]:
                    del tempStartPgraph4[i]
                    del tempEndPgraph4[i]
                    break
                elif tempStartPgraph3[i] < tempStartPgraph4[i] and tempEndPgraph3[i] < tempStartPgraph4[i]:
                    del tempStartPgraph3[i]
                    del tempEndPgraph3[i]
                    break
        # figureC = 4
        # while True:
        #     userChoice = input("1.Add a start and end Point. 2.Remove a start and end point. 3. Keep the same.")
        #     userChoice1 = input("1.Orange and yellow pair. 2. Green and blue pair.")
        #     addremoveIndex = input("Which point you want to insert or remove?")
        #     if userChoice == '2':
        #        if userChoice1=='1':
        #            addremoveIndex=int(addremoveIndex)
        #            del tempStartPgraph4[addremoveIndex-1]
        #            del tempEndPgraph4[addremoveIndex-1]
        #        else:
        #            addremoveIndex = int(addremoveIndex)
        #            del tempStartPgraph3[addremoveIndex - 1]
        #            del tempEndPgraph3[addremoveIndex - 1]
        #     elif userChoice =='1':
        #         if userChoice1 == '1':
        #             addremoveIndex = int(addremoveIndex)
        #             tempStartPgraph4.insert(addremoveIndex-1,tempStartPgraph3[addremoveIndex-1])
        #             tempEndPgraph4.insert(addremoveIndex-1,tempEndPgraph3[addremoveIndex-1])
        #         else:
        #             addremoveIndex = int(addremoveIndex)
        #             tempStartPgraph3.insert(addremoveIndex - 1, tempStartPgraph4[addremoveIndex - 1])
        #             tempEndPgraph3.insert(addremoveIndex - 1, tempEndPgraph4[addremoveIndex - 1])
        #     else:
        #         print("DONE!")
        #         break

        newStartPoints=[]
        newEndPoints=[]
        for i in range(len(tempStartPgraph3)):  # this number should be changed manually each time
            if tempStartPgraph3[i] > tempStartPgraph4[i]:
                newStartPoints.append(tempStartPgraph4[i])
            else:
                newStartPoints.append(tempStartPgraph3[i])
        for i in range(len(tempEndPgraph3)):  # this number should be changed manually each time
            if tempEndPgraph3[i] < tempEndPgraph4[i]:
                newEndPoints.append(tempEndPgraph4[i])
            else:
                newEndPoints.append(tempEndPgraph3[i])

        magHeightNY, indexesNewYssP = peakHeight(newYss, newStartPoints, newEndPoints)
        magHeightNY1, absNewYssHeight1, indexesNewYssD = deepHeight(newYss, newStartPoints, newEndPoints)

        plt.xlabel('Time')
        plt.ylabel('MODIFIED'+ str(selectGraph1) + "-" + str(selectGraph2))
        plt.plot(newxTimes, newYss)

        for i in indexesNewYssP:
            plt.plot(newxTimes[i], newYss[i], 'ro')
        for i in indexesNewYssD:
            plt.plot(newxTimes[i], newYss[i], 'ro')

        count = 0
        for i in tempStartPgraph3:
            count = count + 1
            plt.plot(newxTimes[i], newYss[i], 'o', color='green')
            # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
            plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
        count = 0
        for i in tempEndPgraph3:
            count = count + 1
            plt.plot(newxTimes[i], newYss[i], 'o', color='blue')
            # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
            plt.annotate(count, (xTimes[i], newYss[i]), color='black', va='top')
        count = 0
        for i in tempStartPgraph4:
            count = count + 1
            plt.plot(newxTimes[i], newYss[i], 'o', color='orange')
            # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
            plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
        count = 0
        for i in tempEndPgraph4:
            count = count + 1
            plt.plot(newxTimes[i], newYss[i], 'o', color='yellow')
            # plt.plot(xTimes[i],yPhases[i],'o',color='orange')
            plt.annotate(count, (newxTimes[i], newYss[i]), color='black', va='top')
        figSize = plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.draw()
        plt.pause(0.001)
        print(len(newStartPoints))
        print(len(newEndPoints))

        #Figure 5
        indexMidpoint=[]
        t1=[]
        t2=[]
        ttotal=[]
        plt.figure(5)
        plt.plot(newxTimes, newYss)
        for i in indexesNewYssP:
            plt.plot(newxTimes[i], newYss[i], 'ro')
        for i in indexesNewYssD:
            plt.plot(newxTimes[i], newYss[i], 'ro')
        temp = 0
        temp2 = 0
        for i in range(len(newStartPoints)):
            count = 0  # each time the j move to the new domain, it resets the count to 0
            for j in range(newStartPoints[i], newEndPoints[i]):
                if j in indexesNewYssP or j in indexesNewYssD:
                    count = count + 1
                    if count == 1:
                        temp = j
                    elif count != 0 and count % 2 == 0:
                        temp2 = j
                        count1 = 0
                        klist=[] #reset the list
                        for k in range(temp, temp2):
                            klist.append(newYss[k])
                        for l in range(temp, temp2):
                            minHolder=min(klist,key=lambda x:abs(x-newYss[newStartPoints[i]]))#find the point that is closes to the startpoint
                            if newYss[l]==minHolder:
                                count1 = count1 + 1
                                if count1 == 1:
                                    count1 = count1 + 1
                                    plt.plot(newxTimes[l], newYss[l], 'o', color='yellow')
                                    indexMidpoint.append(l)
                                    ttotal.append(newxTimes[newEndPoints[i]] - newxTimes[newStartPoints[i]])
                                    t2.append(newxTimes[newEndPoints[i]]-newxTimes[l])
                                    t1.append(newxTimes[l]-newxTimes[newStartPoints[i]])
                            # if newYss[l - 1] > newYss[newStartPoints[i]] >newYss[l + 1] or newYss[l]==newYss[newStartPoints[i]]:
                            #     count1 = count1 + 1
                            #     if count1 == 1:
                            #         count1 = count1 + 1
                            #         plt.plot(newxTimes[l], newYss[l],'o',color='yellow')
                            #         indexMidpoint.append(l)
                            #         .ttotal.append(newxTimes(newEndPoints[i])-newxTimes(newStartPointsPoints[i]))
                            #         .t1.append(newxTimes(newEndPoints[i])-newxTimes(newStartPointsPoints[i]))
                            #         .t2.append(newxTimes(newEndPoints[i])-newxTimes(newStartPointsPoints[i]))
                            # elif newYss[l - 1] < newYss[newStartPoints[i]] <newYss[l + 1]or newYss[l]==newYss[newStartPoints[i]]:
                            #     count1 = count1 + 1
                            #     if count1 == 1:
                            #         count1 = count1 + 1
                            #         plt.plot(newxTimes[l], newYss[l],'o',color='yellow')
                            #         indexMidpoint.append(l)
        print("------------------------Midpoint Section-------------------------")
        midPointC=0
        for i in indexMidpoint:
            midPointC=midPointC+1
            print('Midpoint {} is at ({},{})'.format(midPointC, newxTimes[i], newYss[i]))

        writeFile.writerow(['t1:'] + t1)
        writeFile.writerow(['t2:'] + t2)
        writeFile.writerow(['ttotal:'] + ttotal)

        plt.xlabel('Time')
        plt.ylabel('MIDPOINT ' + str(selectGraph1) + "-" + str(selectGraph2))

        outFile.close()
        figSize = plt.get_current_fig_manager()
        figSize.window.state('zoomed')
        plt.show()

if __name__ == '__main__':
    main()