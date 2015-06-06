#include <math.h>
#include "dsp.h"

void complex_mul(fftw_complex to, fftw_complex a, fftw_complex b)
{
	double real = a[0] * b[0] - a[1] * b[1];
	double imag = a[1] * b[0] + a[0] * b[1];
	to[0] = real;
	to[1] = imag;
}

void complex_conj_mul(fftw_complex to, fftw_complex a, fftw_complex b)
{
	double real = a[0] * b[0] + a[1] * b[1];
	double imag = a[1] * b[0] - a[0] * b[1];
	to[0] = real;
	to[1] = imag;
}

void normalize(fftw_complex v)
{
	double mag = sqrt(v[0] * v[0] + v[1] * v[1]);
	v[0] /= mag;
	v[1] /= mag;
}

void nco_init(struct nco *nco)
{
	nco->current[0] = 1;
	nco->current[1] = 0;
	nco->rate[0] = 1;
	nco->rate[1] = 0;
}

void nco_set_rate(struct nco *nco, int sample_rate, double frequency)
{
	nco->rate[0] = cos(frequency * 2 * M_PI / sample_rate);
	nco->rate[1] = sin(frequency * 2 * M_PI / sample_rate);
}

void nco_next(struct nco *nco)
{
	complex_mul(nco->current, nco->current, nco->rate);
}
