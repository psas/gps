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
    '''
    Acquires data from default file when Acquisition.py is run directly
    '''
    # Need these to pass to importFile module
    fs = 4.092*10**6 # Sampling Frequency [Hz]
    numberOfMilliseconds = 14
    sampleLength = numberOfMilliseconds*10**(-3)
    bytesToSkip = 7000000#71000000

    data = IQData()
    # Uncomment one of these lines to choose between Launch12 or gps-sdr-sim data

    # /home/evan/Capstone/gps/resources/JGPS@-32.041913222
    #data.importFile('./resources/JGPS@04.559925043', fs, sampleLength, bytesToSkip)
    data.importFile('./resources/JGPS@-32.041913222', fs, sampleLength, bytesToSkip)
    #data.importFile('../resources/test.max', fs, SampleLength, BytesToSkip)

    acquire(data)


class SatStats:
    def __init__(self):
        self.MaxSNR = None
        self.DopplerHz = None
        self.CodePhaseSamples  = None
        self.CodePhaseChips = None
        self.PeakToSecond = []


def acquire(data, bin_list=range(-8000, 8100, 100), sat_list=range(1, 33),
            show_final_plot=True, save_sat_results=False):
    '''
    Searches for GPS satellites in a raw IQ stream. File must be encodede to the
    specifications found in the README

    ## Args:

    data: gps.IQData object that has already been trimmed to length.

    ## kwArgs:
    bin_list: int list of frequency bins to search across. Defaults to 8kHz above and below carrier
    in 100Hz steps.

    sat_list: int list of SVs to use in acquisition. Defaults to the 32 active GPS satellites.

    showFinalPlot: bool determines whether matplotlib displays a bar graph of the final acquisition
    results. Defaults to True.

    saveSatResults: bool determines whether matplotlib saves a plot of each SV's frequency search.
    Defaults to False.

    ## Returns:
    object containing acquisition results

    '''
    #Choose what frequencies and satellites to increment over

    numberOfMilliseconds = data.sampleTime * 1000


    # Create list of C/A code Taps, for simpler sat selection",
    sat = [(1, 5), (2, 6), (3, 7), (4, 8), (0, 8), (1, 5), (0, 7), (1, 8), (2, 9), (1, 2),
           (2, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 3), (1, 4), (2, 5), (3, 6),
           (4, 7), (5, 8), (0, 2), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (0, 5), (1, 6),
           (2, 7), (3, 8), (4, 9), (3, 9), (0, 6), (1, 7), (3, 9)]

    # Create array to store max values, freq ranges, per satellite
    #SatMax = np.zeros((len(SatelliteList),len(FrequencyList),4))
    satInfoList = []
    for x in range(33):
        satInfoList.append(SatStats())
    maxVals = np.zeros(len(sat_list) + 1)

    satInd = 0
    # Loop through selected satellites
    for curSat in sat_list:
        print("Searching for SV " + str(curSat) + "...")
        # Create Code Generator object for chosen Satellite
        codeGen = GoldCode(sat[curSat - 1]) # Index starts at zero

        # Generate CA Code
        CACode = codeGen.getCode(1023, samplesPerChip=4)


        # Repeat entire array for each ms of data sampled
        CACodeSampled = np.tile(CACode, int(numberOfMilliseconds))

        acqResult = findSat(data, CACodeSampled, bin_list)
        satInfoList[satInd+1] = acqResult

        if save_sat_results:
            plt.figure()
            plt.plot(bin_list, SatInfo[satInd].PeakToSecond)
            plt.ylim((0, 20))
            plt.xlabel('Doppler Shift (Hz)')
            plt.ylabel('Peak-to-SecondLargest ratio (dB)')
            plt.title("Sat %d - PeakToSecondLargest"%curSat)
            plt.show()


        maxVals[satInd + 1] = np.amax(satInfoList[satInd+1].PeakToSecond)

        satInd = satInd+1
    if show_final_plot:
        _outputplot(maxVals)
        _outputTable(satInfoList)
    return satInfoList

