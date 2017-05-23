#!/usr/bin/env python3

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
import configparser

import Acquisition

import GoldCode
from GPSData import IQData

global GPS_conf

#np.set_printoptions(threshold=np.inf)

def main():
    # Import data. Will read many ms at once, then process the blocks as needed.
    # Need these to pass to importFile module
    fs = 4.092*10**6 # Sampling Frequency [Hz]
    numberOfMilliseconds = 350
    sampleLength = numberOfMilliseconds*10**(-3)
    bytesToSkip = 0
    global GPS_conf
    GPS_conf = configparser.ConfigParser()
    GPS_conf.read('Settings.conf')

    data = IQData()
    # Uncomment one of these lines to choose between Launch12 or gps-sdr-sim data

    # /home/evan/Capstone/gps/resources/JGPS@-32.041913222
    #data.importFile('resources/JGPS@04.559925043', fs, sampleLength, bytesToSkip)
    #data.importFile('resources/JGPS@-32.041913222', fs, sampleLength, bytesToSkip)
    #data.importFile('resources/test4092kHz.max', fs, sampleLength, bytesToSkip)
    data.importFile('resources/Single4092KHz5s.max', fs, sampleLength, bytesToSkip)
    RealDataOnly = True
    #data.importFile('resources/Single4092KHz60s.max', fs, sampleLength, bytesToSkip, RealDataOnly)
    #data.importFile('resources/Single4092KHz120s.max', fs, sampleLength, bytesToSkip, RealDataOnly)

    acqresult = Acquisition.SatStats()
    theCodePhase = 630.251585
    acqresult.CodePhaseSamples = int((1023.0 - theCodePhase)*4 + 1)
    acqresult.FineFrequencyEstimate = -3363.8
    acqresult.Sat = 1

    chartOut = True
    channel1 = Channel(data, acqresult, chartOut)
    channel1.Track()
    #channel1._writeBits()
    channel1._writeBits2()
    #channel1.GetEphemeris()





