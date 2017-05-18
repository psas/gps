/* -*- c++ -*- */
/*
 * Copyright 2012 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
	#include "config.h"
#endif

#include "gps_iq_impl.h"
#include <gnuradio/thread/thread.h>
#include <gnuradio/io_signature.h>
#include <cstdio>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdexcept>
#include <stdio.h>
#include <stdint.h>

// win32 (mingw/msvc) specific
#ifdef HAVE_IO_H
	#include <io.h>
#endif
#ifdef O_BINARY
	#define OUR_O_BINARY O_BINARY
#else
	#define OUR_O_BINARY 0
#endif
// should be handled via configure
#ifdef O_LARGEFILE
	#define OUR_O_LARGEFILE O_LARGEFILE
#else
	#define OUR_O_LARGEFILE 0
#endif

namespace gr
{
	namespace blocks
	{

		file_source::sptr file_source::make(size_t itemsize, const char * filename, bool repeat)
		{
			return gnuradio::get_initial_sptr
			       (new gps_iq_impl(filename, repeat));
		}

		gps_iq_impl::gps_iq_impl(const char * filename, bool repeat)
			: sync_block("gps_iq",
			             io_signature::make(0, 0, 0),
			             io_signature::make(1, 1, 1)),
			  d_fp(0), d_new_fp(0), d_repeat(repeat),
			  d_updated(false)
		{
			open(filename, repeat);
			do_update();
		}

		gps_iq_impl::~gps_iq_impl()
		{
			if(d_fp)
			{
				fclose ((FILE *)d_fp);
			}
			if(d_new_fp)
			{
				fclose ((FILE *)d_new_fp);
			}
		}

		bool gps_iq_impl::seek(long seek_point, int whence)
		{
			return fseek((FILE *)d_fp, seek_point / 2, whence) == 0;
		}

		void gps_iq_impl::open(const char * filename, bool repeat)
		{
			// obtain exclusive access for duration of this function
			gr::thread::scoped_lock lock(fp_mutex);

			int fd;

			// we use "open" to use to the O_LARGEFILE flag
			if((fd = ::open(filename, O_RDONLY | OUR_O_LARGEFILE | OUR_O_BINARY)) < 0)
			{
				perror(filename);
				throw std::runtime_error("can't open file");
			}

			if(d_new_fp)
			{
				fclose(d_new_fp);
				d_new_fp = 0;
			}

			if((d_new_fp = fdopen (fd, "rb")) == NULL)
			{
				perror(filename);
				::close(fd);    // don't leak file descriptor if fdopen fails
				throw std::runtime_error("can't open file");
			}

			d_updated = true;
			d_repeat = repeat;
		}

		void gps_iq_impl::close()
		{
			// obtain exclusive access for duration of this function
			gr::thread::scoped_lock lock(fp_mutex);

			if(d_new_fp != NULL)
			{
				fclose(d_new_fp);
				d_new_fp = NULL;
			}
			d_updated = true;
		}

		void gps_iq_impl::do_update()
		{
			if(d_updated)
			{
				gr::thread::scoped_lock lock(fp_mutex); // hold while in scope

				if(d_fp)
				{
					fclose(d_fp);
				}

				d_fp = d_new_fp;    // install new file pointer
				d_new_fp = 0;
				d_updated = false;
			}
		}

		float gps_iq_impl::sign_magnitude(unsigned sign, unsigned magnitude)
		{
			float value = magnitude ? 1      : 1.0 / 3.0;
			float res   = sign      ? -value : value;

			return res;
		}

		void gps_iq_impl::byte_to_two_iq(uint8_t buf, gr_complex * ca, gr_complex * cb)
		{
			// from read-max.c
				/* Each nibble contains, in order from MSB to LSB:
				 * - in-phase (real) part followed by quadrature-phase (imaginary) part
				 * - older sample followed by newer sample */
			ca->real(sign_magnitude((buf >> 7) & 1, (buf >> 6) & 1));
			ca->imag(sign_magnitude((buf >> 5) & 1, (buf >> 4) & 1));

			cb->real(sign_magnitude((buf >> 3) & 1, (buf >> 2) & 1));
			cb->imag(sign_magnitude((buf >> 1) & 1, (buf >> 0) & 1));
		}

		int gps_iq_impl::work(int noutput_items,
		                          gr_vector_const_void_star & input_items,
		                          gr_vector_void_star & output_items)
		{
			gr_complex * o          = (gr_complex *)output_items[0];
			int          size       = noutput_items;

			do_update();       // update d_fp is reqd
			if(d_fp == NULL)
			{
				throw std::runtime_error("work with file not open");
			}

			gr::thread::scoped_lock lock(fp_mutex); // hold for the rest of this function
			while(size)
			{
				int ch = fgetc((FILE *)d_fp);
				if(ch >= 0)
				{
					byte_to_two_iq(ch, o, o + 1);
					size -= 2;
					o += 2;
				}
				else
				{
					// We got an error from fgetc.
					// any event, if we're in repeat mode, seek back to the beginning
					// of the file and try again, else break
					if(!d_repeat)
					{
						break;
					}

					if(fseek ((FILE *) d_fp, 0, SEEK_SET) == -1)
					{
						fprintf(stderr, "[%s] fseek failed\n", __FILE__);
						exit(-1);
					}
				}
			}

			if(size > 0)                  // EOF or error
			{
				if(size == noutput_items)       // we didn't read anything; say we're done
				{
					return -1;
				}
				return noutput_items - size;    // else return partial result
			}
			return noutput_items;
		}
	} /* namespace blocks */
} /* namespace gr */

