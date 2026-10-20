cmake_minimum_required(VERSION 3.28)
project(cpp20_toolchain_smoke LANGUAGES CXX)

# This project verifies the official course toolchain: upstream LLVM/Clang 22
# or newer, used through the GNU-style clang++ driver (on Windows: targeting
# the MSVC ABI). Configuration stops with an error for any other compiler, so a
# green run can never come from a silent fallback to GCC, AppleClang, MSVC,
# clang-cl or MinGW.
if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    message(FATAL_ERROR
        "Expected upstream LLVM Clang, but CMake found ${CMAKE_CXX_COMPILER_ID} "
        "(${CMAKE_CXX_COMPILER}). Pass -DCMAKE_CXX_COMPILER=<path to upstream clang++>.")
endif()
if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS 22)
    message(FATAL_ERROR "Expected Clang 22 or newer, but found ${CMAKE_CXX_COMPILER_VERSION}.")
endif()
if(NOT CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "GNU")
    message(FATAL_ERROR
        "Expected the clang++ driver, but found the ${CMAKE_CXX_COMPILER_FRONTEND_VARIANT} "
        "command-line style (clang-cl?).")
endif()
if(WIN32 AND NOT CMAKE_CXX_SIMULATE_ID STREQUAL "MSVC")
    message(FATAL_ERROR
        "Expected clang++ targeting the MSVC ABI on Windows, but the compiler simulates "
        "'${CMAKE_CXX_SIMULATE_ID}' (MinGW?).")
endif()

# A small static library, a program and a test program: this exercises the
# compiler, the archiver and the linker, not just a single source file.
add_library(smoke STATIC smoke.cpp)
target_compile_features(smoke PUBLIC cxx_std_20)
target_include_directories(smoke PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(cpp20_smoke main.cpp)
target_link_libraries(cpp20_smoke PRIVATE smoke)

add_executable(smoke_test smoke_test.cpp)
target_link_libraries(smoke_test PRIVATE smoke)

set_target_properties(smoke cpp20_smoke smoke_test PROPERTIES CXX_EXTENSIONS OFF)

enable_testing()

# Unit-level checks of the library; fails with a message for each wrong result.
add_test(NAME smoke_test COMMAND smoke_test)

# The program's output, including whether assertions are compiled in. Release
# defines NDEBUG and Debug does not, so this proves which configuration was built.
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    set(expected_assertions off)
else()
    set(expected_assertions on)
endif()
add_test(NAME program_output COMMAND cpp20_smoke)
set_tests_properties(program_output PROPERTIES
    PASS_REGULAR_EXPRESSION "summary: sum=17 evens=1 max=8 assertions=${expected_assertions}")
