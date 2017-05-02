# This is based off of (essentially a Python port of) the tracking.m file included with SoftGNSS v3.0.
# The license that was included with that program is below:

#------------------------Original License----------------------------------
#                           SoftGNSS v3.0
#
# Copyright (C) Dennis M. Akos
# Written by Darius Plausinaitis and Dennis M. Akos
# Based on code by DMAkos Oct-1999
#--------------------------------------------------------------------------
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
#USA.
#--------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

from GoldCode import GoldCode
from GPSData import IQData

#np.set_printoptions(threshold=np.inf)

# Import data. Will read many ms at once, then process the blocks as needed.
# Need these to pass to importFile module
fs = 4.092*10**6 # Sampling Frequency [Hz]
numberOfMilliseconds = 4500
sampleLength = numberOfMilliseconds*10**(-3)
bytesToSkip = 0

data = IQData()
# Uncomment one of these lines to choose between Launch12 or gps-sdr-sim data

# /home/evan/Capstone/gps/resources/JGPS@-32.041913222
#data.importFile('resources/JGPS@04.559925043', fs, sampleLength, bytesToSkip)
#data.importFile('resources/JGPS@-32.041913222', fs, sampleLength, bytesToSkip)
#data.importFile('resources/test4092kHz.max', fs, sampleLength, bytesToSkip)
data.importFile('resources/Single4092KHz5s.max', fs, sampleLength, bytesToSkip)

def calcLoopCoef(LoopNoiseBandwidth, Zeta, LoopGain):
    # Solve for the natural frequency
    Wn = LoopNoiseBandwidth*8*Zeta / (4*Zeta**2 + 1)

    # Solve for tau1 and tau2
    tau1 = LoopGain / (Wn * Wn);
    tau2 = (2.0 * Zeta) / Wn;

    return (tau1, tau2)


class TrackingSettings:
    def __init__(self):
        self.msToProcess = 4400 # How many ms blocks to process per channel
        self.dllCorrelatorSpacing = 0.5 # How many chips to offset for E & L codes.
        self.codeLoopNoiseBandwidth = 2 # [Hz]
        self.codeZeta = 0.7
        self.codeLoopGain = 1.0
        self.carrLoopNoiseBandwidth = 25 # 25 [Hz]
        self.carrZeta = 0.7
        self.carrLoopGain = 0.25 # 0.25
        self.codeFreqBasis = 1.023*10**6 # L1 C/A Code frequency
        self.samplingFreq = 4.092*10**6 # Sampling frequency of ADC
        self.codeLength = 1023
        self.SamplesPerChip = int(self.samplingFreq/self.codeFreqBasis)

# Initialize a settings class
settings = TrackingSettings()

class TrackingResults:
    def __init__(self):
        self.status = False # True if tracking was successful, False otherwise.
        self.PRN = 0
        self.absoluteSample = np.zeros((settings.msToProcess)) # Sample that C/A code 1st starts.
        self.codeFreq = np.zeros((settings.msToProcess)) # C/A code frequency.
        self.carrFreq = np.zeros((settings.msToProcess)) # Frequency of tracked carrier.
        self.I_P  = np.zeros((settings.msToProcess)) # Correlator outputs (resulting sum).
        self.I_E  = np.zeros((settings.msToProcess)) # Correlator outputs (resulting sum).
        self.I_L  = np.zeros((settings.msToProcess)) # Correlator outputs (resulting sum).
        self.Q_P  = np.zeros((settings.msToProcess)) # Correlator outputs (resulting sum).
        self.Q_E  = np.zeros((settings.msToProcess)) # Correlator outputs (resulting sum).
        self.Q_L  = np.zeros((settings.msToProcess)) # Correlator outputs (resulting sum).
        self.dllDiscr = np.zeros((settings.msToProcess)) # Code-Loop discriminator
        self.dllDiscrFilt = np.zeros((settings.msToProcess)) # Code-Loop discriminator filter
        self.pllDiscr = np.zeros((settings.msToProcess)) # Carrier-Loop discriminator
        self.pllDiscrFilt = np.zeros((settings.msToProcess)) # Carrier-Loop discriminator filter

class TrackingChannel:
    def __init__(self):
        self.PRN = 0 # Value will be non-zero if Acquisition was successful for this channel
        self.CodePhase = None # Sample offset of beginning of CA code from acquisition
        self.acquiredFreq = None # Doppler freq from acquisition

# Determine how many code periods to process (same # as ms blocks to process)
codePeriods = settings.msToProcess

# Spacing for early and late CA code (In chips)
earlyLateSpacing = settings.dllCorrelatorSpacing

# How many seconds to perform the integration over (for CA code)
PDIcode = 0.001;

# Calculate filter coefficient values for code loop
tau1code, tau2code = calcLoopCoef(settings.codeLoopNoiseBandwidth, settings.codeZeta, settings.codeLoopGain)

