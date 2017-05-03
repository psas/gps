'''
This reads the binary file that is generated from gps-sdr-sim (8-bit setting)
and outputs a file with the 2-bit IQ (sign/mag) format that we would expect from
the output of the max2769.

More details about the 2-bit data we are working with:
https://github.com/psas/Launch-12/tree/gh-pages/data/GPS

More details regarding the 3rd-party GPS simulation tool:
https://github.com/osqzss/gps-sdr-sim

USAGE:
        ./8bitToMax.py InputBinaryFile OutputBinaryFile

Usage Example:
        ./8bitToMax.py 8bitIQ.bin 2bitIQ.max
'''

import argparse
import numpy as np
import time

parser = argparse.ArgumentParser(
        description='Converts 8bit gps-sdr-sim binary to max2769 2-bit binary.',
        usage='./8bitToMax.py InputBinaryFile OutputBinaryFile'
        )
parser.add_argument('EightBit')
parser.add_argument('Max2769')
args = parser.parse_args()

SimData = np.fromfile(args.EightBit, dtype=np.int8, count=-1,sep='')

TwoBitArrayLen = int(np.ceil(len(SimData)/4))
MaxData = np.zeros(TwoBitArrayLen, dtype=np.dtype('<b'))

posInByte = 7
for byteInd, iqByte in enumerate(SimData):
    # Get magnitude. It looks like the max value is 64.
    # Will use (0 <= val <= 31) for mag to be 0
    # and (val > 31) to be a mag of 1.
    # Our software will treat 0's as 1.0/3.0 and 1's as 1.0
    if iqByte > 31:
        magBit = 1
    else:
        magBit = 0
    MaxData[int(byteInd//4)] = ((magBit << posInByte) | MaxData[int(byteInd//4)])
    posInByte -= 1

    # Get sign. Since 2s compliment, most significant bit determines the
    # sign. A value of 1 means sign is negative (in both 2s compliment, and
    # the two bit sign/mag max data).
    signBit = (iqByte >> 7) & (0b00000001)
    MaxData[int(byteInd//4)] = ((signBit << posInByte) | MaxData[int(byteInd//4)])
    posInByte -= 1

    if posInByte <= 0:
        posInByte = 7

with open(args.Max2769, 'wb') as fMax:
    MaxData.tofile(fMax)
