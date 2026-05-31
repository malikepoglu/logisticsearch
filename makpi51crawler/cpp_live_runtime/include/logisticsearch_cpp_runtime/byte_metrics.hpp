#pragma once

#include <cstddef>
#include <cstdint>
#include <string_view>

namespace logisticsearch::cpp_runtime {

struct byte_metrics {
    std::size_t byte_count = 0;
    std::size_t zero_byte_count = 0;
    std::size_t newline_count = 0;
    std::size_t ascii_printable_count = 0;
    std::size_t high_bit_byte_count = 0;
    std::uint64_t fnv1a64_non_crypto = 14695981039346656037ull;
};

byte_metrics analyze_bytes(const unsigned char* data, std::size_t size) noexcept;
byte_metrics analyze_string_view(std::string_view input) noexcept;

}  // namespace logisticsearch::cpp_runtime
