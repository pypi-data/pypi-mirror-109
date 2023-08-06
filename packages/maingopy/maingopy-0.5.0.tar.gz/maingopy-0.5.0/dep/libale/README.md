# libALE - a library for algebraic logical expression trees

## About

libALE is a C++ library designed to work with mathematical programs (MPs) and consists of three main components:

1. A domain specific language (DSL) for the representation of MPs in an intuitive fashion
2. A flat-hierarchy data structure with symbol-table management for user-defined identifiers
3. An extensible set of operations, implemented using the visitor pattern

## Installation

For compilation, a compiler supporting `C++17` is required.
Use the provided CMakeLists.txt in the repository root directory.

The following command sequence (for Linux) will compile the libALE library and a demo executable:

    $ mkdir build && cd build
    $ cmake ..
    $ make

An example input for the demo executable is located at `demo/input.txt`.
To run the demo executable with the provided input, run the following command sequence (from the build directory):

    $ cp ../demo/input.txt .
    $ ./ale_demo
