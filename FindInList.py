import numpy as np
import numba
import pdb

# Was going to use numba, but it seems to be slightly slower with it than without it.
#@numba.autojit
def FindListInList(ListToSearchIn, ListToSearchFor):
    matchIndexList = []
    for bigInd in range(len(ListToSearchIn)-len(ListToSearchFor) + 1):
        curMatch = 1
        for littleInd in range(len(ListToSearchFor)):
            itemMatch = (ListToSearchFor[littleInd] == ListToSearchIn[bigInd + littleInd])
            curMatch = itemMatch & curMatch
        if curMatch:
            matchIndexList.append(bigInd)
    return matchIndexList

def CheckParity(Data24Bits, Parity6Bits, D29, D30):
    ParityMatches = False # Will change to True if parity checks out.

    # Encode all of the data (0 -> +1) and (1 -> -1)
    EncData = EncodeData(Data24Bits)
    EncParity = EncodeData(Parity6Bits)
    EncD29 = EncodeData(D29)
    EncD30 = EncodeData(D30)
    #pdb.set_trace() # Spawn python shell

    print(EncD30)
    # Invert only the data bits (D1-D24) by multiplying with prior D30
    EncData = EncD30*EncData

    # Generate parity matrix, H
    # First 5 rows, same vector but rotated
    hRow = [1,1,1,0,1,1,0,0,0,1,1,1,1,1,0,0,1,1,0,1,0,0,1,0]
    # Last row is different
    hRowLast = [0,0,1,0,1,1,0,1,1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,1]
    # Create matrix
    H = np.array([hRow, np.roll(hRow,1), np.roll(hRow,2), np.roll(hRow,3), np.roll(hRow,4), hRowLast])

    # Multiply the 24 bits of data by each row of the matrix, resulting in 6x24 matrix
    DxH = EncData*H

    # Each of the 6 rows of the resulting matrix will provide a single
    # parity bit by multiplying all non-zero elements together and then
    # multiplying by either D29 or D30 and then decoding
    # the resulting bit.
    D29orD30 = [EncD29, EncD30, EncD29, EncD30, EncD30, EncD29]
    parityBits = []
    for indRow in range(6):
        tmpBit = 1 # Must start out as one
        for indCol in range(24):
            if np.abs(DxH[indRow,indCol]) == 1:
                tmpBit = tmpBit*DxH[indRow,indCol]
        tmpBit = D29orD30[indRow]*tmpBit
        parityBits.append(tmpBit)
    parityBits = np.array(UnencodeData(parityBits), dtype=np.int)

    # Check to see that generated parity matches received parity bits
    if np.array_equal(parityBits, Parity6Bits):
        ParityMatches = True
    return ParityMatches, UnencodeData(EncData)



def EncodeData(UnencodedData):
    # Check whether numpy array or scalar value
    if isinstance(UnencodedData,(np.ndarray,list)):
        DataLength = len(UnencodedData)
        EncodedData = np.zeros(DataLength, dtype=np.int)
        for ind in range(DataLength):
            if int(UnencodedData[ind]) == 0:
                EncodedData[ind] = 1
            elif int(UnencodedData[ind]) == 1:
                EncodedData[ind] = -1
            else:
                print("Error: Unencoded Data contains values other than 0 or 1.")
    else:
        if UnencodedData == 0:
            EncodedData = 1
        elif UnencodedData == 1:
            EncodedData = -1
        else:
            print("Error: Unencoded Data contains values other than 0 or 1.")

    return EncodedData

def UnencodeData(EncodedData):
    # Check whether numpy array or scalar value
    if isinstance(EncodedData,(np.ndarray,list)):
        DataLength = len(EncodedData)
        UnencodedData = np.zeros(DataLength, dtype=np.int)
        for ind in range(DataLength):
            if EncodedData[ind] == 1:
                UnencodedData[ind] = 0
            elif EncodedData[ind] == -1:
                UnencodedData[ind] = 1
            else:
                print(UnencodedData[ind])
                print("Error: Encoded Data contains values other than -1 or 1.")
    else:
        if EncodedData == 1:
            UnencodedData = 0
        elif EncodedData == -1:
            UnencodedData = 1
        else:
            print("Error: Encoded Data contains values other than -1 or 1.")

    return UnencodedData
