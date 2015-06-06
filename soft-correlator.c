/*
 * Copyright (C) 2011 Jamey Sharp
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301 USA.
 */

#include <fftw3.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "dsp.h"
#include "prn.h"

#define TRACE 0

struct signal_strength {
	double snr;
	double doppler;
	double phase;
	double clock_error;
};

static double sign_magnitude(unsigned sign, unsigned magnitude)
{
	double value = magnitude ? 1 : 1.0/3.0;
	return sign ? -value : value;
}

unsigned samplecount;
unsigned isigncount;
unsigned imagcount;
unsigned qsigncount;
unsigned qmagcount;

static unsigned int read_samples(struct nco *center_freq, fftw_complex *data, unsigned int data_len)
{
	unsigned int i = 0;
	while(i < data_len)
	{
		uint8_t buf;
		unsigned int j;
		if(fread(&buf, sizeof(uint8_t), 1, stdin) != 1)
			break;
		for(j = 0; j < 2; ++j)
		{
			/* Each nibble contains, in order from MSB to LSB:
			 * - in-phase (real) part followed by quadrature-phase (imaginary) part
			 * - older sample followed by newer sample */
			unsigned imag  = (buf >> (8 - j * 4 - 1)) & 1;
			unsigned isign = (buf >> (8 - j * 4 - 2)) & 1;
			unsigned qmag  = (buf >> (8 - j * 4 - 3)) & 1;
			unsigned qsign = (buf >> (8 - j * 4 - 4)) & 1;
			data[i][0] = sign_magnitude(isign, imag);
			data[i][1] = sign_magnitude(qsign, qmag);

			++samplecount;
			if(isign) ++isigncount;
			if(imag)  ++imagcount;
			if(qsign) ++qsigncount;
			if(qmag)  ++qmagcount;

			complex_mul(data[i], data[i], center_freq->current);
			nco_next(center_freq);
			if(++i >= data_len)
				break;
		}
	}
	return i;
}

static void demod(unsigned int sample_freq, double clock_error, fftw_complex *data, unsigned int data_len, int sv, double doppler, double code_phase, unsigned int delay_samples)
{
	double chips_per_sample;
	unsigned int i;
	int ready = 0;
	struct nco nco;
	fftw_complex prompt_sum = { 0, 0 };
	double early_sum = 0, late_sum = 0;

	nco_init(&nco);
	nco_set_rate(&nco, sample_freq, -doppler);
	chips_per_sample = (clock_error + 1023e3 * (1 + doppler / 1575.42e6)) / sample_freq;
	code_phase += delay_samples * chips_per_sample;

	if(TRACE)
		printf("# navigation data from sv %d with Doppler shift %f\n", sv, doppler);
	for(i = 0; i < data_len; ++i)
	{
		fftw_complex result;
		int chip = (int) code_phase % 1023;
		int prompt = cacode(chip, sv) ? 1 : -1;
		int early = cacode((int) (code_phase - 0.5) % 1023, sv) ? 1 : -1;
		int late = cacode((int) (code_phase + 0.5) % 1023, sv) ? 1 : -1;
		complex_mul(result, data[i], nco.current);
		prompt_sum[0] += result[0] * prompt;
		prompt_sum[1] += result[1] * prompt;
		early_sum += result[0] * early;
		late_sum += result[0] * late;

		nco_next(&nco);
		code_phase += chips_per_sample;

		/* Sample the data signal at rising edge of the start of
		 * the code sequence. */
		if(chip != 0)
			ready = 1;
		else if(ready)
		{
			double phase_error = 0, code_phase_error = 0;
			if(fabs(prompt_sum[0]) >= 1)
			{
				fftw_complex tmp;
				phase_error = atan(prompt_sum[1] / prompt_sum[0]);
				tmp[0] = cos(-phase_error);
				tmp[1] = sin(-phase_error);
				complex_mul(nco.current, nco.current, tmp);

				/* Keep nco unit-length so it's only a
				 * rotation. */
				normalize(nco.current);

				doppler += phase_error * (1000 / (2 * M_PI) / 100);
				nco_set_rate(&nco, sample_freq, -doppler);
				chips_per_sample = (clock_error + 1023e3 * (1 + doppler / 1575.42e6)) / sample_freq;
			}

			if(fabs(early_sum) >= 1 || fabs(late_sum) >= 1)
			{
				code_phase_error = 0.5 - fabs(early_sum) / (fabs(early_sum) + fabs(late_sum));
				code_phase += code_phase_error / 10;
			}

			if(TRACE)
				printf("%f\t%f\t%f\t%f\t%f\t%f\n",
					i * 1000.0 / sample_freq,
					prompt_sum[0], prompt_sum[1],
					phase_error, doppler,
					code_phase_error);

			prompt_sum[0] = prompt_sum[1] = 0;
			early_sum = late_sum = 0;
			ready = 0;

			/* Keep code phase in a reasonable range so it
			 * doesn't lose precision on the low bits. */
			code_phase -= 1023;
		}
	}
	if(TRACE)
		printf("\n");
}

