#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <string_view>

namespace logisticsearch::cpp_runtime {

struct byte_histogram {
    std::array<std::uint64_t, 256> buckets{};
    std::uint64_t total_count = 0;
    std::uint16_t distinct_byte_count = 0;
};

byte_histogram analyze_byte_histogram(
    const unsigned char* data,
    std::size_t size
) noexcept;

byte_histogram analyze_string_view_histogram(std::string_view input) noexcept;

}  // namespace logisticsearch::cpp_runtime
