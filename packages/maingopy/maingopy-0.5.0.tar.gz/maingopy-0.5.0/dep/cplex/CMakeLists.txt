cmake_minimum_required(VERSION 3.8 FATAL_ERROR)

message("Checking files for CPLEX.")
project(cplex CXX)

if(MSVC)
	#----------- Since we are using CPLEX 12.8, only 64 bit is allowed -------------------
	if(NOT "${CMAKE_SIZEOF_VOID_P}" STREQUAL "8" )
		message(FATAL_ERROR "CPLEX 12.8 and 12.9 only support 64 bit. Please choose the 'x64' version of the generator (or, in newer CMake versions, 'x64' as optional platform for generator).")
	endif()	
endif()

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}")

find_package(CPLEX)


if(${CPLEX_FOUND})
	
	# On Windows, CPLEX comes as dlls - on other systems as static libraries
	if(WIN32)
		add_library(cplex-lib SHARED IMPORTED GLOBAL)
		set_target_properties(cplex-lib  PROPERTIES  IMPORTED_IMPLIB_RELEASE ${CPLEX_LIBRARY})
		set_target_properties(cplex-lib  PROPERTIES  IMPORTED_IMPLIB_GENERAL ${CPLEX_LIBRARY})
		set_target_properties(cplex-lib  PROPERTIES  IMPORTED_IMPLIB_DEBUG ${CPLEX_LIBRARY_D})

		add_library(cplex-concert SHARED IMPORTED GLOBAL)
		set_target_properties(cplex-concert  PROPERTIES  INTERFACE_INCLUDE_DIRECTORIES ${CPLEX_CONCERT_INCLUDE_DIR})
		set_target_properties(cplex-concert  PROPERTIES  IMPORTED_IMPLIB_RELEASE   ${CPLEX_CONCERT_LIBRARY})
		set_target_properties(cplex-concert  PROPERTIES  IMPORTED_IMPLIB_GENERAL   ${CPLEX_CONCERT_LIBRARY})
		set_target_properties(cplex-concert  PROPERTIES  IMPORTED_IMPLIB_DEBUG   ${CPLEX_CONCERT_LIBRARY_D})

		add_library(cplex-ilo SHARED IMPORTED GLOBAL)
		set_target_properties(cplex-ilo  PROPERTIES  IMPORTED_IMPLIB_RELEASE   ${CPLEX_ILOCPLEX_LIBRARY})
		set_target_properties(cplex-ilo  PROPERTIES  IMPORTED_IMPLIB_GENERAL   ${CPLEX_ILOCPLEX_LIBRARY})
		set_target_properties(cplex-ilo  PROPERTIES  IMPORTED_IMPLIB_DEBUG   ${CPLEX_ILOCPLEX_LIBRARY_D})
	else()
		add_library(cplex-lib STATIC IMPORTED GLOBAL)
		set_target_properties(cplex-lib  PROPERTIES  IMPORTED_LOCATION ${CPLEX_LIBRARY})
		target_link_libraries(cplex-lib INTERFACE m pthread dl)	

		add_library(cplex-concert STATIC IMPORTED GLOBAL)
		set_target_properties(cplex-concert  PROPERTIES  IMPORTED_LOCATION   ${CPLEX_CONCERT_LIBRARY})

		add_library(cplex-ilo STATIC IMPORTED GLOBAL)
		set_target_properties(cplex-ilo  PROPERTIES  IMPORTED_LOCATION   ${CPLEX_ILOCPLEX_LIBRARY})
	endif()

	set_target_properties(cplex-lib  PROPERTIES  INTERFACE_INCLUDE_DIRECTORIES ${CPLEX_INCLUDE_DIR})
	set_target_properties(cplex-lib  PROPERTIES  INTERFACE_COMPILE_DEFINITIONS IL_STD)
	set_target_properties(cplex-lib  PROPERTIES  INTERFACE_COMPILE_DEFINITIONS HAVE_CPLEX)
	set_target_properties(cplex-concert  PROPERTIES  INTERFACE_INCLUDE_DIRECTORIES ${CPLEX_CONCERT_INCLUDE_DIR})
	set_target_properties(cplex-concert  PROPERTIES  INTERFACE_COMPILE_DEFINITIONS IL_STD)
	
else()
	
	add_library(cplex-lib INTERFACE)
	add_library(cplex-concert INTERFACE)
	add_library(cplex-ilo INTERFACE)
	message("CPLEX could not be found. A dummy target will be used instead and the flag HAVE_CPLEX will not be defined.")
	message("This may be OK depending on the application (e.g., in MAiNGO), but you will not be able to actually use CPLEX.")

endif()


if(CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
	if(${CPLEX_FOUND})
		add_executable(cplex-test
			${PROJECT_SOURCE_DIR}/test/test.cpp
		)
	target_link_libraries(cplex-test cplex-lib cplex-concert cplex-ilo)
	else()
		message(FATAL_ERROR "CPLEX could not be found. Cannot build CPLEX test.")
	endif()
	if (MSVC)
		set_target_properties(cplex-test PROPERTIES LINK_FLAGS /ignore:4099)
	endif()
endif()
