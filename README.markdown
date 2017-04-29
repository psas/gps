# GPS Experiments

This is a software correlator for GPS. Our primary reference for FFT-based
correlation was [Andrew Holme's homebrew GPS receiver documentation](http://www.holmea.demon.co.uk/GPS/Main.htm), which we
highly recommend for background.

This project is currently the focus of the 2017 ECE capstone team. The first objective is to create a Python prototype correlator. If time allows, the code will be ported to an embedded Rust implementation, and flown on the rocket as well as OreSat.

# Progress

- [ ] Python Protoype
  - [x] Acquisition
    - [x] Generate C/A Codes
    - [x] Acquire satellite
    - [x] Acquire satellites with Doppler shifts
    - [x] Acquire all satellites in launch data
  - [ ] Tracking
    - [ ] Lock on to plain carrier signal
    - [ ] Lock on to plain code signal
    - [ ] Lock on to plain carrier + code signal
    - [ ] Lock on to generated GPS satellite data
    - [ ] Lock on to satellite signal from launch data
  - [ ] Navigation 
    - [ ] Interpret almanac data
    - [ ] Use TOW to calculate coarse location
    - [ ] Get precise location using code phase
    - [ ] Track position changes (velocity)
    - [ ] Kalman filter PVT data
- [ ] Embedded Rust 
 

# Documentation

To learn more about the theory about how GPS and the software works, you can browse the Jupyter notebooks located in the /notebooks folder. 

## Sample Data

### Python Code

The python code is primarily tested using the GPS data recorded from L-12. The files are located in the /resources/ directory. More info can be found in the Launch 12 repo.

### C Code

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



