# GPS Experiments

This is a software correlator for GPS. Our primary reference for FFT-based
correlation was [Andrew Holme's homebrew GPS receiver documentation](http://www.holmea.demon.co.uk/GPS/Main.htm), which we
highly recommend for background.

This project is currently the focus of the 2017 ECE capstone team. The Python prototype developed will be used in conjunction with the data generator to 
develop revised hardware, and higher performance algorithms. Once the hardware and software perform adequately, they will be implemented into launch hardware 
for the rocket and OreSat.

# Progress

- [ ] Python Protoype
  - [x] Acquisition
    - [x] Generate C/A Codes
    - [x] Acquire satellite
    - [x] Acquire satellites with Doppler shifts
    - [x] Acquire all satellites in launch data
  - [x] Tracking
    - [x] Lock on to plain carrier signal
    - [x] Lock on to plain code signal
    - [x] Lock on to plain carrier + code signal
    - [x] Lock on to generated GPS satellite data
    - [ ] Lock on to satellite signal from launch data
  - [ ] Navigation 
    - [ ] Interpret almanac data
    - [ ] Use TOW to calculate coarse location
    - [ ] Get precise location using code phase
    - [ ] Track position changes (velocity)
    - [ ] Kalman filter PVT data



# Documentation

To learn more about the theory about how GPS and the software works, you can browse the Jupyter notebooks located in the /notebooks folder. 

# Reading List

These are books about GPS theory that we found helpul while working on the code:

- [A Software-Defined GPS and Galileo Receiver: A Single-Frequency Approach](https://www.bookfinder.com/search/?isbn=9780817643904) by Borre, Akos et.al.: We used this book very extensively since their implementation is similar to what we are trying to do. The book comes with a DVD contaning a (GPL Licensed) MATLAB receiver, and one may notice that our code is very similar in some spots to the MATLAB code. 

- [Understanding GPS: Principles and Applications](https://www.bookfinder.com/search/?isbn=9780890067932) by Kaplan: This book is probably the most approachable to someone who is unfamiliar with GPS. This is our recommended starting point.

- [Fundamentals of Global Positioning System Receivers: A Software Approach](https://www.bookfinder.com/search/?isbn=9780471706472) by Tsui: An extremely helpful book that discusses software implementations of GPS receivers. Both this and Borre complement one another with their own perspectives and approaches.

- [Global Positioning System: Signals, Measurements, and Performance](https://www.bookfinder.com/search/?isbn=9780970954428) by Misra, Enge: A (physically) large book that covers a lot of material.

- [Global Positioning System: Theory and Applications Volume II](https://www.bookfinder.com/search/?&isbn=9781563471070) by Parkinson, Spiker: Does not cover GPS receiver, but has many interesting applications of GPS receiver technology to different problems, including differential GPS, orbit determination, attitude determination, and several more. Very interesting if one has a custom GPS receiver available. 

- Also do not forget [Andrew Holme's homebrew GPS receiver documentation](http://www.holmea.demon.co.uk/GPS/Main.htm) linked above.






