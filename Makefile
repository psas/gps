OPTFLAGS = -O3 -flto
CFLAGS = -g -Wall $(OPTFLAGS)
LDFLAGS = $(OPTFLAGS)

all: soft-correlator read-max read-s16 make-prn

soft-correlator: LDLIBS = -lm -lfftw3
soft-correlator: soft-correlator.o dsp.o prn.o

read-max: read-max.o

read-s16: read-s16.o

make-prn: make-prn.o prn.o

clean:
	rm -f *.o
	rm -f soft-correlator read-max read-s16 make-prn
