import numpy as np
import matplotlib.pyplot as plt

def FreqResolutionCell(N,Ts):
    # Returns the frequency resolution cell (Section 8.8 of Tsui)
    return 1/(N*Ts)

def FineFrequencyEstimation(CData,Ts,SamplesBetween):
    # This estimates the fine frequency, by way of DFT.
    # It determines the frequency of the sinusoid by taking a DFT,
    # and finding the tallest bin. Afterwards, a subsequent DFT is
    # performed on a section of data that has been advanced in time
    # by the number of samples specified by SamplesBetween. Using
    # equation 8.42 in Tsui, the fine frequency is determined. The
    # phase difference must be less than (2pi)/5, therefore the number
    # of samples between should be less than: (2*pi*DopplerFreq)/(fs).
    # For 1 kHz, there needs to be < 818 samples in between and for
    # 10 kHz (max expected doppler), there needs to be < 81 samples
    # between. There doesn't appear to be any gain in frequency resolution
    # from varying the SamplesBetween, so some small value (~10) will
    # be used for now. Increasing the size of CData DOES increase the
    # resolution.

    fs = 1/Ts

    # DFT length
    DFT = len(CData) - SamplesBetween

    # Generate frequency vector
    f = np.linspace(0,fs,DFT,endpoint=True)

    # Get first phase angle from highest frequency component
    X1 = np.fft.fft(CData[0:len(CData) - SamplesBetween - 1], DFT)
    maxFreqBin = np.argmax(X1)
    maxFreq1 = f[maxFreqBin]
    #print(maxFreq1)
    angleFound1 = np.arctan2(np.imag(X1[maxFreqBin]),np.real(X1[maxFreqBin]))

    # Get second phase angle using same frequency index from before,
    # but this time from a different time period.
    X2 = np.fft.fft(CData[SamplesBetween:len(CData) - 1], DFT)
    #print(maxFreq2)
    angleFound2 = np.arctan2(np.imag(X2[maxFreqBin]),np.real(X2[maxFreqBin]))

    # Now calculate fine-frequency estimation
    FineFreq = (angleFound2-angleFound1)/(SamplesBetween*Ts*2*np.pi)

    return FineFreq

def FineFrequencyEstimationSingleK(CData1,CData2,Ts,k):
    # Similar to above function, but performs DFT at single value
    # of k. In this case, k can be a non-integer value.
    # Note, CData1,CData2 are assumed to be CData split in two.
    # The frequency must be << FreqResolutionCell, for the results to
    # work.

    fs = 1/Ts

    # DFT length
    N = len(CData1)

    X1_k = 0.0
    for n in range(N):
        X1_k += np.exp(-1j*2*np.pi*n*k/N)*CData1[n]
    angleFound1 = np.arctan2(np.imag(X1_k),np.real(X1_k))

    X2_k = 0.0
    for n in range(N):
        X2_k += np.exp(-1j*2*np.pi*n*k/N)*CData2[n]
    angleFound2 = np.arctan2(np.imag(X2_k),np.real(X2_k))

    # Check for phase-discontinuity
    Nth = np.exp(-1j*2*np.pi*k)
    NthPhase = np.angle(Nth)
    print(NthPhase)

    FineFreq = (angleFound2-angleFound1-NthPhase)/(len(CData1)*Ts*2*np.pi)

    return FineFreq

def StartingPhaseAngle(CData,Ts):
    fs = 1/Ts
    DFT = len(CData)

    f = np.linspace(0,fs,DFT,endpoint=True)
    X = np.fft.fft(CData,DFT)
    maxFreqBin = np.argmax(X)
    maxFreq = f[maxFreqBin]

    angleFound = np.arctan2(np.imag(X[maxFreqBin]),np.real(X[maxFreqBin]))
    return angleFound
