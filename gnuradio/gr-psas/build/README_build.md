### This is the build directory for gr-psas

##### Try this

* cmake ../
* make
* make install
  * Maybe 'sudo make install'


```

~/.../gnuradio/gr-psas/build (master*) > cmake ..
-- The CXX compiler identification is GNU 5.1.0
-- The C compiler identification is GNU 5.1.0
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Build type not specified: defaulting to release.
-- Boost version: 1.58.0
-- Found the following Boost libraries:
--   filesystem
--   system
-- Found PkgConfig: /usr/bin/pkg-config (found version "0.28") 
-- checking for module 'cppunit'
--   found cppunit, version 1.13.2
-- Found CPPUNIT: /usr/lib64/libcppunit.so;dl  
-- Found Doxygen: /usr/bin/doxygen (found version "1.8.9.1") 
Checking for GNU Radio Module: RUNTIME
-- checking for module 'gnuradio-runtime'
--   found gnuradio-runtime, version 3.7.7
 * INCLUDES=/usr/include
 * LIBS=/usr/lib64/libgnuradio-runtime.so;/usr/lib64/libgnuradio-pmt.so
-- Found GNURADIO_RUNTIME: /usr/lib64/libgnuradio-runtime.so;/usr/lib64/libgnuradio-pmt.so  
GNURADIO_RUNTIME_FOUND = TRUE
CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0026 is not set: Disallow use of the LOCATION target property.
  Run "cmake --help-policy CMP0026" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The LOCATION property should not be read from target "test-psas".  Use the
  target name directly with add_custom_command, or use the generator
  expression $<TARGET_FILE>, as appropriate.

Call Stack (most recent call first):
  lib/CMakeLists.txt:80 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- 
-- Checking for module SWIG
-- Found SWIG version 3.0.5.
-- Found SWIG: /usr/bin/swig  
-- Found PythonLibs: /usr/lib64/libpython2.7.so (found suitable version "2.7.10", minimum required is "2") 
-- Found PythonInterp: /usr/bin/python2 (found suitable version "2.7.10", minimum required is "2") 
-- Looking for sys/types.h
-- Looking for sys/types.h - found
-- Looking for stdint.h
-- Looking for stdint.h - found
-- Looking for stddef.h
-- Looking for stddef.h - found
-- Check size of size_t
-- Check size of size_t - done
-- Check size of unsigned int
-- Check size of unsigned int - done
-- Performing Test HAVE_WNO_UNUSED_BUT_SET_VARIABLE
-- Performing Test HAVE_WNO_UNUSED_BUT_SET_VARIABLE - Success
CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0026 is not set: Disallow use of the LOCATION target property.
  Run "cmake --help-policy CMP0026" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The LOCATION property should not be read from target "gnuradio-psas".  Use
  the target name directly with add_custom_command, or use the generator
  expression $<TARGET_FILE>, as appropriate.

Call Stack (most recent call first):
  python/CMakeLists.txt:44 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0045 is not set: Error on non-existent target in
  get_target_property.  Run "cmake --help-policy CMP0045" for policy details.
  Use the cmake_policy command to set the policy and suppress this warning.

  get_target_property() called with non-existent target "/usr/bin/python2".
Call Stack (most recent call first):
  python/CMakeLists.txt:44 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0045 is not set: Error on non-existent target in
  get_target_property.  Run "cmake --help-policy CMP0045" for policy details.
  Use the cmake_policy command to set the policy and suppress this warning.

  get_target_property() called with non-existent target
  "/home/kwilson/Projects/gps/gnuradio/gr-psas/python/qa_gps_iq.py".
Call Stack (most recent call first):
  python/CMakeLists.txt:44 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Configuring done
-- Generating done
-- Build files have been written to: /home/kwilson/Projects/gps/gnuradio/gr-psas/build
~/.../gnuradio/gr-psas/build (master*) > make
Scanning dependencies of target gnuradio-psas
[  6%] Building CXX object lib/CMakeFiles/gnuradio-psas.dir/gps_iq_impl.cc.o
Linking CXX shared library libgnuradio-psas.so
[  6%] Built target gnuradio-psas
Scanning dependencies of target test-psas
[ 12%] Building CXX object lib/CMakeFiles/test-psas.dir/test_psas.cc.o
[ 18%] Building CXX object lib/CMakeFiles/test-psas.dir/qa_psas.cc.o
[ 25%] Building CXX object lib/CMakeFiles/test-psas.dir/qa_gps_iq.cc.o
Linking CXX executable test-psas
[ 25%] Built target test-psas
Scanning dependencies of target _psas_swig_doc_tag
[ 31%] Building CXX object swig/CMakeFiles/_psas_swig_doc_tag.dir/_psas_swig_doc_tag.cpp.o
Linking CXX executable _psas_swig_doc_tag
[ 31%] Built target _psas_swig_doc_tag
Scanning dependencies of target psas_swig_swig_doc
[ 37%] Generating doxygen xml for psas_swig_doc docs
Warning: Tag `XML_SCHEMA' at line 1478 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/swig/psas_swig_doc_swig_docs/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
Warning: Tag `XML_DTD' at line 1484 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/swig/psas_swig_doc_swig_docs/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
[ 43%] Generating python docstrings for psas_swig_doc
[ 43%] Built target psas_swig_swig_doc
Scanning dependencies of target _psas_swig_swig_tag
[ 50%] Building CXX object swig/CMakeFiles/_psas_swig_swig_tag.dir/_psas_swig_swig_tag.cpp.o
Linking CXX executable _psas_swig_swig_tag
[ 50%] Built target _psas_swig_swig_tag
[ 56%] Generating psas_swig.tag
Scanning dependencies of target psas_swig_swig_2d0df
[ 62%] Building CXX object swig/CMakeFiles/psas_swig_swig_2d0df.dir/psas_swig_swig_2d0df.cpp.o
Linking CXX executable psas_swig_swig_2d0df
Swig source
[ 62%] Built target psas_swig_swig_2d0df
Scanning dependencies of target _psas_swig
[ 68%] Building CXX object swig/CMakeFiles/_psas_swig.dir/psas_swigPYTHON_wrap.cxx.o
Linking CXX shared module _psas_swig.so
[ 68%] Built target _psas_swig
Scanning dependencies of target pygen_swig_fe849
[ 75%] Generating psas_swig.pyc
[ 81%] Generating psas_swig.pyo
[ 81%] Built target pygen_swig_fe849
Scanning dependencies of target pygen_python_86b50
[ 87%] Generating __init__.pyc
[ 93%] Generating __init__.pyo
[ 93%] Built target pygen_python_86b50
Scanning dependencies of target pygen_apps_9a6dd
[ 93%] Built target pygen_apps_9a6dd
Scanning dependencies of target doxygen_target
[100%] Generating documentation with doxygen
Warning: Tag `XML_SCHEMA' at line 1510 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/docs/doxygen/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
Warning: Tag `XML_DTD' at line 1516 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/docs/doxygen/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
[100%] Built target doxygen_target
~/.../gnuradio/gr-psas/build (master*) > sudo make install
[  6%] Built target gnuradio-psas
[ 25%] Built target test-psas
[ 31%] Built target _psas_swig_doc_tag
[ 43%] Built target psas_swig_swig_doc
[ 50%] Built target _psas_swig_swig_tag
[ 62%] Built target psas_swig_swig_2d0df
[ 68%] Built target _psas_swig
[ 81%] Built target pygen_swig_fe849
[ 93%] Built target pygen_python_86b50
[ 93%] Built target pygen_apps_9a6dd
[100%] Built target doxygen_target
Install the project...
-- Install configuration: "Release"
-- Up-to-date: /usr/local/lib/cmake/psas/psasConfig.cmake
-- Up-to-date: /usr/local/include/psas/api.h
-- Up-to-date: /usr/local/include/psas/gps_iq.h
-- Installing: /usr/local/lib/libgnuradio-psas.so
-- Installing: /usr/local/lib/python2.7/site-packages/psas/_psas_swig.so
-- Removed runtime path from "/usr/local/lib/python2.7/site-packages/psas/_psas_swig.so"
-- Installing: /usr/local/lib/python2.7/site-packages/psas/psas_swig.py
-- Installing: /usr/local/lib/python2.7/site-packages/psas/psas_swig.pyc
-- Installing: /usr/local/lib/python2.7/site-packages/psas/psas_swig.pyo
-- Up-to-date: /usr/local/include/psas/psas/swig/psas_swig.i
-- Installing: /usr/local/include/psas/psas/swig/psas_swig_doc.i
-- Up-to-date: /usr/local/lib/python2.7/site-packages/psas/__init__.py
-- Installing: /usr/local/lib/python2.7/site-packages/psas/__init__.pyc
-- Installing: /usr/local/lib/python2.7/site-packages/psas/__init__.pyo
-- Up-to-date: /usr/local/share/gnuradio/grc/blocks/psas_gps_iq.xml
-- Up-to-date: /usr/local/share/doc/gr-psas/xml
-- Installing: /usr/local/share/doc/gr-psas/xml/main__page_8dox.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/group__defs_8dox.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacegr_1_1blocks.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacegr_1_1psas.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/classgr_1_1blocks_1_1gps__iq__impl.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/index.xsd
-- Installing: /usr/local/share/doc/gr-psas/xml/dir_3f35a7bb784763f5176abbf2a2e58057.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/combine.xslt
-- Installing: /usr/local/share/doc/gr-psas/xml/gps__iq_8h.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/dir_97aefd0d527b934f1d99a682da8fe6a9.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacegr.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/index.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/group__block.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/indexpage.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacestd.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/api_8h.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/compound.xsd
-- Installing: /usr/local/share/doc/gr-psas/xml/dir_d44c64559bbebec7f509842c48db8b23.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/classgr_1_1psas_1_1gps__iq.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/gps__iq__impl_8h.xml
-- Up-to-date: /usr/local/share/doc/gr-psas/html
-- Installing: /usr/local/share/doc/gr-psas/html/doxygen.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23.html
-- Installing: /usr/local/share/doc/gr-psas/html/functions_type.html
-- Installing: /usr/local/share/doc/gr-psas/html/splitbar.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_0.map
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1psas.html
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/modules.js
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h_source.html
-- Installing: /usr/local/share/doc/gr-psas/html/annotated.js
-- Installing: /usr/local/share/doc/gr-psas/html/doxygen.css
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_0.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl.js
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23_dep.map
-- Installing: /usr/local/share/doc/gr-psas/html/open.png
-- Installing: /usr/local/share/doc/gr-psas/html/tab_b.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/globals.html
-- Installing: /usr/local/share/doc/gr-psas/html/navtreeindex0.js
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h.js
-- Installing: /usr/local/share/doc/gr-psas/html/group__block.html
-- Installing: /usr/local/share/doc/gr-psas/html/annotated.html
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/modules.html
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057_dep.map
-- Installing: /usr/local/share/doc/gr-psas/html/jquery.js
-- Installing: /usr/local/share/doc/gr-psas/html/folderopen.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_1.map
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq__inherit__graph.md5
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057.html
-- Installing: /usr/local/share/doc/gr-psas/html/main__page_8dox.html
-- Installing: /usr/local/share/doc/gr-psas/html/resize.js
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq-members.html
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1blocks.js
-- Installing: /usr/local/share/doc/gr-psas/html/files.html
-- Installing: /usr/local/share/doc/gr-psas/html/graph_legend.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr.js
-- Installing: /usr/local/share/doc/gr-psas/html/nav_g.png
-- Installing: /usr/local/share/doc/gr-psas/html/navtree.css
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/globals_defs.html
-- Installing: /usr/local/share/doc/gr-psas/html/nav_h.png
-- Installing: /usr/local/share/doc/gr-psas/html/group__defs_8dox.html
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl__inherit__graph.md5
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057_dep.md5
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__dep__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_0.md5
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h_source.html
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq__inherit__graph.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23_dep.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9_dep.map
-- Installing: /usr/local/share/doc/gr-psas/html/sync_off.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h_source.html
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq__inherit__graph.map
-- Installing: /usr/local/share/doc/gr-psas/html/arrowright.png
-- Installing: /usr/local/share/doc/gr-psas/html/nav_f.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9_dep.md5
-- Installing: /usr/local/share/doc/gr-psas/html/navtreedata.js
-- Installing: /usr/local/share/doc/gr-psas/html/index.html
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9_dep.png
-- Installing: /usr/local/share/doc/gr-psas/html/hierarchy.html
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h.html
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_1.png
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr.html
-- Installing: /usr/local/share/doc/gr-psas/html/arrowdown.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherits.html
-- Installing: /usr/local/share/doc/gr-psas/html/graph_legend.md5
-- Installing: /usr/local/share/doc/gr-psas/html/navtree.js
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1blocks.html
-- Installing: /usr/local/share/doc/gr-psas/html/files.js
-- Installing: /usr/local/share/doc/gr-psas/html/folderclosed.png
-- Installing: /usr/local/share/doc/gr-psas/html/classes.html
-- Installing: /usr/local/share/doc/gr-psas/html/tabs.css
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl__inherit__graph.map
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_1.md5
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23_dep.md5
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl.html
-- Installing: /usr/local/share/doc/gr-psas/html/tab_s.png
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__dep__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/doc.png
-- Installing: /usr/local/share/doc/gr-psas/html/closed.png
-- Installing: /usr/local/share/doc/gr-psas/html/tab_a.png
-- Installing: /usr/local/share/doc/gr-psas/html/graph_legend.html
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__dep__incl.md5
~/.../gnuradio/gr-psas/build (master*) > cmake ..
-- The CXX compiler identification is GNU 5.1.0
-- The C compiler identification is GNU 5.1.0
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Build type not specified: defaulting to release.
-- Boost version: 1.58.0
-- Found the following Boost libraries:
--   filesystem
--   system
-- Found PkgConfig: /usr/bin/pkg-config (found version "0.28") 
-- checking for module 'cppunit'
--   found cppunit, version 1.13.2
-- Found CPPUNIT: /usr/lib64/libcppunit.so;dl  
-- Found Doxygen: /usr/bin/doxygen (found version "1.8.9.1") 
Checking for GNU Radio Module: RUNTIME
-- checking for module 'gnuradio-runtime'
--   found gnuradio-runtime, version 3.7.7
 * INCLUDES=/usr/include
 * LIBS=/usr/lib64/libgnuradio-runtime.so;/usr/lib64/libgnuradio-pmt.so
-- Found GNURADIO_RUNTIME: /usr/lib64/libgnuradio-runtime.so;/usr/lib64/libgnuradio-pmt.so  
GNURADIO_RUNTIME_FOUND = TRUE
CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0026 is not set: Disallow use of the LOCATION target property.
  Run "cmake --help-policy CMP0026" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The LOCATION property should not be read from target "test-psas".  Use the
  target name directly with add_custom_command, or use the generator
  expression $<TARGET_FILE>, as appropriate.

Call Stack (most recent call first):
  lib/CMakeLists.txt:80 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- 
-- Checking for module SWIG
-- Found SWIG version 3.0.5.
-- Found SWIG: /usr/bin/swig  
-- Found PythonLibs: /usr/lib64/libpython2.7.so (found suitable version "2.7.10", minimum required is "2") 
-- Found PythonInterp: /usr/bin/python2 (found suitable version "2.7.10", minimum required is "2") 
-- Looking for sys/types.h
-- Looking for sys/types.h - found
-- Looking for stdint.h
-- Looking for stdint.h - found
-- Looking for stddef.h
-- Looking for stddef.h - found
-- Check size of size_t
-- Check size of size_t - done
-- Check size of unsigned int
-- Check size of unsigned int - done
-- Performing Test HAVE_WNO_UNUSED_BUT_SET_VARIABLE
-- Performing Test HAVE_WNO_UNUSED_BUT_SET_VARIABLE - Success
CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0026 is not set: Disallow use of the LOCATION target property.
  Run "cmake --help-policy CMP0026" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  The LOCATION property should not be read from target "gnuradio-psas".  Use
  the target name directly with add_custom_command, or use the generator
  expression $<TARGET_FILE>, as appropriate.

Call Stack (most recent call first):
  python/CMakeLists.txt:44 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0045 is not set: Error on non-existent target in
  get_target_property.  Run "cmake --help-policy CMP0045" for policy details.
  Use the cmake_policy command to set the policy and suppress this warning.

  get_target_property() called with non-existent target "/usr/bin/python2".
Call Stack (most recent call first):
  python/CMakeLists.txt:44 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /usr/lib64/cmake/gnuradio/GrTest.cmake:45 (get_target_property):
  Policy CMP0045 is not set: Error on non-existent target in
  get_target_property.  Run "cmake --help-policy CMP0045" for policy details.
  Use the cmake_policy command to set the policy and suppress this warning.

  get_target_property() called with non-existent target
  "/home/kwilson/Projects/gps/gnuradio/gr-psas/python/qa_gps_iq.py".
Call Stack (most recent call first):
  python/CMakeLists.txt:44 (GR_ADD_TEST)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Configuring done
-- Generating done
-- Build files have been written to: /home/kwilson/Projects/gps/gnuradio/gr-psas/build
~/.../gnuradio/gr-psas/build (master*) > make
Scanning dependencies of target gnuradio-psas
[  6%] Building CXX object lib/CMakeFiles/gnuradio-psas.dir/gps_iq_impl.cc.o
Linking CXX shared library libgnuradio-psas.so
[  6%] Built target gnuradio-psas
Scanning dependencies of target test-psas
[ 12%] Building CXX object lib/CMakeFiles/test-psas.dir/test_psas.cc.o
[ 18%] Building CXX object lib/CMakeFiles/test-psas.dir/qa_psas.cc.o
[ 25%] Building CXX object lib/CMakeFiles/test-psas.dir/qa_gps_iq.cc.o
Linking CXX executable test-psas
[ 25%] Built target test-psas
Scanning dependencies of target _psas_swig_doc_tag
[ 31%] Building CXX object swig/CMakeFiles/_psas_swig_doc_tag.dir/_psas_swig_doc_tag.cpp.o
Linking CXX executable _psas_swig_doc_tag
[ 31%] Built target _psas_swig_doc_tag
Scanning dependencies of target psas_swig_swig_doc
[ 37%] Generating doxygen xml for psas_swig_doc docs
Warning: Tag `XML_SCHEMA' at line 1478 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/swig/psas_swig_doc_swig_docs/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
Warning: Tag `XML_DTD' at line 1484 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/swig/psas_swig_doc_swig_docs/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
[ 43%] Generating python docstrings for psas_swig_doc
[ 43%] Built target psas_swig_swig_doc
Scanning dependencies of target _psas_swig_swig_tag
[ 50%] Building CXX object swig/CMakeFiles/_psas_swig_swig_tag.dir/_psas_swig_swig_tag.cpp.o
Linking CXX executable _psas_swig_swig_tag
[ 50%] Built target _psas_swig_swig_tag
[ 56%] Generating psas_swig.tag
Scanning dependencies of target psas_swig_swig_2d0df
[ 62%] Building CXX object swig/CMakeFiles/psas_swig_swig_2d0df.dir/psas_swig_swig_2d0df.cpp.o
Linking CXX executable psas_swig_swig_2d0df
Swig source
[ 62%] Built target psas_swig_swig_2d0df
Scanning dependencies of target _psas_swig
[ 68%] Building CXX object swig/CMakeFiles/_psas_swig.dir/psas_swigPYTHON_wrap.cxx.o
Linking CXX shared module _psas_swig.so
[ 68%] Built target _psas_swig
Scanning dependencies of target pygen_swig_fe849
[ 75%] Generating psas_swig.pyc
[ 81%] Generating psas_swig.pyo
[ 81%] Built target pygen_swig_fe849
Scanning dependencies of target pygen_python_86b50
[ 87%] Generating __init__.pyc
[ 93%] Generating __init__.pyo
[ 93%] Built target pygen_python_86b50
Scanning dependencies of target pygen_apps_9a6dd
[ 93%] Built target pygen_apps_9a6dd
Scanning dependencies of target doxygen_target
[100%] Generating documentation with doxygen
Warning: Tag `XML_SCHEMA' at line 1510 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/docs/doxygen/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
Warning: Tag `XML_DTD' at line 1516 of file `/home/kwilson/Projects/gps/gnuradio/gr-psas/build/docs/doxygen/Doxyfile' has become obsolete.
         To avoid this warning please remove this line from your configuration file or upgrade it using "doxygen -u"
