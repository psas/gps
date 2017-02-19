
#Store the shift registers as a deque, so that deque.rotate{} can be used.
from collections import deque  

class GoldCode:
    '''
    GPS Gold Code generator. Initialized with the feedback taps for one satellite.
    '''
    
    #Feedback taps as defined in GPS spec
    g1tap = [2,9]
    g2tap = [1,2,5,7,8,9]

    
    def __init__(self, taps):
        
        self.reset()
        self.tap = taps
        
        # Current index of the last returned code
        self.index = 0
        
    # Shift SRs
    def _shift(self):
        #Shift g1
        self.g1[9] = sum([self.g1[i] for i in self.g1tap]) % 2 
        self.g1.rotate()

        #Shift g2
        self.g2[9] = sum([self.g2[i] for i in self.g2tap]) % 2 
        self.g2.rotate()
        
        self.index = (self.index % 1023) + 1
        
    def reset(self):
        # Inititialize SRs as all 1's
        self.g1 = deque(1 for i in range(10))
        self.g2 = deque(1 for i in range(10))
        self.index = 0

    def getCode(self, num, zero = False, samplesPerChip = 1):
        #Returns a list of bits that form the Gold Code PRN of the designated satellite
        #zero flag determines whether 0 or -1 is returned
        
        g = []

        for i in range(num):
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
            CACodeSampled = np.repeat(CACode, samplesPerChip)
        return g

    def getSegment(self, first, last, zero = False, samplesPerChip = 1):
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
            CACodeSampled = np.repeat(CACode, samplesPerChip)
        return g

