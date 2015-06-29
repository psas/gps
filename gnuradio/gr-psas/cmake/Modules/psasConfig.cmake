INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PSAS psas)

FIND_PATH(
    PSAS_INCLUDE_DIRS
    NAMES psas/api.h
    HINTS $ENV{PSAS_DIR}/include
        ${PC_PSAS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PSAS_LIBRARIES
    NAMES gnuradio-psas
    HINTS $ENV{PSAS_DIR}/lib
        ${PC_PSAS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PSAS DEFAULT_MSG PSAS_LIBRARIES PSAS_INCLUDE_DIRS)
MARK_AS_ADVANCED(PSAS_LIBRARIES PSAS_INCLUDE_DIRS)