def findSat(data, code, bins, tracking = False):
    '''
    Searches IQ Data for a single satellite across all specified frequencies.

    ## Args:

    data: gps.IQData object that has already been trimmed to length.

    code: C/A code for the desired satellite that has been generated, sampled,
    and extended.

    ## kwArgs:


    ## Returns:
    object containing acquisition results for the satellite

    '''

    # Place to store current satellite information
    curSatInfo = SatStats()

    SNR_THRESHOLD = 3.4
    #if tracking is True:
    peakToSecondList = np.zeros(len(bins))
    codePhaseList = np.zeros(len(bins))
    SNRList = np.zeros(len(bins))

    codefft = np.fft.fft(code, data.Nsamples)

    GCConj = np.conjugate(codefft)
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

        resultSQ = np.real(result * np.conjugate(result))

        rmsPowerdB = 10*np.log10(np.mean(resultSQ))
        resultdB = 10*np.log10(resultSQ)

        codePhaseInSamples = np.argmax(resultSQ[0:4092])

        # Search for secondlargest value in 1 ms worth of data
        secondLargestValue = _GetSecondLargest(resultSQ[0:int(data.sampleFreq*0.001)])

        # Pseudo SNR
        firstPeak = np.amax(resultSQ[0:4092])
        peakToSecond =  10*np.log10(  firstPeak/secondLargestValue  )

        curSatInfo.PeakToSecond.append(peakToSecond)

        #if tracking is True:
        peakToSecondList[n] = peakToSecond
        codePhaseList[n] = codePhaseInSamples
        SNRList[n] = 10*np.log10(  firstPeak/np.mean(resultSQ)  )

        # Don't print data when correlation is probably not happening
        if peakToSecond > SNR_THRESHOLD:
            print("Possible acquisition: Freq: %8.4f, Peak2Second: %8.4f, Code Phase (samples): %8.4f"
                  %(curFreq, peakToSecond, codePhaseInSamples))

        freqInd = freqInd + 1

        # Percentage Output
        print("%02d%%"%((n/N)*100), end="\r")
    maxFreqThisSat = bins[np.argmax(peakToSecondList)]
    codePhaseThisSat = codePhaseList[np.argmax(peakToSecondList)]
    maxSNRThisSat = SNRList[np.argmax(peakToSecondList)]
    curSatInfo.MaxSNR = maxSNRThisSat
    curSatInfo.DopplerHz = maxFreqThisSat
    curSatInfo.CodePhaseSamples = codePhaseThisSat
    L1SampleRatio = (1.023*10**6)/(4.092*10**6)
    curSatInfo.CodePhaseChips = 1023 - L1SampleRatio*codePhaseThisSat
    return curSatInfo


def _outputTable(satInfoList):
    print("|-----+---------------+--------------+--------------+--------------------+----------------------|")
    print("| PRN | Max SNR (dB)  | P2StoP2Smean | Doppler [Hz] | Code Phase [Chips] | Code Phase [Samples] |")
    print("|-----+---------------+--------------+--------------+--------------------+----------------------|")
    for i in range(1,33):
        P2SToMeanP2SdB = 10*np.log10(  np.amax(satInfoList[i].PeakToSecond)/np.mean(satInfoList[i].PeakToSecond)  )
        if P2SToMeanP2SdB >= 7:
            print("| %2d     %8.3f        %8.3f       %6d           %9.3f               %6d         |"
                  %(i,satInfoList[i].MaxSNR, P2SToMeanP2SdB , satInfoList[i].DopplerHz,satInfoList[i].CodePhaseChips, satInfoList[i].CodePhaseSamples))
    print("|-----+---------------+--------------+--------------+--------------------+----------------------|")


def _outputplot(ratios):
    '''
    Outputs a formatted matplotlib plot of the highest pseudo-SNR value for each SW across all
    frequencies.
    '''

    ran = np.arange(len(ratios))
    fig, ax = plt.subplots(figsize=[10, 8])

    #Use highest correlations for the 6 highest channels
    channels = np.argpartition(ratios, -6)[-6:]

    ax.bar(ran, ratios, linewidth=0, color='#aec7e8', align='center')
    #ax.set_axis_bgcolor('#e3ecf9')

    childrenLS = ax.get_children()
    barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), childrenLS)

    for n, bar0 in enumerate(barlist):
        if n in channels:
            bar0.set_color('#ffbb78')
            bar0.edgecolor = 'b'
            bar0.linewidth = 6
        elif (n != 33) and ratios[n] > 3.0:
            bar0.set_color('#98df8a')

    plt.xlim([0, len(ratios) + 1])
    plt.title('Acquisition Results')
    plt.ylabel('Ratio of top 2 peaks (abs squared)')
    plt.xlabel('Satellite')
    plt.show()

def _GetSecondLargest(DataList):
    '''
    Returns the second largest value in an array
    '''
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

    for ind, val in enumerate(DataArray):
        if val < ScaledLargest:
            if val > SecondLargest:
            #Ignore adjacent bins to Largest
                if np.abs(LargestIndex-ind) > 100:
                    SecondLargest = val
                    SecondLargestIndex = ind

    #print("Second largest value: %f, at position: %d"%(SecondLargest,SecondLargestIndex))
    return SecondLargest


if __name__ == "__main__":
    main()