static void update_stats(struct signal_strength *stats, double bin_width, int shift, double phase, double snr_0, double snr_1, double snr_2)
{
	double shift_correction;
	/* ignore this sample if it is not a local peak */
	if(snr_0 > snr_1 || snr_2 > snr_1)
		return;
	/* take only the highest peak */
	if(snr_1 <= stats->snr)
		return;

	/* do a weighted average of the three points around this peak */
	shift_correction = (snr_2 - snr_0) / (snr_0 + snr_1 + snr_2);

	stats->snr = snr_1;
	stats->doppler = (shift + shift_correction) * bin_width;
	stats->phase = phase;
}

static struct signal_strength check_satellite(unsigned int sample_freq, fftw_complex *data_fft, unsigned int data_fft_len, fftw_complex *check, unsigned int check_len, int sv)
{
	struct signal_strength stats;
	const unsigned int len = sample_freq / 1000;
	const unsigned int fft_len = len / 2 + 1;
	fftw_complex *prod = fftw_malloc(sizeof(fftw_complex) * len);
	void *ca_buf = fftw_malloc(sizeof(fftw_complex) * fft_len);
	double *ca_samples = ca_buf;
	fftw_complex *ca_fft = ca_buf;
	const double samples_per_chip = sample_freq / 1023e3;
	const int max_shift = 15000 * data_fft_len / sample_freq;
	const double bin_width = (double) sample_freq / data_fft_len;
	double snr_1 = 0, snr_2 = 0, best_phase_1 = 0;
	double max_pwr, best_phase;
	unsigned int i;
	int shift;
	fftw_plan fft = fftw_plan_dft_r2c_1d(len, ca_samples, ca_fft, FFTW_ESTIMATE | FFTW_DESTROY_INPUT);
	fftw_plan ifft = fftw_plan_dft_1d(len, prod, prod, FFTW_BACKWARD, FFTW_ESTIMATE | FFTW_DESTROY_INPUT);
	fftw_complex *check_fft = fftw_malloc(sizeof(fftw_complex) * check_len);
	fftw_plan check_plan = fftw_plan_dft_1d(check_len, check_fft, check_fft, FFTW_FORWARD, FFTW_ESTIMATE | FFTW_DESTROY_INPUT);

	for(i = 0; i < len; ++i)
		ca_samples[i] = cacode((int) (i / samples_per_chip), sv) ? 1 : -1;

	fftw_execute(fft);
	fftw_destroy_plan(fft);

	if(TRACE)
		printf("# SV %d correlation\n", sv);
	stats.snr = 0;
	for(shift = -max_shift; shift <= max_shift; ++shift)
	{
		const double doppler = shift * bin_width;
		double tot_pwr = 0, snr;
		for(i = 0; i < len / 2; ++i)
		{
			complex_mul(prod[i], data_fft[(i * (data_fft_len / len) + shift + data_fft_len) % data_fft_len], ca_fft[i]);
			complex_conj_mul(prod[len - 1 - i], data_fft[((len - 1 - i) * (data_fft_len / len) + shift + data_fft_len) % data_fft_len], ca_fft[i + 1]);
		}

		fftw_execute(ifft);

		max_pwr = best_phase = 0;
		for(i = 0; i < len; ++i)
		{
			double pwr = prod[i][0] * prod[i][0] + prod[i][1] * prod[i][1];
			double phase = i * (1023.0 / len);
			if(TRACE)
				printf("%f\t%f\t%f\n", doppler, phase, pwr);
			if(pwr > max_pwr)
			{
				max_pwr = pwr;
				best_phase = phase;
			}
			tot_pwr += pwr;
		}

		snr = max_pwr / (tot_pwr / len);
		update_stats(&stats, bin_width, shift - 1, best_phase_1, snr_2, snr_1, snr);
		if(TRACE)
			printf("# best for doppler %f: code phase %f, S/N %f\n", doppler, best_phase, snr);

		snr_2 = snr_1;
		snr_1 = snr;
		best_phase_1 = best_phase;
	}
	update_stats(&stats, bin_width, max_shift, best_phase_1, snr_2, snr_1, 0);
	if(TRACE)
		printf("\n");

