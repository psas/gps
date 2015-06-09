# GPS Utilities

These might be helpful in debugging or understanding what is happeneing with GPS
signals we're trying to track.

## `constellation.py`

Draw the current local sky with aproximate GPS satellite positions above 5°
altitude. Includes estimated Doppler shifts.

### Example:

Run:

    $ ./constellation.py

Output:

![exmample sky chart](example.png)

    $ #SV, Doppler (Hz), Alt (deg), Az (deg)
    $ 08, -3421, 67, 50
