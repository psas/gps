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
