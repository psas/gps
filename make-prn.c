#include <stdio.h>
#include <stdlib.h>
#include "prn.h"

static void usage(char *name)
{
	fprintf(stderr, "usage: %s sample-freq [satellite]\n", name);
	exit(1);
}

int main(int argc, char **argv)
{
	if(argc < 2)
		usage(argv[0]);
	const int sample_freq = atoi(argv[1]);
	const int total_samples = sample_freq / 1000;

	int sv = 1;
	if(argc > 2)
		sv = atoi(argv[2]);
	if(sv < 1 || sv > MAX_SV)
		usage(argv[0]);

	float buf[2] = { 0, 0 };
	unsigned int i;
	for(i = 0; i < total_samples; ++i)
	{
		buf[0] = cacode(i * 1023 / total_samples, sv) ? 1.0f : -1.0f;
		fwrite(buf, sizeof *buf, 2, stdout);
	}
	return 0;
}