	/* Now estimate sample-clock error using a second, shorter,
	 * training pass.
	 *
	 * The quick extra pass provides two benefits:
	 *
	 * - Initializes the code-tracking loop with an estimate of how
	 *   much the receiver's clock is drifting relative to the
	 *   atomic clocks on the GPS satellites.
	 *
	 * - Provides a very good heuristic about whether there's
	 *   actually a satellite there to track.
	 */
	for(i = 0; i < check_len; ++i)
	{
		fftw_complex tmp;
		tmp[0] = cos(-stats.doppler * 2 * M_PI * i / sample_freq);
		tmp[1] = sin(-stats.doppler * 2 * M_PI * i / sample_freq);
		complex_mul(check_fft[i], check[i], tmp);
	}

	fftw_execute(check_plan);
	fftw_destroy_plan(check_plan);

	for(i = 0; i < check_len; ++i)
		check_fft[i][1] = -check_fft[i][1];
	for(i = 0; i < len / 2; ++i)
	{
		complex_mul(prod[i], check_fft[i * (check_len / len)], ca_fft[i]);
		complex_conj_mul(prod[len - 1 - i], check_fft[(len - 1 - i) * (check_len / len)], ca_fft[i + 1]);
	}

	fftw_execute(ifft);

	max_pwr = best_phase = 0;
	for(i = 0; i < len; ++i)
	{
		double pwr = prod[i][0] * prod[i][0] + prod[i][1] * prod[i][1];
		double phase = i * (1023.0 / len);
		if(pwr > max_pwr)
		{
			max_pwr = pwr;
			best_phase = phase;
		}
	}

	stats.clock_error = (best_phase - stats.phase) * sample_freq / data_fft_len - 1023e3 * (1 + stats.doppler / 1575.42e6);
	const double ambig = 1023.0 * sample_freq / data_fft_len;
	stats.clock_error -= lround(stats.clock_error / ambig) * ambig;

	fftw_free(check_fft);
	fftw_destroy_plan(ifft);
	fftw_free(ca_buf);
	fftw_free(prod);
	return stats;
}

int main()
{
	const unsigned int sample_freq = 4092000;
	struct nco center_freq;
	unsigned int training1_len = sample_freq * 10 / 1000;
	unsigned int training2_len = sample_freq * 5 / 1000;
	unsigned int training_len = training1_len + training2_len;
	fftw_complex *training = fftw_malloc(sizeof(fftw_complex) * training_len);
	fftw_complex *training2 = training + training1_len;
	unsigned int data_len = sample_freq * 2;
	fftw_complex *data = fftw_malloc(sizeof(fftw_complex) * data_len);
	struct signal_strength signals[MAX_SV];
	int i;
	double clock_error_sum = 0;
	unsigned int visible_satellites = 0;
	fftw_plan training_plan = fftw_plan_dft_1d(training1_len, training, training, FFTW_FORWARD, FFTW_ESTIMATE | FFTW_DESTROY_INPUT);

	nco_init(&center_freq);
	nco_set_rate(&center_freq, sample_freq, 0);

	if(read_samples(&center_freq, training, training_len) < training_len)
	{
		fprintf(stderr, "couldn't read %u input samples needed for training\n", training_len);
		exit(EXIT_FAILURE);
	}
	fftw_execute(training_plan);
	fftw_destroy_plan(training_plan);

	for(i = 0; i < training1_len; ++i)
	{
		/* precompute the complex conjugate of the training FFT */
		training[i][1] = -training[i][1];
	}

	data_len = read_samples(&center_freq, data, data_len);

	printf("# frequency of 1-bits: i-sign %.1f%%, i-mag %.1f%%, q-sign %.1f%%, q-mag %.1f%%\n",
		100.0 * isigncount / samplecount,
		100.0 * imagcount / samplecount,
		100.0 * qsigncount / samplecount,
		100.0 * qmagcount / samplecount
		);

	for(i = 0; i < MAX_SV; ++i)
		signals[i] = check_satellite(sample_freq, training, training1_len, training2, training2_len, i + 1);

	printf("# SV, S/N ratio, doppler shift (Hz), code phase (chips), sample clock error (chips/s)\n");
	for(i = 0; i < MAX_SV; ++i)
	{
		if(fabs(signals[i].clock_error) < 30)
		{
			printf("%c %d\t%f\t%f\t%f\t%f\n", fabs(signals[i].clock_error) < 30 ? '*' : ' ', i + 1,
				signals[i].snr, signals[i].doppler, signals[i].phase, signals[i].clock_error);
			clock_error_sum += signals[i].clock_error;
			++visible_satellites;
		}
	}
	printf("# %u satellites in view; average clock error %f chips/s\n", visible_satellites, clock_error_sum / visible_satellites);
	printf("\n");

	for(i = 0; i < MAX_SV; ++i)
		if(fabs(signals[i].clock_error) < 30)
			demod(sample_freq, clock_error_sum / visible_satellites, data, data_len, i + 1, signals[i].doppler, signals[i].phase, training_len);

	fftw_free(data);
	fftw_free(training);
	fftw_cleanup();
	exit(EXIT_SUCCESS);
}
