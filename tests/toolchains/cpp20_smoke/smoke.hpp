#pragma once

#include <compare>
#include <span>
#include <string>

namespace smoke {

struct Summary {
    long long sum = 0;
    int evens = 0;
    int max = 0;

    auto operator<=>(const Summary&) const = default;
};

// Sum, number of even values and largest value; an empty span gives Summary{}.
Summary summarize(std::span<const int> values);

// "sum=<sum> evens=<evens> max=<max>", formatted with std::format.
std::string describe(const Summary& summary);

}  // namespace smoke
