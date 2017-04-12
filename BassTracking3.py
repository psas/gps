import numpy as np
import matplotlib.pyplot as plt
from Bass import *
from GPSData import *
from GoldCode import *

# Outputs of BASS tracking program: Phase angle measurements, Beginning of
# C/A Code, and Fine time resolution measurements.

#  This file is a fork of BassTracking.py, with the intention of testing
# the functions in Bass.py with the simulated and the launch12 data.

fs = 4.092*10**6 # Sampling Frequency [Hz]
Ts = 1/fs
numberOfMilliseconds = 2
sampleLength = numberOfMilliseconds*10**(-3)
bytesToSkip = 0

data = IQData()

data.importFile('./resources/JGPS@-32.041913222', fs, sampleLength, bytesToSkip)
t = np.linspace(0,sampleLength,int(sampleLength/Ts),endpoint=True)

# This currently doesn't work for larger frequency values.
# In order to work, freq << FreqResolutionCell

N = len(data.CData)
print("")
print("Frequency Resolution Cell: %f" %(FreqResolutionCell(N,Ts)))

# Will choose satellite information from tracking in order to Generate
# in phase CA code and to despread the signal.
estFreq = 3300 # Hz
estPhase = 389 # Bins (will rotate left)

#Choose which satellite's C/A code is generated
Satellite = 4

# Create list of C/A code Taps, for simpler sat selection",
sat = [(1,5),(2,6),(3,7),(4,8),(0,8),(1,5),(0,7),(1,8),(2,9),(1,2),(2,3),(4,5),(5,6),(6,7),(7,8),(8,9),(0,3),(1,4),(2,5),(3,6),(4,7),(5,8),(0,2),(3,5),(4,6),(5,7),(6,8),(7,9),(0,5),(1,6),(2,7),(3,8),(4,9),(3,9),(0,6),(1,7),(3,9)]

# Create Code Generator object for chosen Satellite
CodeGen = GoldCode(sat[Satellite - 1]) # Index starts at zero

# Generate CA Code
CACode = CodeGen.getCode(1023)

# Reformat GC to have -1 in place of 0 (Now done in GoldCode)
#for n,i in enumerate(CACode):
#    if i==0:
#        CACode[n]=-1

# Repeat each chip 4 times (See markdown in above cell), to match our ADC sample frequency",
CACodeSampled = np.repeat(CACode,4)
print("Satellite chosen: %d, with tap: %s" %(Satellite,str(sat[Satellite - 1])))

# Repeat entire array for each ms of data sampled
CACodeSampled = np.tile(CACodeSampled,int(sampleLength*1000))
print(len(CACodeSampled))

# Rotate CA Code array so phase aligns with that of the signal.
CACodeSampledRotated = np.roll(CACodeSampled,-estPhase)

dataDespread = data.CData*CACodeSampledRotated

SpaceBetweenSamples = 10
ProvideFreqEstimate = True
print("Fine Frequency Estimation: %f" %(FineFrequencyEstimation(dataDespread,Ts,SpaceBetweenSamples,ProvideFreqEstimate,estFreq)))
#print("Starting Phase Angle: %f" %(StartingPhaseAngle(dataDespread,Ts)))

# calculate k from freq and sampleLength
binSize = fs/N
k = estFreq/binSize

# Still needs a bit of work for consistent results.
print("Fine Frequency Estimation - Single k (where k = %f): %f" %(k,FineFrequencyEstimationSingleK(dataDespread[0:255],dataDespread[256:512],Ts,k)))
