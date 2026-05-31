#pragma once

#include <cstddef>
#include <cstdint>
#include <filesystem>

#include "logisticsearch_cpp_runtime/byte_metrics.hpp"

namespace logisticsearch::cpp_runtime {

enum class file_byte_metrics_error : std::uint8_t {
    none = 0,
    invalid_chunk_size = 1,
    path_is_not_regular_file = 2,
    open_failed = 3,
    read_failed = 4,
};

struct file_byte_metrics_result {
    bool ok = false;
    file_byte_metrics_error error_code = file_byte_metrics_error::none;
    byte_metrics metrics{};
    std::uintmax_t bytes_read = 0;
    std::size_t chunks_read = 0;
};

constexpr std::size_t min_file_byte_metrics_chunk_size = 1U;
constexpr std::size_t max_file_byte_metrics_chunk_size = 16U * 1024U * 1024U;

file_byte_metrics_result analyze_file_bytes(
    const std::filesystem::path& path,
    std::size_t chunk_size
) noexcept;

}  // namespace logisticsearch::cpp_runtime
