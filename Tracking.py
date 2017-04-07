'''
Portland State Aerospace Society

Tracking.py

Creates channels for acquired satellites, and locks on to the CDMA transmission to get
position, velocity, and time data.

'''
import numpy as np
import matplotlib.pyplot as plt
from GoldCode import GoldCode
from GPSData import IQData

def main():
    '''
    Function executed when Tracking.py is executed standalone.

    '''
    # Bring in some data
    fs = 4.092*10**6 # Sampling Frequency [Hz]
    numberOfMilliseconds = 40
    sampleLength = numberOfMilliseconds*10**(-3)
    bytesToSkip = 0

    data = IQData()
    data.importFile('./resources/JGPS@04.559925043', fs, sampleLength, bytesToSkip)

    

class TrackingChannel():
    '''
    Class for a single channel in the reciever
    '''

    self.Locked = False

    self.Ie = 0.0
    self.Ip = 0.0
    self.Il = 0.0
    
    self.Qe = 0.0
    self.Qp = 0.0
    self.Ql = 0.0

    self.Dcode = 0.0
    self.Dcarr = 0.0

    def __init__(self, sat_ind, acq_phase, samples_per_chip=4, chip_delay=0.5):
        self.InitTrackingCodes(sat_ind, acq_phase, samples_per_chip=4, chip_delay=0.5)
    
    def Update(datams):
        '''
        Feed this function 1ms of data to track the assigned satellite
        '''
        _mixAndSum(datams.IData, datams.QData)
        _discriminators()

    def _mixAndSum(Idata, Qdata)
        '''
        Pass this 1ms of Idata and 1ms of Qdata, the tracking values will update
        '''

        self.Ie = np.sum(Idata * self.codeE)
        self.Ip = np.sum(Idata * self.codeP)
        self.Il = np.sum(Idata * self.codeL)
        
        self.Qe = np.sum(Qdata * self.codeE)
        self.Qp = np.sum(Qdata * self.codeP)
        self.Ql = np.sum(Qdata * self.codeL)

    def _discriminators():
        '''
        Updates Code and carrier discriminators
        '''
        
        self.Dcode = ((self.Ie ** 2 + self.Qe ** 2) - (self.Il ** 2 + self.Ql ** 2)) / ((self.Ie ** 2 + self.Qe ** 2) + (self.Il ** 2 + self.Ql ** 2))
        self.Dcarr = (np.arctan(self.Qp / self.Ip) / (2 * np.pi))

    def InitTrackingCodes(sat_ind, estimated_phase, samples_per_chip=4, chip_delay=0.5):
        '''
        sets Early,Late,Prompt CA Codes for the channel.

        # Args
        satPRL - PRL number of CA code to generate
        
        estimatePhase - Phase estimate from Acquisition in samples
        
        samplesPerChip - How many times a single chip is sampled. This
            is a function of sampling frequency and chip-rate.
        
        chipDelay - How many samples away is the Early and Late CA code
            from the Prompt code. Typically will be half a chip.

        #Returns


        '''
        # Create list of C/A code Taps, for simpler sat selection (zero-indexed)
        sat = [(1, 5), (2, 6), (3, 7), (4, 8), (0, 8), (1, 5), (0, 7), (1, 8), (2, 9), (1, 2),
            (2, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 3), (1, 4), (2, 5), (3, 6),
            (4, 7), (5, 8), (0, 2), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (0, 5), (1, 6),
            (2, 7), (3, 8), (4, 9), (3, 9), (0, 6), (1, 7), (3, 9)]

        # Create Code Generator object for chosen Satellite
        self.CodeGen = GoldCode(sat[sat_ind - 1]) # Index starts at zero

        # Generate Prompt code, using estimated phase from Acquisition
        # Numpy array allows the array to be "rolled" (circular shifted)
        # Note: if phase is positive, it will be shifted left (reason for minus in roll)
        self.codeP = np.array(CodeGen.getCode(1023, samplesPerChip=samples_per_chip))
        self.codeP = np.roll(codeP, -estimated_phase)

        # Create Early and Late codes, by shifting Prompt code
        self.codeE = np.roll(codeP, -chip_delay)
        self.codeL = np.roll(codeP, chip_delay)

        


