#include "logisticsearch_cpp_runtime/byte_histogram.hpp"

namespace logisticsearch::cpp_runtime {
namespace {

void finalize_distinct_count(byte_histogram& histogram) noexcept {
    std::uint16_t distinct = 0;

    for (const auto count : histogram.buckets) {
        if (count != 0U) {
            ++distinct;
        }
    }

    histogram.distinct_byte_count = distinct;
}

}  // namespace

byte_histogram analyze_byte_histogram(
    const unsigned char* data,
    std::size_t size
) noexcept {
    byte_histogram histogram{};

    if (data == nullptr && size != 0U) {
        return histogram;
    }

    for (std::size_t index = 0; index < size; ++index) {
        const auto byte_value = static_cast<std::size_t>(data[index]);
        ++histogram.buckets[byte_value];
        ++histogram.total_count;
    }

    finalize_distinct_count(histogram);
    return histogram;
}

byte_histogram analyze_string_view_histogram(std::string_view input) noexcept {
    const auto* data = reinterpret_cast<const unsigned char*>(input.data());
    return analyze_byte_histogram(data, input.size());
}

}  // namespace logisticsearch::cpp_runtime
