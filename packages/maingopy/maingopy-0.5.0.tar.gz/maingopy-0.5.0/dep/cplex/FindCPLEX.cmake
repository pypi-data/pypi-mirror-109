# This module finds cplex.
#
# The variables CPLEX_ROOT_DIR_x can serve as a hint stored in the cmake cache.

if(WIN32)
  execute_process(COMMAND cmd /C set CPLEX_STUDIO_DIR OUTPUT_VARIABLE CPLEX_STUDIO_DIR_VAR ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)

  if(NOT CPLEX_STUDIO_DIR_VAR)
    message("Unable to find CPLEX: environment variable CPLEX_STUDIO_DIR<VERSION> not set.")
  else()

    # We want to use version 12.8 or 12.9 only, where the latter is preferred
	string(REGEX MATCH "CPLEX_STUDIO_DIR129[^\n]*" CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION ${CPLEX_STUDIO_DIR_VAR})
	if (NOT(CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION))
		string(REGEX MATCH "CPLEX_STUDIO_DIR128[^\n]*" CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION ${CPLEX_STUDIO_DIR_VAR})
	endif()
	if (NOT(CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION))
		message("Unable to find CPLEX versions 12.8 or 12.9: only found the following environment variables:\n${CPLEX_STUDIO_DIR_VAR}")
	else()
		string(REGEX REPLACE "CPLEX_STUDIO_DIR" "" CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION ${CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION})
		string(REGEX MATCH "^[0-9]+" CPLEX_WIN_VERSION ${CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION})
		string(REGEX REPLACE "[0-9]+=" "" CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION ${CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION})
		file(TO_CMAKE_PATH "${CPLEX_STUDIO_DIR_VAR_CORRECT_VERSION}" CPLEX_ROOT_DIR_GUESS)
		set(CPLEX_ROOT_DIR "${CPLEX_ROOT_DIR_GUESS}")

		message(STATUS "Found CPLEX version ${CPLEX_WIN_VERSION} at '${CPLEX_ROOT_DIR}'")

		string(REGEX REPLACE "/VC/bin/.*" "" VISUAL_STUDIO_PATH ${CMAKE_CXX_COMPILER})
		string(REGEX MATCH "Studio/[0-9]+/" CPLEX_WIN_VS_VERSION ${VISUAL_STUDIO_PATH})
		string(REGEX REPLACE "Studio/" "" CPLEX_WIN_VS_VERSION ${CPLEX_WIN_VS_VERSION})
		string(REGEX REPLACE "/" "" CPLEX_WIN_VS_VERSION ${CPLEX_WIN_VS_VERSION})

		if(NOT ( (${CPLEX_WIN_VS_VERSION} STREQUAL "2017") OR (${CPLEX_WIN_VS_VERSION} STREQUAL "2015") ) )
		message(FATAL_ERROR "CPLEX: unknown Visual Studio version at '${VISUAL_STUDIO_PATH}'.")
		endif()

		set(CPLEX_WIN_VS_VERSION ${CPLEX_WIN_VS_VERSION} CACHE STRING "Visual Studio Version")

		set(CPLEX_WIN_BITNESS x64)

		set(CPLEX_WIN_BITNESS ${CPLEX_WIN_BITNESS} CACHE STRING "On Windows: x86 or x64 (32bit resp. 64bit)")

		message(STATUS "CPLEX: using Visual Studio ${CPLEX_WIN_VS_VERSION} ${CPLEX_WIN_BITNESS} at '${VISUAL_STUDIO_PATH}'")

		if(NOT CPLEX_WIN_LINKAGE)
		set(CPLEX_WIN_LINKAGE mda CACHE STRING "CPLEX linkage variant on Windows. One of these: mda (dll, release), mdd (dll, debug), mta (static, release), mtd (static, debug)")
		endif(NOT CPLEX_WIN_LINKAGE)

		if(NOT CPLEX_WIN_LINKAGE_D)
		set(CPLEX_WIN_LINKAGE_D mdd CACHE STRING "CPLEX linkage variant on Windows. One of these: mda (dll, release), mdd (dll, debug), mta (static, release), mtd (static, debug)")
		endif(NOT CPLEX_WIN_LINKAGE_D)

		# now, generate platform string
		set(CPLEX_WIN_PLATFORM "${CPLEX_WIN_BITNESS}_windows_vs${CPLEX_WIN_VS_VERSION}/stat_${CPLEX_WIN_LINKAGE}")
		set(CPLEX_WIN_PLATFORM_D "${CPLEX_WIN_BITNESS}_windows_vs${CPLEX_WIN_VS_VERSION}/stat_${CPLEX_WIN_LINKAGE_D}")
	  endif()
  endif()