class Channel:
    '''
    Class that is a channel dedicated to tracking one satellite through a section of data.
    At least 4 are required to get a pseudorange.
    '''
    def __init__(self, datain, acqData, chartoutput = True):
        
        global GPS_conf
        self.settings = GPS_conf['TRACKING']
        
        #Acquisition inputs
        self.data = datain
        self.codePhase = acqData.CodePhaseSamples
        self.acquiredCarrFreq = acqData.FineFrequencyEstimate
        self.PRN = acqData.Sat # Value will be non-zero if Acquisition was successful for this channel

        self.progress = True #Output progress
        self.status = False # True if tracking was successful, False otherwise.
        
        self.SamplesPerChip = int(float(GPS_conf['DATA']['fs']) /
                                  float(self.settings['codeFreqBasis']))

        #Tracking Result/Logging Parameters
        self.outputChart = chartoutput
        # We still need I_P for data processing, even without needing to plot.
        #if self.outputChart:
        if True:
            #Preallocate space if charts are requested
            self.absoluteSample = np.zeros(int(self.settings['msToProcess']))   # Sample that C/A code 1st starts.
            self.codeFreq = np.zeros(int(self.settings['msToProcess']))         # C/A code frequency.
            self.carrFreq = np.zeros(int(self.settings['msToProcess']))         # Frequency of tracked carrier.
            
            self.I_P  = np.zeros(int(self.settings['msToProcess']))             # Correlator outputs (resulting sum).
            self.I_E  = np.zeros(int(self.settings['msToProcess']))             # Correlator outputs (resulting sum).
            self.I_L  = np.zeros(int(self.settings['msToProcess']))             # Correlator outputs (resulting sum).
            self.Q_P  = np.zeros(int(self.settings['msToProcess']))             # Correlator outputs (resulting sum).
            self.Q_E  = np.zeros(int(self.settings['msToProcess']))             # Correlator outputs (resulting sum).
            self.Q_L  = np.zeros(int(self.settings['msToProcess']))             # Correlator outputs (resulting sum).
            
            self.dllDiscr = np.zeros(int(self.settings['msToProcess']))         # Code-Loop discriminator
            self.dllDiscrFilt = np.zeros(int(self.settings['msToProcess']))     # Code-Loop discriminator filter
            self.pllDiscr = np.zeros(int(self.settings['msToProcess']))         # Carrier-Loop discriminator
            self.pllDiscrFilt = np.zeros(int(self.settings['msToProcess']))     # Carrier-Loop discriminator filter
    
    def Track(self):
        '''
        Retrieves data from data array (self.data), and aligns the replica code and 
        carrier to get navigation bits. Takes no arguments, but reads from self.data,
        and outputs navigation data on self.I_P.
        '''
        global GPS_conf

        # Calculate filter coefficient values for code loop
        coeffCode1, coeffCode2 = self._calcLoopCoef(float(self.settings['codeLoopNoiseBandwidth'])
                                                , float(self.settings['codeZeta']), float(self.settings['codeLoopGain']))

        # Calculate filter coefficient values for carrier loop
        coeffCar1, coeffCar2 = self._calcLoopCoef(float(self.settings['carrLoopNoiseBandwidth'])
                                                , float(self.settings['carrZeta']), float(self.settings['carrLoopGain']))

        # Process each channel (Will impliment loop in future. For now only processing one channel)
        # Process channel if PRN is non-zero (Acquisition successful)
        if self.PRN:
            # Create instance of TrackingResults to store results into
            CACode = GoldCode.getTrackingCode(self.PRN)

            # Perform additional initializations:
            codeFreq = float(self.settings['codeFreqBasis'])

            # Residual code/carrier phase
            remCodePhase = 0.0
            remCarrPhase  = 0.0

            # code tracking loop parameters
            oldCodeNco   = 0.0
            oldCodeError = 0.0

            # carrier/Costas loop parameters
            oldCarrNco   = 0.0
            oldCarrError = 0.0

            dataPosition = 0
            blksize = 0

            carrFreq = self.acquiredCarrFreq

            #Pre-cast configuration parameters
            ms = int(self.settings['msToProcess'])
            fs = float(GPS_conf['DATA']['fs'])
            codeLength = int(self.settings['codeLength'])
            earlyLateSpacing = float(self.settings['earlyLateSpacing'])
            chippingRate = float(self.settings['codeFreqBasis'])

            # Process the requested number of code periods (num of ms to process)
            for loopCount in range(0, ms):
                if self.progress:
                    print("------- %2.1f percent complete --------"%((loopCount/ms)*100), end = '\r')
                
                # Update the phasestep based on code freq (variable) and
                # sampling frequency (fixed)
                codePhaseStep = np.real(codeFreq / fs)

                #print("Old blksize: %d"%blksize)
                blksize = int(np.ceil((codeLength-remCodePhase) / codePhaseStep))
                #print("New blksize: %d"%blksize)
                #print("Old remCodePhase: %f" %remCodePhase)

                # Read in the appropriate number of samples to process this
                # iteration
                rawSignal = self.data.IData[self.codePhase + dataPosition: self.codePhase + dataPosition + blksize]
                dataPosition = dataPosition + blksize


                # Generate Early CA Code.
                tStart = remCodePhase - earlyLateSpacing
                tStep = codePhaseStep
                tEnd = ((blksize-1)*codePhaseStep+remCodePhase) + codePhaseStep - earlyLateSpacing
                tcode = np.linspace(tStart,tEnd,blksize,endpoint=False)
                tcode2 = (np.ceil(tcode)).astype(int)
                earlyCode = CACode[tcode2]


                # Generate Late CA Code.
                tStart = remCodePhase + earlyLateSpacing
                tStep = codePhaseStep
                tEnd = ((blksize-1)*codePhaseStep+remCodePhase) + codePhaseStep + earlyLateSpacing
                tcode = np.linspace(tStart,tEnd,blksize,endpoint=False)
                tcode2 = (np.ceil(tcode)).astype(int)
                lateCode = CACode[tcode2]


                # Generate Prompt CA Code.
                tStart = remCodePhase
                tStep = codePhaseStep
                tEnd = ((blksize-1)*codePhaseStep+remCodePhase) + codePhaseStep
                tcode = np.linspace(tStart,tEnd,blksize,endpoint=False)
                tcode2 = (np.ceil(tcode)).astype(int)
                promptCode = CACode[tcode2]


                # Figure out remaining code phase (uses tcode from Prompt CA Code generation):
                remCodePhase = (tcode[blksize-1]) - 1023.00
                if abs(remCodePhase) > codePhaseStep:
                    remCodePhase = sign(remCodePhase)*codePhaseStep
                else:
                    remCodePhase = 0
                #print("remCodePhase: %f" %remCodePhase)
                
                # Generate the carrier frequency to mix the signal to baseband
                time = np.array(range(0,blksize+1))/fs

                #print("Length of time array for cos and sin: %d" %len(time))
                # Get the argument to sin/cos functions
                trigarg = ((carrFreq * 2.0 * np.pi) * time) + remCarrPhase
                
                # Carry the leftover phase to the next argument by looking at the last element
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

                # Implement carrier loop filter and generate NCO command
                carrNco = oldCarrNco + coeffCar1 * (carrError - oldCarrError) + carrError * coeffCar2
                oldCarrNco   = carrNco
                oldCarrError = carrError

                # Modify carrier freq based on NCO command
                carrFreq = self.acquiredCarrFreq + carrNco

                # Find DLL error and update code NCO -------------------------------------
                codeError = (np.sqrt(I_E * I_E + Q_E * Q_E) - np.sqrt(I_L * I_L + Q_L * Q_L)) /\
                            (np.sqrt(I_E * I_E + Q_E * Q_E) + np.sqrt(I_L * I_L + Q_L * Q_L))

                # Implement code loop filter and generate NCO command
                codeNco = oldCodeNco + coeffCode1 * (codeError - oldCodeError) + codeError * coeffCode2
                oldCodeNco   = codeNco
                oldCodeError = codeError

                # Modify code freq based on NCO command
                codeFreq = chippingRate - codeNco

                if self.outputChart:
                    self.pllDiscr[loopCount] = carrError
                    self.carrFreq[(loopCount)] = carrFreq # Return real value only?

                    self.codeFreq[(loopCount)] = codeFreq
                    self.I_E[loopCount] = I_E
                    self.I_P[loopCount] = I_P
                    self.I_L[loopCount] = I_L
                    self.Q_E[loopCount] = Q_E
                    self.Q_P[loopCount] = Q_P
                    self.Q_L[loopCount] = Q_L

            if self.outputChart:
                self._plotOutputs()
                

    def _plotOutputs(self):
        plt.plot(self.carrFreq)
        plt.ylabel("PLL Frequency (Hz)")
        plt.xlabel("t (ms)")
        plt.title("Carrier frequency of NCO")
        plt.show()
        
        plt.subplot(2,1,1)
        plt.plot(self.I_E**2,label="I_E")
        plt.plot(self.I_P**2,label="I_P")
        plt.plot(self.I_L**2,label="I_L")
        plt.title("DLL Inphase")
        plt.legend()
        
        plt.subplot(2,1,2)
        plt.plot(self.Q_E**2,label="Q_E")
        plt.plot(self.Q_P**2,label="Q_P")
        plt.plot(self.Q_L**2,label="Q_L")
        plt.title("DLL Quadrature")
        plt.xlabel("t (ms)")
        plt.show()

        SatelliteData = self.I_P
        for ind,IP in enumerate(SatelliteData):
            if IP > 0.1:
                SatelliteData[ind] = 1
            elif IP < 0.1:
                SatelliteData[ind] = 0

        plt.plot(SatelliteData)
        plt.ylim([-.5,1.5])
        plt.title("50bps Navigation Data (from I_P)")
        plt.show()

        #plt.plot(self.pllDiscr)
        #plt.show()

    def _calcLoopCoef(self, LoopNoiseBandwidth, Zeta, LoopGain):
        '''
        Calculates the loop coefficients tau1 and tau2. 

        This process is discussed in sections 7.1-7.3 of Borre.
        '''
        # Solve for the natural frequency
        Wn = LoopNoiseBandwidth*8*Zeta / (4*Zeta**2 + 1)

        # Solve for tau1 and tau2
        tau1 = LoopGain / (Wn * Wn);
        tau2 = (2.0 * Zeta) / Wn;

        coeff1 = tau2/tau1
        coeff2 = float(self.settings['sumInt'])/tau1

        return (coeff1, coeff2)

    def _writeBits(self, dr = '.', name = 'default'):
        '''
        Writes out the navigation data bits to a file for analysis using navigation tools. This version is 
        not fully working.
        '''

        if name == 'default':
            name = 'SV%s.bin'%self.PRN
        
        # First find a bit transition to be the starting index of the integration
        start = np.sign(self.I_P[0])

        startInd = 0
        for samp in self.I_P:
            if (np.sign(samp) != start ):
                break
            else:
                startInd += 1
            
        #Start integrating bits in groups of 20ms
        ptr = 0
        bits = np.zeros(len(self.I_P)/20)

        for ind in range(startInd, len(self.I_P), 20):
            m = np.mean(self.I_P[ind:ind+20])
            
            if np.sign(m) == 1:
                bits[ptr] = 1
            elif np.sign(m) == -1:
                bits[ptr] = 0
            else:
                pass
                #raise BitsError(ind)
            ptr += 1
        
        #Write out the ms offset, followed by bitstream
        with open( '%s/%s'%(dr, name),'w') as f:
            f.write("%1d"%startInd) 
            f.writelines(["%3d" % item  for item in bits])
            print()
            print("File written to: %s"%f.name)
                


    def _writeBits2(self, dr = '.', name = 'default'):
        '''
        Writes out the navigation data bits to a file, revised from _writeBits()

        # kwArgs

        dr: directory where the file of bits ends up. Default is the cwd.
        
        name: prefix of the name of the exported file to differetiate it from other channels.
              default is to use SV followed by the identification number of the satellite. 

        # ToDo

        - Add a timestamp option for the filename. This differetiates the file from other 'runs'
        of the tracking algorithm.
        '''

        
        if name == 'default':
            name = 'SV%s.bin'%self.PRN

        # Quantize I_P levels to be either 0 or 1
        SatelliteData = np.zeros(len(self.I_P), dtype=int)
        self.SatelliteBits = []
        for ind,IP in enumerate(self.I_P):
            if IP >= 0.1:
                SatelliteData[ind] = 1
            elif IP < 0.1:
                SatelliteData[ind] = 0
            # Save value every 20ms (choose middle value)
            if (ind%20 == 10): # If middle of 20ms chunk
                self.SatelliteBits.append(SatelliteData[ind])# store bit value

        fHandle = open(name,'wb')
        fHandle.write(bytes(self.SatelliteBits))
        print()
        print("Total data bits: %d, written to file: %s."%(len(self.SatelliteBits),fHandle.name))

    

class BitsError(Exception):
    def __init__(self, index):
        self.message = "Integration Error at index %d"%index

        print(self.message)



if __name__ == "__main__":
    main()