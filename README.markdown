# GPS Experiments

This is a software correlator for GPS. Our primary reference for FFT-based
correlation was Andrew Holme's homebrew GPS receiver documentation, which we
highly recommend for background:

> <http://www.holmea.demon.co.uk/GPS/Main.htm>

## Sample Data

The input format is that used by KD7LMO for OTA GPS captures in 2005. KD7LMO's
data is:

 - downconverted from 1575.42 MHz,
 - quadrature sampled at 4MSPS,
 - encoded Intel endian, 32-bit floating point values in I, Q interleaved

Original site: <http://www.kd7lmo.net/ground_gnuradio_ota.html>
Mirrored at: <http://ad7zj.net/kd7lmo/ground_gnuradio_ota.html>

These datafile should have the following sats in them:

 File Name                         | Capture Info            | Sats, remarks
 --------------------------------- | ----------------------- | -------------
 `gps_4m_complex.dat`              | 0008 UTC on 26 Mar 2005 | SV 1, 3, 14, 15, 19, 21, 22, 25 and WAAS 47
 `gps_4m_complex.21Apr2005.dat`    | 0522 UTC on 21 Apr 2005 | SV 3, 8, 13, 16, 19, 20, 23, 27 and WAAS 35 and 47
 `gps_4msps_complex.12Sep2005.dat` | A 60 second capture     | Snapshot contains at least one set of ephemeris data.

For another source of raw GPS samples, try:
- <http://kom.aau.dk/project/softgps/data.php>.
- <http://sourceforge.net/projects/gnss-sdr/files/data/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar.gz/download> (1.2GB) From http://www.gnss-sdr.org/ project.
- <http://setiquest.org/setidata/data3/download/2010-10-08-GPS-27_1575_1/> (7+GB) From setiQuest SigBlips archive.  See http://www.acasper.org/2011/11/07/gps-signal-analysis/ for analysis of this data.
- <http://setiquest.org/setidata/data1/download/2010-01-22-gps-prn26> (3.2GB) 3 minutes of SV26 from setiQuest SigBlips archive.



