# from __future__ import print_function
# import sys
# import os
# import csv
# import matplotlib.pyplot as plt
# import numpy as np
# import pdb #for debug
#
# #access to the file, and retrive the data
# '''
# formatedLines=[]
# inFile=open('input.csv')
# for lines in inFile:
#     formatedLine=lines.strip().split(',')
#     formatedLines.append(formatedLine)
# #formatedLine.remove(formatedLine[0])
# formatedLines.remove(formatedLines[0])
# print(formatedLines[1])
# '''
# with open('C:/Users/Hal/Desktop/VMEC 2018/For HAL/Run23/69696_231_Run23_20_58_13_Demod3.csv') as csvfile:
#     readCSV=csv.reader(csvfile,delimiter=',')
#     data = [row for row in readCSV]  # stores the data to data, row by row, strings
#     xTime = data[0]
#     yMagnitude = data[5]
#     yPhase = data[6]
#     xTime1st = float(xTime[0]) / (210 * 10 ** 6)  # this is used for time conversion
#     xTimes = []
#     yMagnitudes = []
#     yPhases = []
#     for i in xTime:
#         xTimes.append(float(i) / (210 * 10 ** 6) - xTime1st)  # make the first time element as 0, and convert it to actual time
#     for i in yMagnitude:
#         yMagnitudes.append(float(i))
#     for i in yPhase:
#         yPhases.append(float(i))
#     pointsTimeMag = np.column_stack((xTimes, yMagnitudes))  # tuple for Magnitude over Time
#     pointsTimePha = np.column_stack((xTimes, yPhases))  # tuple for Phase over Time
#     plt.plot(xTimes, yMagnitudes)
#     for i in range(len(yMagnitudes)-1):
#             if(yMagnitudes[i-1]>yMagnitudes[i] and yMagnitudes[i]<yMagnitudes[i+1]):
#                 print('Peak is at (',xTimes[i],yMagnitudes[i],')')
#                 plt.plot(xTimes[i],yMagnitudes[i],'ro')#plot the peaks
#     plt.show()#show plot
import numpy as np
from matplotlib import pyplot as plt

def main():
    plt.axis([-50,50,0,10000])
    plt.ion()
    plt.show()

    x = np.arange(-50, 51)
    for pow in range(1,5):   # plot x^1, x^2, ..., x^4
        y = [Xi**pow for Xi in x]
        plt.plot(x, y)
        plt.draw()
        plt.pause(0.001)
        input("Press [enter] to continue.")

if __name__ == '__main__':
    main(

        figSize=plt.get_current_fig_manager()
    figSize.window.state('zoomed')
    plt.draw()
    plt.pause(0.001)

    # Figure 4 and 5 modify
    tempStartP = []
    tempEndP = []
    userChoice = input("1.Modify the graph, 2. Satisfy with the current result.")
    if userChoice == '1':
        else:
