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

np.set_printoptions(threshold=np.inf)

parser = argparse.ArgumentParser(
        description='Reads ephemeris data from Tracking data bit dump.',
        usage='./ReadEphem.py InputBinaryFile'
        )
parser.add_argument('DataFile')
args = parser.parse_args()

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
        preambleIndexList.append(ind)

# Print indexes of preambles.
print(preambleIndexList)
print("Total preambles found: %d" %len(preambleIndexList))
