# C GPS Correlator

The C version of the GPS correlator was written before the capstone, and currently is able to acqurire satellites from launch data.

## Build

Requres libfft.

    $ sudo apt-get install libfftw3-dev
    $ make

## Useful commands

Run the soft correlator at one-second intervals over data recorded from
a MAX2769 to the Launch-12 avionics stack. (Assumes you've fetched the
raw
[flightcomputer.log](http://annex.psas.pdx.edu/Launch-12/flightcomputer.log)
and the [psas\_packet](https://github.com/psas/psas_packet) library
source code.)

    .../psas_packet/binary-slice JGPS < flightcomputer.log | split --filter='./read-max | ./soft-correlator 4092000 > $FILE &' --bytes=2046000 --suffix-length=4 --numeric-suffixes - sats/fft

## Sample Data

The C code has been tested with the data logged by KD7LMO. [Original Site](http://www.kd7lmo.net/ground_gnuradio_ota.html) // [Mirror](http://ad7zj.net/kd7lmo/ground_gnuradio_ota.html). More info about the data is below:

The input format is that used by KD7LMO for OTA GPS captures in 2005. KD7LMO's
data is:

 - downconverted from 1575.42 MHz,
 - quadrature sampled at 4MSPS,
 - encoded Intel endian, 32-bit floating point values in I, Q interleaved

These datafiles should have the following sats in them:

 File Name                         | Capture Info            | Sats, remarks
 --------------------------------- | ----------------------- | -------------
 `gps_4m_complex.dat`              | 0008 UTC on 26 Mar 2005 | SV 1, 3, 14, 15, 19, 21, 22, 25 and WAAS 47
 `gps_4m_complex.21Apr2005.dat`    | 0522 UTC on 21 Apr 2005 | SV 3, 8, 13, 16, 19, 20, 23, 27 and WAAS 35 and 47
 `gps_4msps_complex.12Sep2005.dat` | A 60 second capture     | Snapshot contains at least one set of ephemeris data.

### Other data samples

For another source of raw GPS samples, try:
- [SoftGPS Project](http://kom.aau.dk/project/softgps/data.php)
- [(1.2GB) gnss-sdr project @ Sourceforge](http://sourceforge.net/projects/gnss-sdr/files/data/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar.gz/download)
- [(7+GB) From setiQuest SigBlips archive.](http://setiquest.org/setidata/data3/download/2010-10-08-GPS-27_1575_1/) See [here](http://www.acasper.org/2011/11/07/gps-signal-analysis/) for analysis of this data.
- [(3.2GB) 3 minutes of SV26 from setiQuest SigBlips archive](http://setiquest.org/setidata/data1/download/2010-01-22-gps-prn26)
