#!/usr/bin/env python3

'''
This reads the data that have been exported by Tracking.py.

USAGE:
        ./ReadEphem.py InputBinaryFile

EXAMPLE USAGE:
        python3 ReadEphem.py SV1.bin
'''

import argparse
import numpy as np
import time
import matplotlib.pyplot as plt
from FindInList import *
import pdb

np.set_printoptions(threshold=np.inf)

parser = argparse.ArgumentParser(
        description='Reads ephemeris data from Tracking data bit dump.',
        usage='./ReadEphem.py InputBinaryFile'
        )
parser.add_argument('DataFile')
args = parser.parse_args()

# Create class to store subframes:
class SubFrame:
    def __init__(self):
        self.LastD29 = None # Second-to-last bit from last frame (value 0 or 1 initially)
        self.LastD30 = None # Second-to-last bit from last frame (value 0 or 1 initially)
        self.FrameData = None # 300 bytes long (each byte is one bit value)
        self.FrameNumber = None # Will be a value 1-5
        self.ParityD25toD30 = None # Current parity bits

TrackingData = np.fromfile(args.DataFile, dtype=np.int8, count=-1,sep='')

PreambleRegular  = np.array([1,0,0,0,1,0,1,1]) #.decode()
PreambleInverted = np.array([0,1,1,1,0,1,0,0]) #.decode()

# Find occurences of preamble pattern and store indexes in array
matches = FindListInList(TrackingData, PreambleInverted)

#### Will need to search for both the regular, as well as inverted preamble. For
# now, just using the inverted, since manually confirmed this was the one in the data.

# Assume each index value is a preamble, which means that every 300 samples,
# there will be another preamble. If the first index is 15, then the next actual
# preamble would be 315. So subtract 15 from all of the indexes, and take
# the modulus of 300 of each index value. If the result is zero, than that index
# is a multiple of 300 in reference to that index. The indexes with the largest
# amount of zeros will be assumed to be the indexes that are actual preambles.
# Once that index is determined, will store all indexes that resulted in zeros
# as the indexes for the preambles.
ZeroCount = []
for indexOfFirstPreamble in range(0,len(matches)):
    multOfThreeHundred = []
    for (ind,val) in enumerate(matches):
        multOfThreeHundred.append(((val-matches[indexOfFirstPreamble]) % 300))
    ZeroCount.append(multOfThreeHundred.count(0))

FirstPreamble = np.argmax(np.array(ZeroCount))
multOfThreeHundred = []
preambleIndexList = []
for (ind,val) in enumerate(matches):
    multOfThreeHundred.append(((val-matches[FirstPreamble]) % 300))
    if multOfThreeHundred[len(multOfThreeHundred)-1] == 0:
        preambleIndexList.append(val) #ind

# Print indexes of preambles.
print(preambleIndexList)
print("Total preambles found: %d" %len(preambleIndexList))

#c1

# Now that the preambles are found, load class with subframe information
SubFrameList = []
for (ind,val) in enumerate(preambleIndexList):
    if (len(TrackingData) - 300) < val:
        print("Subframe associated with last preamble not complete, so discarding.")
        break # Current subframe not complete, so break.
        # Will need to do another check to make sure val > 1
    curSubFrame = SubFrame()
    curSubFrame.LastD29 = TrackingData[val-2]
    curSubFrame.LastD30 = TrackingData[val-1]
    curSubFrame.FrameData = TrackingData[val:val+301]
    SubFrameList.append(curSubFrame)

# Convert data bits 1-24 so that multiplication can replace modulo-2 addition
for indFrame in range(len(SubFrameList)):
    #print ("Frame %d of %d" %(indFrame+1,len(SubFrameList)))
    for indBit in range(24): # change bits 1-24
        if SubFrameList[indFrame].FrameData[indBit] == 1:
            SubFrameList[indFrame].FrameData[indBit] = -1
        elif SubFrameList[indFrame].FrameData[indBit] == 0:
            SubFrameList[indFrame].FrameData[indBit] = 1
        else:
            print("Data bit found that was not 0 or 1!!!")


### Generate parity matrix
# First 5 rows, same vector but rotated
hRow = [1,1,1,0,1,1,0,0,0,1,1,1,1,1,0,0,1,1,0,1,0,0,1,0]
# Last row is different
hRowLast = [0,0,1,0,1,1,0,1,1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,1]
# Create matrix
H = np.array([hRow, np.roll(hRow,1), np.roll(hRow,2), np.roll(hRow,3), np.roll(hRow,4), hRowLast])

#pdb.set_trace() # Spawn python shell
