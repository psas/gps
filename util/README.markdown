# GPS Utilities

These might be helpful in debugging or understanding what is happening with GPS
signals we're trying to track.

## `constellation.py`

This draws the current local sky with approximate GPS satellite positions above 5°
altitude. Includes estimated Doppler shifts.

### Requirements

Install matplotlib (`sudo apt-get install python-matplotlib`, or `pip install matplotlib`) and [pyephem](http://rhodesmill.org/pyephem/) (`pip install pyephem`)

Download GPS orbit data from [CelesTrak](https://celestrak.com/NORAD/elements/):

    $ ./update-gps.sh

### Example:

Run:

    $ ./constellation.py

Output:

![exmample sky chart](example.png)


    #SV, Doppler (Hz), Alt (deg), Az (deg)
    13,  3195, 23.3, 216.5
    11,  3097,  5.8,  39.0
    28,  1581, 43.4,  76.3
    17,   359, 80.6,  80.1
    12, -2825,  5.6, 277.7
    15,  1994, 25.7, 255.4
    01,  1797, 19.3,  44.4
    24, -2592, 31.9, 309.6
    30,  3378, 13.4, 141.2
    06, -3321, 21.1, 159.8

