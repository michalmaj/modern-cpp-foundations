#include "smoke.hpp"

#include <array>
#include <cassert>
#include <iostream>
#include <version>

static_assert(__cplusplus >= 202002L, "this project must be compiled as C++20");

int main() {
    constexpr std::array values{5, 3, 8, 1};
    const smoke::Summary summary = smoke::summarize(values);
    assert(summary.sum == 17);  // compiled in Debug, removed in Release (NDEBUG)

#ifdef NDEBUG
    const char* assertions = "off";
#else
    const char* assertions = "on";
#endif
    std::cout << "summary: " << smoke::describe(summary) << " assertions=" << assertions << '\n';

    // Which toolchain built this program, for the log.
    std::cout << "compiler: clang " << __clang_version__ << '\n';
#if defined(_LIBCPP_VERSION)
    std::cout << "standard library: libc++ " << _LIBCPP_VERSION << '\n';
#elif defined(_GLIBCXX_RELEASE)
    std::cout << "standard library: libstdc++ " << _GLIBCXX_RELEASE << " (" << __GLIBCXX__ << ")\n";
#elif defined(_MSVC_STL_VERSION)
    std::cout << "standard library: MSVC STL " << _MSVC_STL_VERSION << " (update " << _MSVC_STL_UPDATE << ")\n";
#else
    std::cout << "standard library: unknown\n";
#endif
    std::cout << "__cplusplus: " << __cplusplus << '\n';
}