def GetTrackingCodes(sat_ind, estimated_phase, samples_per_chip=4, chip_delay=0.5):
    '''
    Returns Early,Late,Prompt CA Codes.

    # Args
    satPRL - PRL number of CA code to generate
    
    estimatePhase - Phase estimate from Acquisition in samples
    
    samplesPerChip - How many times a single chip is sampled. This
        is a function of sampling frequency and chip-rate.
    
    chipDelay - How many samples away is the Early and Late CA code
        from the Prompt code. Typically will be half a chip.

    #Returns

    3 element tuple containing the E, P, and L codes.

    '''
    # Create list of C/A code Taps, for simpler sat selection (zero-indexed)
    sat = [(1, 5), (2, 6), (3, 7), (4, 8), (0, 8), (1, 5), (0, 7), (1, 8), (2, 9), (1, 2),
           (2, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 3), (1, 4), (2, 5), (3, 6),
           (4, 7), (5, 8), (0, 2), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (0, 5), (1, 6),
           (2, 7), (3, 8), (4, 9), (3, 9), (0, 6), (1, 7), (3, 9)]

    # Create Code Generator object for chosen Satellite
    CodeGen = GoldCode(sat[sat_ind - 1]) # Index starts at zero

    # Generate Prompt code, using estimated phase from Acquisition
    # Numpy array allows the array to be "rolled" (circular shifted)
    # Note: if phase is positive, it will be shifted left (reason for minus in roll)
    codeP = np.array(CodeGen.getCode(1023, samplesPerChip=samples_per_chip))
    codeP = np.roll(codeP, -estimated_phase)

    # Create Early and Late codes, by shifting Prompt code
    codeE = np.roll(codeP, -chip_delay)
    codeL = np.roll(codeP, chip_delay)

    # Return the 3-tuple, containing the phase-delayed CA codes
    return (codeE, codeP, codeL)

def GetMSOfData(millisecondBlockIndex, fileName, fs, estimatedDoppler):
    '''
    # Evan says don't use this function....
    '''

    oneMS = 1*10**(-3)
    samplesPerByte = 2

    # Determine how many bytes equal one millisecond
    bytesPerMS = int((oneMS*fs)/samplesPerByte)

    # Calculate how many bytes to skip
    BytesToSkip = millisecondBlockIndex*bytesPerMS

    # Grab single MS of data, at index requested
    data = IQData()
    data.importFile(fileName, fs, oneMS, BytesToSkip)

    # Will apply estimated doppler frequency shift to data
    t = np.linspace(0, oneMS, data.Nsamples,endpoint=True)

    # Frequency Shift method #1 (used in Matlab version)
    IDataShifted = (data.IData)* np.cos(2 * np.pi* estimatedDoppler * t)
    QDataShifted = data.QData *  np.sin(2 * np.pi* estimatedDoppler * t)

    # Frequency Shift method #2
    #CDataShifted = data.CData*np.exp(1j*2*np.pi*estimatedDoppler*t)
    #IDataShifted = np.real(CDataShifted)
    #QDataShifted = np.imag(CDataShifted)

    return (IDataShifted, QDataShifted)

def MixSignals(CodeE, CodeP, CodeL, SigI, SigQ):

    ImixE = CodeE*SigI
    ImixP = CodeP*SigI
    ImixL = CodeL*SigI

    QmixE = CodeE*SigQ
    QmixP = CodeP*SigQ
    QmixL = CodeL*SigQ

    return (ImixE, ImixP, ImixL, QmixE, QmixP, QmixL)

def SumSignals(ImixE, ImixP, ImixL, QmixE, QmixP, QmixL):
    intIE = np.sum(ImixE)
    intIP = np.sum(ImixP)
    intIL = np.sum(ImixL)

    intQE = np.sum(QmixE)
    intQP = np.sum(QmixP)
    intQL = np.sum(QmixL)

    return (intIE,intIP,intIL, intQE,intQP,intQL)

def PrintCodeTracking(intIE, intIP, intIL, intQE, intQP, intQL, discriminator):
    print()
    print("Integrator results: ")
    print("  In-Phase    Early:  %f" %(intIE**2))
    print("  In-Phase    Prompt: %f" %(intIP**2))
    print("  In-Phase    Late:   %f" %(intIL**2))
    print("  Quadrature  Early:  %f" %(intQE**2))
    print("  Quadrature  Prompt: %f" %(intQP**2))
    print("  Quadrature  Late:   %f" %(intQL**2))
    print("Discriminator results: %f" %(discriminator))

def CodeDiscriminator(BoolCarrierLocked, intIE, intIP, intIL, intQE, intQP, intQL):
    if (BoolCarrierLocked == False):
        discriminator = ((intIE ** 2 + intQE ** 2) - (intIL ** 2 + intQL ** 2)) / ((intIE ** 2 + intQE ** 2) + (intIL ** 2 + intQL ** 2))
    else:
        discriminator = (1/4)*((intIE-intIL)/intIP)

    return discriminator

if __name__ == "__main__":
    main()
 