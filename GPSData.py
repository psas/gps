'''
This module contains tools to import raw GPS data for
use with the soft correlator.


'''
import numpy as np

class IQData:
    
    IData = []
    QData = []
    CData = []
    
    def _byteToIQPairs(self, TheByte ):
        IQPairs = []

        # This code reads each of the four pairs of bits from the byte 
        # and determines the sign and magnitude. Then it returns a list 
        # containing two pairs of IQ data as floating point [I1,Q1,I2,Q2].
        # For magnitude: a bit value of 1 means mag 1, 0 means mag 1/3
        # For sign: a bit value of 1 means negative, 0 means positive
        # This interpretation was taken by the sample code provided
        # in the PSAS Launch12 github repo (example was provided in C)
        #
        # f_s = 4.092 MHz (sampling rate of raw signal)

        IMag1 = (TheByte >> 7) & (0b00000001)
        ISign1 = (TheByte >> 6) & (0b00000001)
        I1 = 1.0 if (IMag1 == 1) else 1.0/3.0
        I1 = -I1 if (ISign1 == 1) else I1
        IQPairs.append(I1)

        QMag1 = (TheByte >> 5) & (0b00000001)
        QSign1 = (TheByte >> 4) & (0b00000001)
        Q1 = 1.0 if (QMag1 == 1) else 1.0/3.0
        Q1 = -Q1 if (QSign1 == 1) else Q1
        IQPairs.append(Q1)    

        IMag2 = (TheByte >> 3) & (0b00000001)
        ISign2 = (TheByte >> 2) & (0b00000001)
        I2 = 1.0 if (IMag2 == 1) else 1.0/3.0
        I2 = -I2 if (ISign2 == 1) else I2
        IQPairs.append(I2)    

        QMag2 = (TheByte >> 1) & (0b00000001)
        QSign2 = (TheByte >> 0) & (0b00000001)
        Q2 = 1.0 if (QMag2 == 1) else 1.0/3.0
        Q2 = -Q2 if (QSign2 == 1) else Q2
        IQPairs.append(Q2)

        return IQPairs 

    def _complexData(self):
        #Returns array of complex data
        self.CData = np.zeros(len(self.IData), dtype=np.complex)

        for d in range(len(self.IData)):
            self.CData[d] = self.IData[d]  + self.QData[d] * 1j  # Complex data

        return

    def importFile(self, path):
        print("Opening a file.")
        fHandle = open(path,'rb')
        print("File handle is: %d." % (fHandle.fileno()))
        
        # Read file one byte at a time, extract the two 
        # IQ pairs, and store in array, after conversion to float.
        # Will initially read enough samples for ~20 ms of data
        fs = 4.092*10**6 # Sampling Frequency [Hz]
        Ts = 1/fs # Sampling Period [s]
        NumberOfMilliseconds = 1
        SampleLength = NumberOfMilliseconds*10**(-3) # Sample length in 1ms multiples
        StartingByte = 0 # Can change this if we want to discard initial samples
        TotalSamples = int(np.ceil(SampleLength/Ts)) 
        TotalBytes = int(np.ceil(TotalSamples/2))
        print("Total Samples to read: %d"%(TotalSamples))
        print("Total Bytes read: %d." %(TotalBytes))
        print("Which equals %d IQ pairs." %(TotalBytes*2))
        print("Sample Length: %f seconds." %(TotalBytes*2*Ts))
        
        i = StartingByte
        SingleByte = fHandle.read(1)
        self.IData = []
        self.QData = []
        while SingleByte != "":
            IQPairs = self._byteToIQPairs(ord(SingleByte))
            self.IData.append(IQPairs[0])
            self.IData.append(IQPairs[2])
            self.QData.append(IQPairs[1])
            self.QData.append(IQPairs[3])
            #print("I: %f, Q: %f ." % (IQPairs[0], IQPairs[1]))
            #print("I: %f, Q: %f ." % (IQPairs[2], IQPairs[3]))
            
            i += 1
            if i >= (TotalBytes - StartingByte):
                break
            SingleByte = fHandle.read(1)
        
        fHandle.close()
        print("File is now closed.")

        self._complexData()
