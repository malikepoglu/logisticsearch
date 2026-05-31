#include "logisticsearch_cpp_runtime/byte_metrics.hpp"

namespace logisticsearch::cpp_runtime {
namespace {

constexpr std::uint64_t fnv1a64_offset_basis = 14695981039346656037ull;
constexpr std::uint64_t fnv1a64_prime = 1099511628211ull;

constexpr bool is_ascii_printable(unsigned char value) noexcept {
    return value >= 0x20u && value <= 0x7eu;
}

}  // namespace

byte_metrics analyze_bytes(const unsigned char* data, std::size_t size) noexcept {
    byte_metrics result{};
    result.byte_count = size;
    result.fnv1a64_non_crypto = fnv1a64_offset_basis;

    if (data == nullptr && size != 0U) {
        return result;
    }

    for (std::size_t index = 0; index < size; ++index) {
        const unsigned char value = data[index];

        if (value == 0U) {
            ++result.zero_byte_count;
        }

        if (value == static_cast<unsigned char>('\n')) {
            ++result.newline_count;
        }

        if (is_ascii_printable(value)) {
            ++result.ascii_printable_count;
        }

        if ((value & 0x80u) != 0U) {
            ++result.high_bit_byte_count;
        }

        result.fnv1a64_non_crypto ^= static_cast<std::uint64_t>(value);
        result.fnv1a64_non_crypto *= fnv1a64_prime;
    }

    return result;
}

byte_metrics analyze_string_view(std::string_view input) noexcept {
    const auto* data = reinterpret_cast<const unsigned char*>(input.data());
    return analyze_bytes(data, input.size());
}

}  // namespace logisticsearch::cpp_runtime
