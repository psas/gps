OPTFLAGS = -O3 -flto
CFLAGS = -g -Wall $(OPTFLAGS)
LDFLAGS = $(OPTFLAGS)
LDLIBS = -lm -lfftw3

all: soft-correlator

soft-correlator: soft-correlator.o dsp.o prn.o