[100%] Built target doxygen_target
~/.../gnuradio/gr-psas/build (master*) > sudo make install
[  6%] Built target gnuradio-psas
[ 25%] Built target test-psas
[ 31%] Built target _psas_swig_doc_tag
[ 43%] Built target psas_swig_swig_doc
[ 50%] Built target _psas_swig_swig_tag
[ 62%] Built target psas_swig_swig_2d0df
[ 68%] Built target _psas_swig
[ 81%] Built target pygen_swig_fe849
[ 93%] Built target pygen_python_86b50
[ 93%] Built target pygen_apps_9a6dd
[100%] Built target doxygen_target
Install the project...
-- Install configuration: "Release"
-- Up-to-date: /usr/local/lib/cmake/psas/psasConfig.cmake
-- Up-to-date: /usr/local/include/psas/api.h
-- Up-to-date: /usr/local/include/psas/gps_iq.h
-- Installing: /usr/local/lib/libgnuradio-psas.so
-- Installing: /usr/local/lib/python2.7/site-packages/psas/_psas_swig.so
-- Removed runtime path from "/usr/local/lib/python2.7/site-packages/psas/_psas_swig.so"
-- Installing: /usr/local/lib/python2.7/site-packages/psas/psas_swig.py
-- Installing: /usr/local/lib/python2.7/site-packages/psas/psas_swig.pyc
-- Installing: /usr/local/lib/python2.7/site-packages/psas/psas_swig.pyo
-- Up-to-date: /usr/local/include/psas/psas/swig/psas_swig.i
-- Installing: /usr/local/include/psas/psas/swig/psas_swig_doc.i
-- Up-to-date: /usr/local/lib/python2.7/site-packages/psas/__init__.py
-- Installing: /usr/local/lib/python2.7/site-packages/psas/__init__.pyc
-- Installing: /usr/local/lib/python2.7/site-packages/psas/__init__.pyo
-- Up-to-date: /usr/local/share/gnuradio/grc/blocks/psas_gps_iq.xml
-- Up-to-date: /usr/local/share/doc/gr-psas/xml
-- Installing: /usr/local/share/doc/gr-psas/xml/main__page_8dox.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/group__defs_8dox.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacegr_1_1blocks.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacegr_1_1psas.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/classgr_1_1blocks_1_1gps__iq__impl.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/index.xsd
-- Installing: /usr/local/share/doc/gr-psas/xml/dir_3f35a7bb784763f5176abbf2a2e58057.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/combine.xslt
-- Installing: /usr/local/share/doc/gr-psas/xml/gps__iq_8h.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/dir_97aefd0d527b934f1d99a682da8fe6a9.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacegr.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/index.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/group__block.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/indexpage.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/namespacestd.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/api_8h.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/compound.xsd
-- Installing: /usr/local/share/doc/gr-psas/xml/dir_d44c64559bbebec7f509842c48db8b23.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/classgr_1_1psas_1_1gps__iq.xml
-- Installing: /usr/local/share/doc/gr-psas/xml/gps__iq__impl_8h.xml
-- Up-to-date: /usr/local/share/doc/gr-psas/html
-- Installing: /usr/local/share/doc/gr-psas/html/doxygen.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23.html
-- Installing: /usr/local/share/doc/gr-psas/html/functions_type.html
-- Installing: /usr/local/share/doc/gr-psas/html/splitbar.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_0.map
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1psas.html
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/modules.js
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h_source.html
-- Installing: /usr/local/share/doc/gr-psas/html/annotated.js
-- Installing: /usr/local/share/doc/gr-psas/html/doxygen.css
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_0.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl.js
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23_dep.map
-- Installing: /usr/local/share/doc/gr-psas/html/open.png
-- Installing: /usr/local/share/doc/gr-psas/html/tab_b.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/globals.html
-- Installing: /usr/local/share/doc/gr-psas/html/navtreeindex0.js
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h.js
-- Installing: /usr/local/share/doc/gr-psas/html/group__block.html
-- Installing: /usr/local/share/doc/gr-psas/html/annotated.html
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/modules.html
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057_dep.map
-- Installing: /usr/local/share/doc/gr-psas/html/jquery.js
-- Installing: /usr/local/share/doc/gr-psas/html/folderopen.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_1.map
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq__inherit__graph.md5
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057.html
-- Installing: /usr/local/share/doc/gr-psas/html/main__page_8dox.html
-- Installing: /usr/local/share/doc/gr-psas/html/resize.js
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq-members.html
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1blocks.js
-- Installing: /usr/local/share/doc/gr-psas/html/files.html
-- Installing: /usr/local/share/doc/gr-psas/html/graph_legend.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr.js
-- Installing: /usr/local/share/doc/gr-psas/html/nav_g.png
-- Installing: /usr/local/share/doc/gr-psas/html/navtree.css
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/globals_defs.html
-- Installing: /usr/local/share/doc/gr-psas/html/nav_h.png
-- Installing: /usr/local/share/doc/gr-psas/html/group__defs_8dox.html
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl__inherit__graph.md5
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057_dep.md5
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__dep__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_0.md5
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h_source.html
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq__inherit__graph.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23_dep.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9_dep.map
-- Installing: /usr/local/share/doc/gr-psas/html/sync_off.png
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h_source.html
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq__inherit__graph.map
-- Installing: /usr/local/share/doc/gr-psas/html/arrowright.png
-- Installing: /usr/local/share/doc/gr-psas/html/nav_f.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9_dep.md5
-- Installing: /usr/local/share/doc/gr-psas/html/navtreedata.js
-- Installing: /usr/local/share/doc/gr-psas/html/index.html
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9_dep.png
-- Installing: /usr/local/share/doc/gr-psas/html/hierarchy.html
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h.html
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_1.png
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr.html
-- Installing: /usr/local/share/doc/gr-psas/html/arrowdown.png
-- Installing: /usr/local/share/doc/gr-psas/html/inherits.html
-- Installing: /usr/local/share/doc/gr-psas/html/graph_legend.md5
-- Installing: /usr/local/share/doc/gr-psas/html/navtree.js
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1blocks.html
-- Installing: /usr/local/share/doc/gr-psas/html/files.js
-- Installing: /usr/local/share/doc/gr-psas/html/folderclosed.png
-- Installing: /usr/local/share/doc/gr-psas/html/classes.html
-- Installing: /usr/local/share/doc/gr-psas/html/tabs.css
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl__inherit__graph.map
-- Installing: /usr/local/share/doc/gr-psas/html/inherit_graph_1.md5
-- Installing: /usr/local/share/doc/gr-psas/html/dir_d44c64559bbebec7f509842c48db8b23_dep.md5
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl.html
-- Installing: /usr/local/share/doc/gr-psas/html/tab_s.png
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__dep__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/doc.png
-- Installing: /usr/local/share/doc/gr-psas/html/closed.png
-- Installing: /usr/local/share/doc/gr-psas/html/tab_a.png
-- Installing: /usr/local/share/doc/gr-psas/html/graph_legend.html
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__dep__incl.md5
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq.js
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h.html
-- Installing: /usr/local/share/doc/gr-psas/html/bdwn.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9.html
-- Installing: /usr/local/share/doc/gr-psas/html/functions_func.html
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq.html
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1psas.js
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057_dep.png
-- Installing: /usr/local/share/doc/gr-psas/html/tab_h.png
-- Installing: /usr/local/share/doc/gr-psas/html/functions.html
-- Installing: /usr/local/share/doc/gr-psas/html/dynsections.js
-- Installing: /usr/local/share/doc/gr-psas/html/sync_on.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl__inherit__graph.png
-- Installing: /usr/local/share/doc/gr-psas/html/bc_s.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl-members.html
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h.html
-- Installing: /usr/local/share/doc/gr-psas/html/hierarchy.js
~/.../gnuradio/gr-psas/build (master*) > 
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__incl.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq.js
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq__impl_8h.html
-- Installing: /usr/local/share/doc/gr-psas/html/bdwn.png
-- Installing: /usr/local/share/doc/gr-psas/html/dir_97aefd0d527b934f1d99a682da8fe6a9.html
-- Installing: /usr/local/share/doc/gr-psas/html/functions_func.html
-- Installing: /usr/local/share/doc/gr-psas/html/api_8h__incl.map
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1psas_1_1gps__iq.html
-- Installing: /usr/local/share/doc/gr-psas/html/namespacegr_1_1psas.js
-- Installing: /usr/local/share/doc/gr-psas/html/dir_3f35a7bb784763f5176abbf2a2e58057_dep.png
-- Installing: /usr/local/share/doc/gr-psas/html/tab_h.png
-- Installing: /usr/local/share/doc/gr-psas/html/functions.html
-- Installing: /usr/local/share/doc/gr-psas/html/dynsections.js
-- Installing: /usr/local/share/doc/gr-psas/html/sync_on.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl__inherit__graph.png
-- Installing: /usr/local/share/doc/gr-psas/html/bc_s.png
-- Installing: /usr/local/share/doc/gr-psas/html/classgr_1_1blocks_1_1gps__iq__impl-members.html
-- Installing: /usr/local/share/doc/gr-psas/html/gps__iq_8h.html
-- Installing: /usr/local/share/doc/gr-psas/html/hierarchy.js
~/.../gnuradio/gr-psas/build (master*) > 

```


##### Then run GNU Radio Companion

```
gnuradio-companion
```


