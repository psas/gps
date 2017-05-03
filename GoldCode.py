
#Store the shift registers as a deque, so that deque.rotate{} can be used.
from collections import deque  
import numpy as np

'''
GPS Gold Code generator. Initialized with the feedback taps for one satellite.
'''

#Feedback taps as defined in GPS spec
g1tap = [2,9]
g2tap = [1,2,5,7,8,9]

sats = [(1, 5), (2, 6), (3, 7), (4, 8), (0, 8), (1, 9), (0, 7), (1, 8), (2, 9), (1, 2),
            (2, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 3), (1, 4), (2, 5), (3, 6),
            (4, 7), (5, 8), (0, 2), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (0, 5), (1, 6),
            (2, 7), (3, 8), (4, 9), (3, 9), (0, 6), (1, 7), (3, 9)]

def __init__(taps):
    
    self.reset()
    self.tap = taps
    
    # Current index of the last returned code
    self.index = 0
    
# Shift SRs
def _shift():
    #Shift g1
    self.g1[9] = sum([self.g1[i] for i in self.g1tap]) % 2 
    self.g1.rotate()

    #Shift g2
    self.g2[9] = sum([self.g2[i] for i in self.g2tap]) % 2 
    self.g2.rotate()
    
    self.index = (self.index % 1023) + 1
    
def reset():
    # Inititialize SRs as all 1's
    g1 = deque(1 for i in range(10))
    g2 = deque(1 for i in range(10))
    index = 0

def getCode(num, zero = False, samplesPerChip = 1, prn = 0):
    #Returns a list of bits that form the Gold Code PRN of the designated satellite
    #zero flag determines whether 0 or -1 is returned
    
    g1 = deque(1 for i in range(10))
    g2 = deque(1 for i in range(10))
    
    if prn == 0:
        prn = tap
    
    g = []

    for i in range(num):
        val = (g1[9] + g2[prn[0]] + g2[prn[1]]) % 2
        g.append(val)

        #Shift g1
        g1[9] = sum([g1[i] for i in g1tap]) % 2 
        g1.rotate()

        #Shift g2
        g2[9] = sum([g2[i] for i in g2tap]) % 2 
        g2.rotate()

    if(zero == False):
        #format GC to have -1 in place of 0
        for n,i in enumerate(g):
            if i==0:
                g[n]=-1
    
    if (samplesPerChip > 1 ):
        # Repeat each chip to match our ADC sample frequency
        gsamp = np.repeat(g, samplesPerChip)
        return gsamp
    return g
    
def getTrackingCode():
    pass


def getAcquisitionCode(sat, spc):
    return getCode(1023, samplesPerChip = spc, prn = sats[sat-1])

def getSegment(first, last, zero = False, samplesPerChip = 1):
    #Works like getCode(), but returns a specific segment of the Gold Code

    g = []
    
    diff = last - first
    
    self.reset()

    for i in range(first):
        val = (self.g1[9] + self.g2[self.tap[0]] + self.g2[self.tap[1]]) % 2
        self._shift()
    
    for i in range(diff + 1):
        val = (self.g1[9] + self.g2[self.tap[0]] + self.g2[self.tap[1]]) % 2
        g.append(val)
        self._shift()

    if(zero == False):
        #format GC to have -1 in place of 0
        for n,i in enumerate(g):
            if i==0:
                g[n]=-1
    

    if (samplesPerChip > 1 ):
        # Repeat each chip to match our ADC sample frequency
        gsamp = np.repeat(g, samplesPerChip)
        return gsamp
    return g

