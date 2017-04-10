import numpy as np
import matplotlib.pyplot as plt
from Bass import *

# Outputs of BASS tracking program: Phase angle measurements, Beginning of
# C/A Code, and Fine time resolution measurements.

fs = 1023*4*10**3
Ts = 1/fs

#  Generate complex sinusoid (for initial testing, then will move
# on to simulated GPS data, and finally the real data.)
sampleLength = 0.002
t = np.linspace(0,sampleLength,int(sampleLength/Ts),endpoint=True)

# This currently doesn't work for larger frequency values.
# In order to work, freq << FreqResolutionCell

freq = 250 #Hz

expArg = 1j*2*np.pi*freq*t
complexSinusoid = np.exp(expArg)

N = len(complexSinusoid)
print("")
print("Frequency Resolution Cell: %f" %(FreqResolutionCell(N,Ts)))
print("Fine Frequency Estimation: %f" %(FineFrequencyEstimation(complexSinusoid,Ts,10)))
#print("Starting Phase Angle: %f" %(StartingPhaseAngle(complexSinusoid,Ts)))

# calculate k from freq and sampleLength
binSize = freq/sampleLength
k = freq/binSize 

# Still needs a bit of work for consistent results.
print("Fine Frequency Estimation - Single k (where k = %f): %f" %(k,FineFrequencyEstimationSingleK(complexSinusoid[0:255],complexSinusoid[256:512],Ts,k)))
