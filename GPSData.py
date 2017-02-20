'''
This module contains tools to import raw GPS data for
use with the soft correlator.


'''
import numpy as np

class IQData:
    
    IData = []
    QData = []
    CData = []
    
    sampleFreq = 0
    sampleTime = 0
    Nsamples   = 0

    def _byteToIQPairs(self, TheByte ):
    
        # This code reads each of the four pairs of bits from the byte 
        # and determines the sign and magnitude. Then it returns a list 
        # containing two pairs of IQ data as floating point [I1,Q1,I2,Q2].
        # For magnitude: a bit value of 1 means mag 1, 0 means mag 1/3
        # For sign: a bit value of 1 means negative, 0 means positive
        # This interpretation was taken by the sample code provided
        # in the PSAS Launch12 github repo (example was provided in C)
 
        IMag1 = (TheByte >> 7) & (0b00000001)
        ISign1 = (TheByte >> 6) & (0b00000001)
        I1 = 1.0 if (IMag1 == 1) else 1.0/3.0
        I1 = -I1 if (ISign1 == 1) else I1

        QMag1 = (TheByte >> 5) & (0b00000001)
        QSign1 = (TheByte >> 4) & (0b00000001)
        Q1 = 1.0 if (QMag1 == 1) else 1.0/3.0
        Q1 = -Q1 if (QSign1 == 1) else Q1

        IMag2 = (TheByte >> 3) & (0b00000001)
        ISign2 = (TheByte >> 2) & (0b00000001)
        I2 = 1.0 if (IMag2 == 1) else 1.0/3.0
        I2 = -I2 if (ISign2 == 1) else I2

        QMag2 = (TheByte >> 1) & (0b00000001)
        QSign2 = (TheByte >> 0) & (0b00000001)
        Q2 = 1.0 if (QMag2 == 1) else 1.0/3.0
        Q2 = -Q2 if (QSign2 == 1) else Q2

        return (I1, I2, Q1, Q2) 

    def _complexData(self):
        #Returns array of complex data
        self.CData = np.zeros(len(self.IData), dtype=np.complex)
        self.CData = np.array(self.IData) + np.array(self.QData) * 1j  # Complex data
        return

    def _timeVector(self, bytesToSkip, Ts, seconds):
        #Generates time vector of requested data.
        #Will assume that t=0 for the start of file. 
        
        # Each byte has 2 IQ pairs, so 2*Ts seconds will have elapsed.
        StartingTime = bytesToSkip*2*Ts
        
        EndingTime = StartingTime + seconds
        
        self.t = np.linspace(StartingTime,EndingTime,self.Nsamples)

    def importFile(self, path, fs, seconds, bytesToSkip):
        '''
        imports IQ Data from a file
        fs is sampling frequency
        seconds is the length of data in seconds

        '''
        print("Opening a file.")
        fHandle = open(path,'rb')
        print("File handle is: %d." % (fHandle.fileno()))
        
        self.sampleFreq = fs
        self.sampleTime = seconds

        # Read file one byte at a time, extract the two 
        # IQ pairs, and store in array, after conversion to float.
        # Will initially read enough samples for ~20 ms of data
        Ts = 1/fs # Sampling Period [s]
        SampleLength = seconds # Sample length in 1ms multiples
        StartingByte = bytesToSkip # Can change this if we want to discard initial samples
        TotalSamples = int(np.ceil(SampleLength/Ts)) 
        self.Nsamples = TotalSamples
        TotalBytes = int(np.ceil(TotalSamples/2))
        print("Total Samples to read: %d"%(TotalSamples))
        print("Total Bytes read: %d." %(TotalBytes))
        print("Which equals %d IQ pairs." %(TotalBytes*2))
        print("Sample Length: %f seconds." %(TotalBytes*2*Ts))
        
        i = 0
        # Go to requested starting position
        fHandle.seek(StartingByte)
        
        # Read a single byte to get started
        SingleByte = fHandle.read(1)
        self.IData = []
        self.QData = []
        
        # Loop until reach EOF (will also break of exceeds requested size)
        while SingleByte != "":
            I1, I2, Q1, Q2 = self._byteToIQPairs(ord(SingleByte))
            self.IData.extend((I1, I2))
            self.QData.extend((Q1, Q2))
            i += 1 # Increment current position
            if (i >= TotalBytes):
                break # Stop reading bytes if will exceed requested amount of samples
            SingleByte = fHandle.read(1)
        
        fHandle.close()
        print("File is now closed.")

        self._complexData()
        self._timeVector(bytesToSkip, Ts, seconds)