else()

  set(CPLEX_ROOT_DIR "/usr/local/ILOG/CPLEX_Studio129" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR2 "~/IBM/ILOG/CPLEX_Studio129" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR3 "/opt/ibm/ILOG/CPLEX_Studio129" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR4 "/APPLICATIONS/CPLEX_Studio129" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR5 "/usr/local/ILOG/CPLEX_Studio128" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR6 "~/IBM/ILOG/CPLEX_Studio128" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR7 "/opt/ibm/ILOG/CPLEX_Studio128" CACHE PATH "CPLEX root directory.")
  set(CPLEX_ROOT_DIR8 "/APPLICATIONS/CPLEX_Studio128" CACHE PATH "CPLEX root directory.")
  set(CPLEX_WIN_PLATFORM "")

endif()

find_path(CPLEX_INCLUDE_DIR
  ilcplex/cplex.h
  HINTS ${CPLEX_ROOT_DIR}
        ${CPLEX_ROOT_DIR2}
        ${CPLEX_ROOT_DIR3}
        ${CPLEX_ROOT_DIR4}
        ${CPLEX_ROOT_DIR5}
        ${CPLEX_ROOT_DIR6}
        ${CPLEX_ROOT_DIR7}
        ${CPLEX_ROOT_DIR8}
  NO_DEFAULT_PATH
  PATH_SUFFIXES
      include
	  cplex/include
  )

find_path(CPLEX_CONCERT_INCLUDE_DIR
  ilconcert/iloenv.h
  HINTS ${CPLEX_ROOT_DIR}
        ${CPLEX_ROOT_DIR2}
        ${CPLEX_ROOT_DIR3}
        ${CPLEX_ROOT_DIR4}
        ${CPLEX_ROOT_DIR5}
        ${CPLEX_ROOT_DIR6}
        ${CPLEX_ROOT_DIR7}
        ${CPLEX_ROOT_DIR8}
  PATH_SUFFIXES
      include
	  concert/include
  )

find_library(CPLEX_LIBRARY
  NAMES cplex${CPLEX_WIN_VERSION} cplex${CPLEX_WIN_VERSION}0 cplex
  HINTS ${CPLEX_ROOT_DIR}
        ${CPLEX_ROOT_DIR2}
        ${CPLEX_ROOT_DIR3}
        ${CPLEX_ROOT_DIR4}
        ${CPLEX_ROOT_DIR5}
        ${CPLEX_ROOT_DIR6}
        ${CPLEX_ROOT_DIR7}
        ${CPLEX_ROOT_DIR8}
  PATH_SUFFIXES
      cplex/lib/x86-64_debian4.0_4.1/static_pic
	  cplex/lib/x86-64_sles10_4.1/static_pic
	  cplex/lib/x86-64_linux/static_pic
	  cplex/lib/x86-64_osx/static_pic
	  cplex/lib/x86-64_darwin/static_pic
	  cplex/lib/${CPLEX_WIN_PLATFORM}
)


find_library(CPLEX_ILOCPLEX_LIBRARY
  ilocplex
  HINTS ${CPLEX_ROOT_DIR}
        ${CPLEX_ROOT_DIR2}
        ${CPLEX_ROOT_DIR3}
        ${CPLEX_ROOT_DIR4}
        ${CPLEX_ROOT_DIR5}
        ${CPLEX_ROOT_DIR6}
        ${CPLEX_ROOT_DIR7}
        ${CPLEX_ROOT_DIR8}
  PATH_SUFFIXES
      cplex/lib/x86-64_debian4.0_4.1/static_pic
	  cplex/lib/x86-64_sles10_4.1/static_pic
	  cplex/lib/x86-64_linux/static_pic
	  cplex/lib/x86-64_osx/static_pic
	  cplex/lib/x86-64_darwin/static_pic
	  cplex/lib/${CPLEX_WIN_PLATFORM}
  )
message(STATUS "ILOCPLEX Library: ${CPLEX_ILOCPLEX_LIBRARY}")


find_library(CPLEX_CONCERT_LIBRARY
  concert
  HINTS ${CPLEX_ROOT_DIR}
        ${CPLEX_ROOT_DIR2}
        ${CPLEX_ROOT_DIR3}
        ${CPLEX_ROOT_DIR4}
        ${CPLEX_ROOT_DIR5}
        ${CPLEX_ROOT_DIR6}
        ${CPLEX_ROOT_DIR7}
        ${CPLEX_ROOT_DIR8}
  PATH_SUFFIXES
      concert/lib/x86-64_debian4.0_4.1/static_pic
	  concert/lib/x86-64_sles10_4.1/static_pic
	  concert/lib/x86-64_linux/static_pic
	  concert/lib/x86-64_osx/static_pic
	  concert/lib/x86-64_darwin/static_pic
	  concert/lib/${CPLEX_WIN_PLATFORM}
  )
