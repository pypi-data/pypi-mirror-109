cmake_minimum_required(VERSION 3.8 FATAL_ERROR)

set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)

##########
# libALE project
##########

message("Checking files for libALE.")
project(ale)

##########
# Library target
##########

add_library(ale STATIC
    ${PROJECT_SOURCE_DIR}/src/lexer.cpp
    ${PROJECT_SOURCE_DIR}/src/token_buffer.cpp
    ${PROJECT_SOURCE_DIR}/src/parser.cpp

)
target_include_directories(ale
    PUBLIC ${PROJECT_SOURCE_DIR}/src
)
set_target_properties(ale
        PROPERTIES CXX_STANDARD 17
)
if(MSVC)
    message(STATUS "Detected MSVC: using compile flag /bigobj")
    target_compile_options(ale
        PUBLIC /bigobj
    )
    message(STATUS "Detected MSVC: using compile definitions _USE_MATH_DEFINES")
    add_compile_definitions(_USE_MATH_DEFINES)
endif()

##########
# Demo target
##########

if(CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
    add_library(ale_test STATIC
        ${PROJECT_SOURCE_DIR}/src/config.cpp
        ${PROJECT_SOURCE_DIR}/src/helper.cpp
        ${PROJECT_SOURCE_DIR}/src/tensor.cpp
        ${PROJECT_SOURCE_DIR}/src/value.cpp
        ${PROJECT_SOURCE_DIR}/src/node.cpp
        ${PROJECT_SOURCE_DIR}/src/expression.cpp
        ${PROJECT_SOURCE_DIR}/src/symbol.cpp
        ${PROJECT_SOURCE_DIR}/src/symbol_printer.cpp
        ${PROJECT_SOURCE_DIR}/src/symbol_table.cpp
        ${PROJECT_SOURCE_DIR}/src/token.cpp
        ${PROJECT_SOURCE_DIR}/src/util/evaluator.cpp
    )
    target_include_directories(ale_test
        PUBLIC ${PROJECT_SOURCE_DIR}/src
    )
    set_target_properties(ale_test
        PROPERTIES CXX_STANDARD 17
    )
    add_executable(ale_demo ${PROJECT_SOURCE_DIR}/demo/src/main.cpp)
    target_include_directories(ale_demo
        PRIVATE ${PROJECT_SOURCE_DIR}/demo/src
    )
    set_target_properties(ale_demo
        PROPERTIES CXX_STANDARD 17
    )
    target_link_libraries(ale_demo ale ale_test)
endif()