VMEC Cell Data Analysis program is designed to shorten the time for researchers on collecting peaks, dips, and height of impedance. 

First, this program will retrieve the data from the folder.
Between, it will ask the user to select a graph and enlarge it for a better view (User has the option to choose No).
Second, it will ask the user to select the best baseline and uses it for all other graphs.
Third, it will ask the user to selects two graphs, the first graph's y values will minus the second graph's y values to form a new graph and displays the mid points.  NOTE: the first graph's list size should be smaller than the second graph's list size.

Dependencies:
from __future__ import print_function
import sys
import os
import csv
import glob
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.figure as fig
import pdb #for debug
NOTE: make sure to download these packages before running the program.
File->settings->Project:Name->click the green button '+'-> search package name->ok

Functions: 
getData(csvDirectory): takes a argument of directory of the input files
maxValue(aList): find the max value of a list
minValue(aList): find the min value of a list
mostFreNum(aList): find the most common value of a list
autoLevelLine(aList): use the common value of a list to define the baseline
findPeaks(ys,yzero): find peaks from a y values and the baseline
printPeaks(minPeakHeight,aList,ys,yzero): get rid of any peaks that are below a certain percentage of the max height
findDeeps(ys,yzero): find dips from a y values and the baseline
printDeeps(minPeakHeight,aList,ys,yzero): get rid of any dips that are below a certain percentage of the max height
sefindPeaks(ys,yzero,minPeakHeight): find the start and end point
peakHeight(ys,startList,endList): find the index and height of a list
sefindDeeps(ys,yzero,minDeepHeight): find the start and end point
deepHeight(ys,startList,endList): find the index and height of a list
autoMain2(cellCount, rowPlot,colPlot,plotPos,writeFile):
use to display the graph and write the peaks, dips, and baseline value to the output file
ultimateAutoMain(cellCount,rowPlot,colPlot,writeFile,startPoints, endPoints): display the graph and write the height values to the output file.