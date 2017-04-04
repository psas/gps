from tracking import *
import numpy as np
np.set_printoptions(threshold=np.inf)


# CA Code settings:
satPRL = 13 # Satellite PRN
estimatedPhase = 1471# Estimated CA code phase from Acquisition
samplesPerChip = 4 # Samples per chip
chipDelay = 2 # Sample spacing between (Early or Late) and Prompt code

# Data settings:
millisecondBlockIndex = 0 # 0 = 1st ms block
fileName = 'resources/JGPS@04.559925043'
fs = 4.092*10**6
estimatedDoppler = 13 # Hz, from Acquisition



# Get Early, Prompt, Late C/A codes
codeE, codeP, codeL = GetCACodeEPL(satPRL, estimatedPhase, samplesPerChip, chipDelay)

# Get MS of data
IData, QData = GetMSOfData(millisecondBlockIndex, fileName, fs, estimatedDoppler)

# Mix the signals
ImixE, ImixP, ImixL, QmixE, QmixP, QmixL = MixSignals(codeE,codeP,codeL,IData,QData)

# Perform integration (sum)
intIE,intIP,intIL, intQE,intQP,intQL = SumSignals(ImixE, ImixP, ImixL, QmixE, QmixP, QmixL)

# Get discriminator
discriminator = ((intIE ** 2 + intQE ** 2) - (intIL ** 2 + intQL ** 2)) / ((intIE ** 2 + intQE ** 2) + (intIL ** 2 + intQL ** 2))

# Print results
PrintCodeTracking(intIE,intIP,intIL, intQE,intQP,intQL,discriminator)
