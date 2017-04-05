#!/usr/bin/env python3  
'''
Portland State Aerospace Society

GPS signal acquisition

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from GoldCode import GoldCode
from GPSData import IQData

def main():
    # Need these to pass to importFile module
    fs = 4.092*10**6 # Sampling Frequency [Hz]
    NumberOfMilliseconds = 14
    SampleLength = NumberOfMilliseconds*10**(-3)
    BytesToSkip = 0

    data = IQData()

    # Uncomment one of these lines to choose between Launch12 or gps-sdr-sim data
    data.importFile('./resources/JGPS@04.559925043', fs, SampleLength, BytesToSkip)
    #data.importFile('../resources/test.max', fs, SampleLength, BytesToSkip)

    acquire(data)

class SatStats():
    def __init__(self, SatName):
        self.SatName = SatName
        self.dBPeakToMean = []
        self.PeakToSecond = []
    

def acquire(data, showFinalPlot = True, saveSatResults = False):
    #Choose what frequencies and satellites to increment over
    StartingFrequencyShift = -8*10**3
    EndingFrequencyShift = 8*10**3
    FrequencyShiftIncrement = 100
    FrequencyList = range(StartingFrequencyShift,EndingFrequencyShift + FrequencyShiftIncrement,FrequencyShiftIncrement)
    NumberOfMilliseconds = data.sampleTime * 1000
    nfft = data.Nsamples
    fs = data.sampleFreq
    StartingSatellite = 1
    EndingSatellite = 32
    SatelliteList = range(StartingSatellite, EndingSatellite + 1)

    # Create list of C/A code Taps, for simpler sat selection",
    sat = [(1,5),(2,6),(3,7),(4,8),(0,8),(1,5),(0,7),(1,8),(2,9),(1,2),(2,3),(4,5),(5,6),(6,7),(7,8),(8,9),(0,3),(1,4),(2,5),(3,6),(4,7),(5,8),(0,2),(3,5),(4,6),(5,7),(6,8),(7,9),(0,5),(1,6),(2,7),(3,8),(4,9),(3,9),(0,6),(1,7),(3,9)]

    # Create array to store max values, freq ranges, per satellite
    #SatMax = np.zeros((len(SatelliteList),len(FrequencyList),4))

    maxVals = np.zeros(EndingSatellite + 1)

    satInd = 0 
    # Loop through selected satellites
    for curSat in SatelliteList: 
        print("Searching for SV " + str(curSat) + "...")
        # Create Code Generator object for chosen Satellite
        CodeGen = GoldCode(sat[curSat - 1]) # Index starts at zero

        # Generate CA Code
        CACode = CodeGen.getCode(1023)

        # Repeat each chip 4 times (See markdown in above cell), to match our ADC sample frequency",
        CACodeSampled = np.repeat(CACode,4)

        # Repeat entire array for each ms of data sampled
        CACodeSampled = np.tile(CACodeSampled,NumberOfMilliseconds)
       
        acqResult = findSat(data, CACodeSampled, FrequencyList)

        #Peak to Mean doesn't show as much as peak to second-largest
        if saveSatResults == True:
            plt.figure()
            plt.plot(FrequencyList, SatInfo[satInd].PeakToSecond)
            plt.ylim((0,20))
            plt.xlabel('Doppler Shift (Hz)')
            plt.ylabel('Peak-to-SecondLargest ratio (dB)')
            plt.title("Sat %d - PeakToSecondLargest"%curSat)
            plt.show()
        

        maxVals[satInd + 1] = max(acqResult[1])
        satInd = satInd+1
    if showFinalPlot == True:
        _outputplot(maxVals)

def findSat(data, code, bins, tracking = False):
    #Inputs: some IQ data, a CA code, and the frequency bins to seach through
    #Outputs: The frequency bin where acquired, and a list of pseudo-SNRs,
    

    SNR_THRESHOLD = 3.4
    #if tracking is True:
    PeakToSecondList = np.zeros(len(bins))
    Codefft = np.fft.fft(code,data.Nsamples)
    
    GCConj = np.conjugate(Codefft)
    N = len(bins)
    freqInd = 0
    # Loop through all frequencies
    for n, curFreq in enumerate(bins):
        # Initialize complex array
        CDataShifted = np.zeros(len(data.CData), dtype=np.complex)

        # Shift frequency using complex exponential 
        CDataShifted = data.CData*np.exp(-1j*2*np.pi*curFreq*data.t)

        fftCDataShifted = np.fft.fft(CDataShifted, data.Nsamples)

        result = np.fft.ifft(GCConj * fftCDataShifted, data.Nsamples)

        resultSQ = np.real(result*np.conjugate(result))

        rmsPowerdB = 10*np.log10(np.mean(resultSQ))
        resultdB= 10*np.log10(resultSQ)

        maxAbsSquared = np.amax(resultSQ)
        maxAbsSquaredInd = np.argmax(resultSQ)
        phaseInTime = maxAbsSquaredInd/data.sampleFreq
        phaseInChips = phaseInTime*1.023*10**6
        phaseInChips = 1023 - phaseInChips%1023

        maxdB = np.amax(resultdB)
        maxdBInd = np.argmax(resultdB)

        PeakTodBRatio = maxdB - rmsPowerdB

        # Search for secondlargest value in 1 ms worth of data
        SecondLargestValue = _GetSecondLargest(resultSQ[0:int(data.sampleFreq*0.001)])

        # Pseudo SNR

        PeakToSecond = ( 10*np.log10(np.amax(resultSQ)/SecondLargestValue))
        #if tracking is True:
        PeakToSecondList[n] = PeakToSecond 

        #SatInfo[satInd].dBPeakToMean.append(PeakTodBRatio)

        # Don't print data when correlation is probably not happening
        if PeakToSecond > SNR_THRESHOLD:
            print("Possible acquisition: Freq: %8.4f, PeakToMean: %8.4f, PeakToSecond: %8.4f, Phase (chips): %8.4f"%(curFreq,PeakTodBRatio,PeakToSecond, phaseInChips))

        freqInd = freqInd + 1

        print("%02d%%"%((n/N)*100), end = "\r")
    MaxFreqThisSat = bins[np.argmax(PeakToSecondList)]

    return (MaxFreqThisSat, PeakToSecondList)





def _outputplot(ratios):
    #Creates an output plot that shows the acquisition result for all SVs
    ran = np.arange(len(ratios))
    fig, ax = plt.subplots(figsize = [10,8])

    #Use highest correlations for the 6 highest channels
    channels = np.argpartition(ratios, -6)[-6:]

    ax.bar(ran, ratios, linewidth=1)
    ax.set_axis_bgcolor('#898b8e')

    childrenLS = ax.get_children()
    barlist=filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), childrenLS)

    for n, bar in enumerate(barlist):
        if n in channels:
            bar.set_color('#99ff66')
            bar.edgecolor = 'white'
            bar.linewidth = 6
                                            
    plt.xlim([0, len(ratios) + 1])
    plt.title('Acquisition Results')
    plt.ylabel('Ratio of top 2 peaks (dB)')
    plt.xlabel('Satellite')
    plt.show()

def _GetSecondLargest(DataList):
    # This will return second largest value
    # It will also ignore any value that is close to the second largest value
    
    # Make sure is a numpy array
    DataArray = np.array(DataList)

    # Find largest value
    Largest = np.amax(DataArray)
    LargestIndex = np.argmax(DataArray)
    #print("Largest value: %f, at position: %d"%(Largest,LargestIndex))

    # Reduce value by a percent to prevent near-identical values from being selected
    ScaleAmount = 0.95
    ScaledLargest = ScaleAmount*Largest
    SecondLargest = 0
    SecondLargestIndex = 0

    for ind,val in enumerate(DataArray):
        if val < ScaledLargest:
            if val > SecondLargest:
            #Ignore adjacent bins to Largest
                if (np.abs(LargestIndex-ind) > 100):
                    SecondLargest = val
                    SecondLargestIndex = ind

    #print("Second largest value: %f, at position: %d"%(SecondLargest,SecondLargestIndex))
    return SecondLargest


if __name__ == "__main__":
    main()
