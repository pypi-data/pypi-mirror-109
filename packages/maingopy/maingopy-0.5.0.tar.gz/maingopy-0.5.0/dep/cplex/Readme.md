This is a wrapper for IBM ILOG CPLEX.
It requires a separate CPLEX installation and merely provides the CMakeLists.txt and FindCPLEX.cmake for including it in MAiNGO.
If CPLEX is not found, a pre-processor flag will be set accordingly and MAiNGO will be compiled without CPLEX.
The current version of MAiNGO requires CPLEX versions 12.8 or 12.9.