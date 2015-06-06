OPTFLAGS = -O3 -flto
CFLAGS = -g -Wall $(OPTFLAGS)
LDFLAGS = $(OPTFLAGS)

all: soft-correlator read-max read-s16

soft-correlator: LDLIBS = -lm -lfftw3
soft-correlator: soft-correlator.o dsp.o prn.o

read-max: read-max.o

read-s16: read-s16.o
