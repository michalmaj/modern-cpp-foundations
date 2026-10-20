#include "smoke.hpp"

#include <algorithm>
#include <format>
#include <numeric>

namespace smoke {

Summary summarize(std::span<const int> values) {
    Summary result;
    result.sum = std::accumulate(values.begin(), values.end(), 0LL);
    result.evens = static_cast<int>(std::ranges::count_if(values, [](int v) { return v % 2 == 0; }));
    if (!values.empty()) {
        result.max = std::ranges::max(values);
    }
    return result;
}

std::string describe(const Summary& summary) {
    return std::format("sum={} evens={} max={}", summary.sum, summary.evens, summary.max);
}

}  // namespace smoke
