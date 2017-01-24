#ifndef DSP_H
#define DSP_H

#include <fftw3.h>

struct nco {
	fftw_complex current;
	fftw_complex rate;
};

void complex_mul(fftw_complex to, fftw_complex a, fftw_complex b);
void complex_conj_mul(fftw_complex to, fftw_complex a, fftw_complex b);
void normalize(fftw_complex v);
void nco_init(struct nco *nco);
void nco_set_rate(struct nco *nco, int sample_rate, double frequency);
void nco_next(struct nco *nco);

#endif /* DSP_H */
