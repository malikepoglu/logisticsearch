#include "logisticsearch_cpp_runtime/file_byte_metrics.hpp"

#include <fstream>
#include <ios>
#include <system_error>
#include <vector>

namespace logisticsearch::cpp_runtime {
namespace {

constexpr std::uint64_t fnv1a64_offset_basis = 14695981039346656037ull;
constexpr std::uint64_t fnv1a64_prime = 1099511628211ull;

void update_full_stream_fnv1a64(
    byte_metrics& metrics,
    const unsigned char* data,
    std::size_t size
) noexcept {
    if (data == nullptr && size != 0U) {
        return;
    }

    for (std::size_t index = 0; index < size; ++index) {
        metrics.fnv1a64_non_crypto ^= static_cast<std::uint64_t>(data[index]);
        metrics.fnv1a64_non_crypto *= fnv1a64_prime;
    }
}

void merge_chunk_metrics(
    byte_metrics& total,
    const byte_metrics& chunk,
    const unsigned char* data,
    std::size_t size
) noexcept {
    total.byte_count += chunk.byte_count;
    total.zero_byte_count += chunk.zero_byte_count;
    total.newline_count += chunk.newline_count;
    total.ascii_printable_count += chunk.ascii_printable_count;
    total.high_bit_byte_count += chunk.high_bit_byte_count;

    update_full_stream_fnv1a64(total, data, size);
}

bool valid_chunk_size(std::size_t chunk_size) noexcept {
    return chunk_size >= min_file_byte_metrics_chunk_size &&
        chunk_size <= max_file_byte_metrics_chunk_size;
}

}  // namespace

file_byte_metrics_result analyze_file_bytes(
    const std::filesystem::path& path,
    std::size_t chunk_size
) noexcept {
    file_byte_metrics_result result{};
    result.metrics.fnv1a64_non_crypto = fnv1a64_offset_basis;

    if (!valid_chunk_size(chunk_size)) {
        result.error_code = file_byte_metrics_error::invalid_chunk_size;
        return result;
    }

    try {
        std::error_code filesystem_error{};
        if (!std::filesystem::is_regular_file(path, filesystem_error) || filesystem_error) {
            result.error_code = file_byte_metrics_error::path_is_not_regular_file;
            return result;
        }

        std::ifstream input(path, std::ios::binary);
        if (!input.is_open()) {
            result.error_code = file_byte_metrics_error::open_failed;
            return result;
        }

        std::vector<unsigned char> buffer(chunk_size);

        while (input) {
            input.read(
                reinterpret_cast<char*>(buffer.data()),
                static_cast<std::streamsize>(buffer.size())
            );

            const std::streamsize read_count = input.gcount();
            if (read_count > 0) {
                const auto actual_read = static_cast<std::size_t>(read_count);
                const auto chunk = analyze_bytes(buffer.data(), actual_read);

                merge_chunk_metrics(result.metrics, chunk, buffer.data(), actual_read);
                result.bytes_read += static_cast<std::uintmax_t>(actual_read);
                ++result.chunks_read;
            }

            if (input.bad()) {
                result.error_code = file_byte_metrics_error::read_failed;
                return result;
            }
        }

        result.ok = true;
        result.error_code = file_byte_metrics_error::none;
        return result;
    } catch (...) {
        result.ok = false;
        result.error_code = file_byte_metrics_error::read_failed;
        return result;
    }
}

}  // namespace logisticsearch::cpp_runtime
