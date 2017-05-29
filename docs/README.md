# GPS Docs

The files in this folder are intended to give a comprehensive overview of the development and usage of the SDR GPS reciever. The documentation assumes a certain level of technical knowledge at points, so it may be worth brushing up on Fourier analysis, and signal processing concepts before digging in. 

# Setup

You will need to download the Launch 12 data, and a generated data file, and put them in /resources before getting started. 

Download and install Python3, and then use pip to install numpy. The docs are viewable on GitHub, but if you want to edit the notebooks to gain a better understanding, you will need Jupyter notebook.

# Table of Contents

The proposed contents of this folder are listed below. Each section is best read after the ones preceding it. Some sections are still a work in progress.

- README 
- 1.GoldCodes
- 2.Acquisition 
- 3.Carrier Tracking
- 4.Code Tracking
- 5.Navigation Data
- 6.Pseudoranges
- A.Generating Data
- B.Using the prototype
- C.Additional work

# GPS Signal Overview

The goal of the receiver at this stage is to obtain a pseudorange, the receivers location on the Earth. This is possible by listening to the GPS satellite network, which continuously transmits the position and time of a data frame transmission. Using this information, the reciever can find the distance between itself, and at least 4 satellites to triangulate its location.

## Data

The data frames being sent by each of the satellites are binary phase shift key (BPSK) modulated. All that really means is that digital 1s and 0s cause the signal to "flip over", or more precisely they shift phase by 180 degrees. These can be represented mathematically by a 1 or -1 multiplication. 50 data bits are transmitted per second. 

## CDMA

All ~30 of the GPS satellites use the same frequency (1575.42 MHz) for commmunication. Code division multiple access (CDMA) is used to keep the signals from each satellite apart. Each satellite is assinged a pseudo-random sequence of 1s and -1s called chips. Unlike bits, they only exist for channel access, and carry no information on their own. The chip sequence is also called a Gold Code, and is 1023 chips long. 

Gold Codes described in more detail in chapter 1. 

## L1 Carrier

The $Data * Chips$ signal travels on the GPS L1 frequency of 1575.42 MHz. There are other frequencies, but they are out of scope for this project. The core part of a GPS receiver is its trakcing loops. These interlocked loops track the carrier signal as it Doppler shifts, and the Gold Code as it drifts out of phase. 

If these two loops are locked, the code and carrier can be cancelled out, leaving the data bits behind. From the bits, we can get a location for the receiver. 