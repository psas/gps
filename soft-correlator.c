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

static unsigned int read_samples(fftw_complex *data, unsigned int data_len)
{
	unsigned int i = 0;
	for(i = 0; i < data_len; ++i)
	{
		float buf[2];
		if(fread(buf, sizeof(float), 2, stdin) != 2)
			break;
		data[i][0] = buf[0];
		data[i][1] = buf[1];
	}
	return i;
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

	/* I think each forward FFT and the inverse FFT multiply by
	 * another sqrt(len), so to get normalized power, we need to
	 * divide by sqrt(len)^3. This doesn't change any of the
	 * results, except when debugging the raw per-bin power. For the
	 * normalization convention FFTW uses see
	 * http://www.fftw.org/doc/The-1d-Discrete-Fourier-Transform-_0028DFT_0029.html
	 */
	const double normalize_dft = pow(len, 1.5);

	for(i = 0; i < len; ++i)
		ca_samples[i] = (cacode((int) (i / samples_per_chip), sv) ? 1 : -1) / normalize_dft;

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

static int is_present(const struct signal_strength *signal)
{
	/* S/N ratio of about 12.79 dB-Hz is the lowest I've seen that
	 * rules out all undetectable signals I've encountered in test
	 * data sets. It isn't based on any reasoning from first
	 * principles, it just seems to work across a wide range of
	 * source data. */
	return signal->snr >= 19;
}

int main(int argc, char **argv)
{
	if(argc <= 1)
	{
		fprintf(stderr, "usage: %s sample-freq\n", argv[0]);
		exit(1);
	}

	const unsigned int sample_freq = atoi(argv[1]);

	unsigned int training1_len = sample_freq * 10 / 1000;
	unsigned int training2_len = sample_freq * 5 / 1000;
	unsigned int training_len = training1_len + training2_len;
	fftw_complex *training = fftw_malloc(sizeof(fftw_complex) * training_len);
	fftw_complex *training2 = training + training1_len;
	struct signal_strength signals[MAX_SV];
	int i;
	double clock_error_sum = 0;
	unsigned int visible_satellites = 0;
	fftw_plan training_plan = fftw_plan_dft_1d(training1_len, training, training, FFTW_FORWARD, FFTW_ESTIMATE | FFTW_DESTROY_INPUT);

	if(read_samples(training, training_len) < training_len)
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

	for(i = 0; i < MAX_SV; ++i)
		signals[i] = check_satellite(sample_freq, training, training1_len, training2, training2_len, i + 1);

	printf("# SV, S/N (dB-Hz), doppler shift (Hz), code phase (chips), sample clock error (chips/s)\n");
	for(i = 0; i < MAX_SV; ++i)
	{
		if(is_present(&signals[i]))
		{
			printf("%c %d\t%f\t%f\t%f\t%f\n", is_present(&signals[i]) ? '*' : ' ', i + 1,
				10 * log10(signals[i].snr), signals[i].doppler, signals[i].phase, signals[i].clock_error);
			clock_error_sum += signals[i].clock_error;
			++visible_satellites;
		}
	}
	printf("# %u satellites in view; average clock error %f chips/s\n", visible_satellites, clock_error_sum / visible_satellites);
	printf("\n");

	fftw_free(training);
	fftw_cleanup();
	exit(EXIT_SUCCESS);
}
