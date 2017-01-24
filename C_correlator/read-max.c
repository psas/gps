#include <stdint.h>
#include <stdio.h>

static float sign_magnitude(unsigned sign, unsigned magnitude)
{
	float value = magnitude ? 1 : 1.0/3.0;
	return sign ? -value : value;
}

int main(void)
{
	unsigned samplecount = 0;
	unsigned isigncount = 0;
	unsigned imagcount = 0;
	unsigned qsigncount = 0;
	unsigned qmagcount = 0;

	while(1)
	{
		uint8_t buf;
		if(fread(&buf, sizeof(uint8_t), 1, stdin) != 1)
			break;

		unsigned int j;
		for(j = 0; j < 2; ++j)
		{
			/* Each nibble contains, in order from MSB to LSB:
			 * - in-phase (real) part followed by quadrature-phase (imaginary) part
			 * - older sample followed by newer sample */
			unsigned imag  = (buf >> (8 - j * 4 - 1)) & 1;
			unsigned isign = (buf >> (8 - j * 4 - 2)) & 1;
			unsigned qmag  = (buf >> (8 - j * 4 - 3)) & 1;
			unsigned qsign = (buf >> (8 - j * 4 - 4)) & 1;
			float sample[2] = {
				sign_magnitude(isign, imag),
				sign_magnitude(qsign, qmag),
			};
			fwrite(sample, sizeof(float), 2, stdout);

			++samplecount;
			if(isign) ++isigncount;
			if(imag)  ++imagcount;
			if(qsign) ++qsigncount;
			if(qmag)  ++qmagcount;
		}
	}

	fprintf(stderr, "frequency of 1-bits: i-sign %.1f%%, i-mag %.1f%%, q-sign %.1f%%, q-mag %.1f%%\n",
		100.0 * isigncount / samplecount,
		100.0 * imagcount / samplecount,
		100.0 * qsigncount / samplecount,
		100.0 * qmagcount / samplecount
		);

	return 0;
}
