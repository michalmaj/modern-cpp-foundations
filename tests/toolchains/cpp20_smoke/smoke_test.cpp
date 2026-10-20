#include "smoke.hpp"

#include <array>
#include <concepts>
#include <iostream>
#include <string_view>
#include <vector>

namespace {

int failures = 0;

void expect(bool ok, std::string_view what) {
    if (!ok) {
        std::cerr << "FAIL: " << what << '\n';
        ++failures;
    }
}

template <std::integral T>
constexpr T twice(T value) {
    return value * 2;
}

}  // namespace

int main() {
    constexpr std::array values{5, 3, 8, 1};
    const smoke::Summary summary = smoke::summarize(values);
    expect(summary == smoke::Summary{.sum = 17, .evens = 1, .max = 8}, "summarize({5, 3, 8, 1})");
    expect(smoke::describe(summary) == "sum=17 evens=1 max=8", "describe() formats with std::format");

    expect(smoke::summarize(std::span<const int>{}) == smoke::Summary{}, "summarize() of an empty span");

    const std::vector<int> negatives{-4, -7, -2};
    expect(smoke::summarize(negatives) == smoke::Summary{.sum = -13, .evens = 2, .max = -2},
           "summarize({-4, -7, -2})");

    static_assert(twice(21) == 42);

    if (failures != 0) {
        std::cerr << failures << " check(s) failed\n";
        return 1;
    }
    std::cout << "all checks passed\n";
    return 0;
}
