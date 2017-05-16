/* -*- c++ -*- */

#define PSAS_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "psas_swig_doc.i"

%{
#include "psas/gps_iq.h"
%}


%include "psas/gps_iq.h"
GR_SWIG_BLOCK_MAGIC2(psas, gps_iq);