message(STATUS "CONCERT Library: ${CPLEX_CONCERT_LIBRARY}")

#Debug libraries (available for Windows only)
if(WIN32)
    find_library(CPLEX_LIBRARY_D
      NAMES cplex${CPLEX_WIN_VERSION} cplex${CPLEX_WIN_VERSION}0 cplex
      HINTS ${CPLEX_ROOT_DIR}/cplex/lib/${CPLEX_WIN_PLATFORM_D} #windows
      NO_DEFAULT_PATH
      )
    message(STATUS "CPLEX Library (Debug): ${CPLEX_LIBRARY_D}")

    find_library(CPLEX_ILOCPLEX_LIBRARY_D
      ilocplex
      HINTS ${CPLEX_ROOT_DIR}/cplex/lib/${CPLEX_WIN_PLATFORM_D} #windows
      NO_DEFAULT_PATH
      )
    message(STATUS "ILOCPLEX Library (Debug): ${CPLEX_ILOCPLEX_LIBRARY_D}")

    find_library(CPLEX_CONCERT_LIBRARY_D
      concert
      HINTS ${CPLEX_ROOT_DIR}/concert/lib/${CPLEX_WIN_PLATFORM_D} #windows
      NO_DEFAULT_PATH
      )
    message(STATUS "CONCERT Library (Debug): ${CPLEX_CONCERT_LIBRARY_D}")
endif()

# Binaries
if(WIN32)
    find_path(CPLEX_BIN_DIR
      cplex${CPLEX_WIN_VERSION}.dll cplex${CPLEX_WIN_VERSION}0.dll
          HINTS ${CPLEX_ROOT_DIR}/cplex/bin/${CPLEX_WIN_PLATFORM} #windows
      )
else()
    find_path(CPLEX_BIN_DIR
      cplex
	  HINTS ${CPLEX_ROOT_DIR}
			${CPLEX_ROOT_DIR2}
			${CPLEX_ROOT_DIR3}
			${CPLEX_ROOT_DIR4}
			${CPLEX_ROOT_DIR5}
			${CPLEX_ROOT_DIR6}
			${CPLEX_ROOT_DIR7}
			${CPLEX_ROOT_DIR8}
	  PATH_SUFFIXES
		  cplex/bin/x86-64_debian4.0_4.1/static_pic
		  cplex/bin/x86-64_sles10_4.1/static_pic
		  cplex/bin/x86-64_linux/static_pic
		  cplex/bin/x86-64_osx/static_pic
		  cplex/bin/x86-64_darwin/static_pic
		  cplex/bin/${CPLEX_WIN_PLATFORM}
    )
endif()
message(STATUS "CPLEX Bin Dir: ${CPLEX_BIN_DIR}")

include(FindPackageHandleStandardArgs)
if(WIN32)
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(CPLEX DEFAULT_MSG
        CPLEX_LIBRARY CPLEX_LIBRARY_D CPLEX_INCLUDE_DIR CPLEX_ILOCPLEX_LIBRARY CPLEX_ILOCPLEX_LIBRARY_D CPLEX_CONCERT_LIBRARY CPLEX_CONCERT_LIBRARY_D CPLEX_CONCERT_INCLUDE_DIR)
else()
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CPLEX DEFAULT_MSG
        CPLEX_LIBRARY CPLEX_INCLUDE_DIR CPLEX_ILOCPLEX_LIBRARY CPLEX_CONCERT_LIBRARY CPLEX_CONCERT_INCLUDE_DIR)
endif()


if(CPLEX_FOUND)
  set(CPLEX_INCLUDE_DIRS ${CPLEX_INCLUDE_DIR} ${CPLEX_CONCERT_INCLUDE_DIR})
  set(CPLEX_LIBRARIES ${CPLEX_CONCERT_LIBRARY} ${CPLEX_CONCERT_LIBRARY_D} ${CPLEX_ILOCPLEX_LIBRARY} ${CPLEX_ILOCPLEX_LIBRARY_D} ${CPLEX_LIBRARY} ${CPLEX_LIBRARY_D} )
  if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    set(CPLEX_LIBRARIES "${CPLEX_LIBRARIES};m;pthread")
  endif(CMAKE_SYSTEM_NAME STREQUAL "Linux")
endif(CPLEX_FOUND)

mark_as_advanced(CPLEX_LIBRARY CPLEX_LIBRARY_D CPLEX_INCLUDE_DIR CPLEX_ILOCPLEX_LIBRARY CPLEX_ILOCPLEX_LIBRARY_D CPLEX_CONCERT_INCLUDE_DIR CPLEX_CONCERT_LIBRARY CPLEX_CONCERT_LIBRARY_D)