# How many seconds to perform the integration over (for carrier)
PDIcarr = 0.001;

# Calculate filter coefficient values for carrier loop
tau1carr, tau2carr = calcLoopCoef(settings.carrLoopNoiseBandwidth, settings.carrZeta, settings.carrLoopGain)

# Initialize channel with data from acquisition
# Manually filling in these values from the simulated gps information (exact values) for now.
# Once working, will pass the values found from acquisition.
channel = TrackingChannel()
channel.PRN = 1
# For codePhase below, + 1 was added experimentally. This should be removed when code phase adjustment is working properly.
channel.codePhase = int((1023.0 - 630.251585)*4 + 1) # Value from generator
#channel.codePhase = int(655.25*4) # Value from generator

#channel.acquiredFreq = -3363.817361 # Value from generator
channel.acquiredFreq = -3340

# Process each channel (Will impliment loop in future. For now only processing one channel)
# Process channel if PRN is non-zero (Acquisition successful)
if channel.PRN:
    # Create instance of TrackingResults to store results into
    trackResults = TrackingResults()
    trackResults.PRN = channel.PRN

    # Create sampled CA Code:
    # Create list of C/A code Taps, for simpler sat selection",
    sat = [(1, 5), (2, 6), (3, 7), (4, 8), (0, 8), (1, 9), (0, 7), (1, 8), (2, 9), (1, 2),
           (2, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 3), (1, 4), (2, 5), (3, 6),
           (4, 7), (5, 8), (0, 2), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (0, 5), (1, 6),
           (2, 7), (3, 8), (4, 9), (3, 9), (0, 6), (1, 7), (3, 9)]

    codeGen = GoldCode(sat[channel.PRN - 1]) # Index starts at zero

    # Generate CA Code
    CACode = np.array(codeGen.getCode(1023, samplesPerChip=1))
    #print(CACode)
    CACode = np.append(CACode,CACode[0])
    CACode = np.insert(CACode,0, CACode[len(CACode) - 2])
    #print(CACode)
    # Perform additional initializations:
    codeFreq = settings.codeFreqBasis

    # Residual code phase (Chips)
    remCodePhase = 0.0

    # Carrier frequency from acquisition (doppler freq)
    carrFreq      = channel.acquiredFreq
    carrFreqBasis = channel.acquiredFreq

    # define residual carrier phase
    remCarrPhase  = 0.0

    # code tracking loop parameters
    oldCodeNco   = 0.0
    oldCodeError = 0.0

    # carrier/Costas loop parameters
    oldCarrNco   = 0.0
    oldCarrError = 0.0

    dataPosition = 0
    blksize = 0

    # Process the requested number of code periods (num of ms to process)
    for loopCount in range(0,codePeriods):
        print("------- Loop Count:   %d  --------"%loopCount)
        # Read current block of data
        # Find the size of a "block" or code period in whole samples

        # Update the phasestep based on code freq (variable) and
        # sampling frequency (fixed)
        codePhaseStep = np.real(codeFreq / settings.samplingFreq)

        #print("Old blksize: %d"%blksize)
        blksize = int(np.ceil((settings.codeLength-remCodePhase) / codePhaseStep))
        #print("New blksize: %d"%blksize)
        #print("Old remCodePhase: %f" %remCodePhase)

        # Read in the appropriate number of samples to process this
        # iteration
        rawSignal = data.IData[channel.codePhase + dataPosition: channel.codePhase + dataPosition + blksize]
        dataPosition = dataPosition + blksize

        # If did not read in enough samples, then could be out of
        # data - better exit
        #print(len(rawSignal))

        # Generate Early CA Code.
        tStart = remCodePhase - earlyLateSpacing
        tStep = codePhaseStep
        tEnd = ((blksize-1)*codePhaseStep+remCodePhase) + codePhaseStep - earlyLateSpacing
        tcode = np.linspace(tStart,tEnd,blksize,endpoint=False)
        tcode2 = (np.ceil(tcode)).astype(int)
        earlyCode = CACode[tcode2]
        #print(earlyCode)
        #print(tcode)
        #print(tcode2)
        #quit()

        # Generate Late CA Code.
        tStart = remCodePhase + earlyLateSpacing
        tStep = codePhaseStep
        tEnd = ((blksize-1)*codePhaseStep+remCodePhase) + codePhaseStep + earlyLateSpacing
        tcode = np.linspace(tStart,tEnd,blksize,endpoint=False)
        tcode2 = (np.ceil(tcode)).astype(int)
        lateCode = CACode[tcode2]
        #print(earlyCode)
        #print(tcode)
        #print(tcode2)
        #quit()

        # Generate Prompt CA Code.
        tStart = remCodePhase
        tStep = codePhaseStep
        tEnd = ((blksize-1)*codePhaseStep+remCodePhase) + codePhaseStep
        tcode = np.linspace(tStart,tEnd,blksize,endpoint=False)
        tcode2 = (np.ceil(tcode)).astype(int)
        promptCode = CACode[tcode2]
        #print(promptCode)
        #print(tcode)
        #print(tcode2)
        #quit()

        # Figure out remaining code phase (uses tcode from Prompt CA Code generation):
        remCodePhase = (tcode[blksize-1]) - 1023.00
        if abs(remCodePhase) > codePhaseStep:
            remCodePhase = sign(remCodePhase)*codePhaseStep
        else:
            remCodePhase = 0
        #print("remCodePhase: %f" %remCodePhase)
        # The line above is not working properly. I believe the tcode array is
        # not correct, but will need to do some debugging, therefore the
        # remCodePhase is set to zero below, for the time being.
        #remCodePhase = 0
        #print("New remCodePhase: %12.8f" %remCodePhase)

        # Generate the carrier frequency to mix the signal to baseband
        #time    = np.linspace(0, blksize/settings.samplingFreq, blksize+1, endpoint=True)
        time = np.array(range(0,blksize+1))/settings.samplingFreq

        #print("Length of time array for cos and sin: %d" %len(time))
        # Get the argument to sin/cos functions
        trigarg = ((carrFreq * 2.0 * np.pi) * time) + remCarrPhase
        remCarrPhase = trigarg[blksize] % (2 * np.pi)

        # Finally compute the signal to mix the collected data to baseband
        carrCos = np.cos(trigarg[0:blksize])
        carrSin = np.sin(trigarg[0:blksize])

        # First mix to baseband
        qBasebandSignal = carrCos * rawSignal
        iBasebandSignal = carrSin * rawSignal

        # Now get early, late, and prompt values for each
        I_E = np.sum(earlyCode  * iBasebandSignal)
        Q_E = np.sum(earlyCode  * qBasebandSignal)
        I_P = np.sum(promptCode * iBasebandSignal)
        Q_P = np.sum(promptCode * qBasebandSignal)
        I_L = np.sum(lateCode   * iBasebandSignal)
        Q_L = np.sum(lateCode   * qBasebandSignal)

        # Find PLL error and update carrier NCO
        # Implement carrier loop discriminator (phase detector)
        carrError = np.arctan(Q_P / I_P) / (2.0 * np.pi)
        trackResults.pllDiscr[loopCount] = carrError

        # Implement carrier loop filter and generate NCO command
        carrNco = oldCarrNco + (tau2carr/tau1carr) * (carrError - oldCarrError) + carrError * (PDIcarr/tau1carr)
        oldCarrNco   = carrNco
        oldCarrError = carrError

        # Modify carrier freq based on NCO command
        carrFreq = carrFreqBasis + carrNco

        trackResults.carrFreq[(loopCount)] = carrFreq # Return real value only?

        # Find DLL error and update code NCO -------------------------------------
        codeError = (np.sqrt(I_E * I_E + Q_E * Q_E) - np.sqrt(I_L * I_L + Q_L * Q_L)) / (np.sqrt(I_E * I_E + Q_E * Q_E) + np.sqrt(I_L * I_L + Q_L * Q_L))

        # Implement code loop filter and generate NCO command
        codeNco = oldCodeNco + (tau2code/tau1code) * (codeError - oldCodeError) + codeError * (PDIcode/tau1code)
        oldCodeNco   = codeNco
        oldCodeError = codeError

        # Modify code freq based on NCO command
        codeFreq = settings.codeFreqBasis - codeNco

        trackResults.codeFreq[(loopCount)] = codeFreq
        trackResults.I_E[loopCount] = I_E
        trackResults.I_P[loopCount] = I_P
        trackResults.I_L[loopCount] = I_L
        trackResults.Q_E[loopCount] = Q_E
        trackResults.Q_P[loopCount] = Q_P
        trackResults.Q_L[loopCount] = Q_L


    plt.plot(trackResults.carrFreq)
    plt.title("Carrier frequency of NCO per ms data sample.")
    plt.show()

    plt.plot(trackResults.I_E**2,label="I_E")
    plt.plot(trackResults.I_P**2,label="I_P")
    plt.plot(trackResults.I_L**2,label="I_L")
    plt.title("In-phase int/dump vs. ms data block")
    plt.legend()
    plt.show()

    plt.plot(trackResults.Q_E**2,label="Q_E")
    plt.plot(trackResults.Q_P**2,label="Q_P")
    plt.plot(trackResults.Q_L**2,label="Q_L")
    plt.title("Quadrature int/dump vs. ms data block")
    plt.show()

    SatelliteData = trackResults.I_P
    for ind,IP in enumerate(SatelliteData):
        if IP > 0.1:
            SatelliteData[ind] = 1
        elif IP < 0.1:
            SatelliteData[ind] = -1

    plt.plot(SatelliteData)
    plt.title("In-phase Prompt per ms (shows data transitions)")
    plt.show()

    plt.plot(trackResults.pllDiscr)
    plt.show()
