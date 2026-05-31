#include <array>
#include <cstddef>
#include <filesystem>
#include <fstream>

#include "logisticsearch_cpp_runtime/file_byte_metrics.hpp"

namespace {

int expect_true(bool condition, int code) {
    return condition ? 0 : code;
}

bool write_bytes(const std::filesystem::path& path, const unsigned char* data, std::size_t size) {
    std::ofstream output(path, std::ios::binary | std::ios::trunc);
    if (!output.is_open()) {
        return false;
    }

    output.write(reinterpret_cast<const char*>(data), static_cast<std::streamsize>(size));
    return output.good();
}

}  // namespace

int main() {
    const auto temp_root = std::filesystem::temp_directory_path();
    const auto test_path = temp_root / "logisticsearch_file_byte_metrics_test.bin";
    const auto empty_path = temp_root / "logisticsearch_file_byte_metrics_empty.bin";

    {
        const std::array<unsigned char, 5> bytes{{0x00u, 0x41u, 0x0au, 0x80u, 0xffu}};
        if (const int rc = expect_true(write_bytes(test_path, bytes.data(), bytes.size()), 1); rc != 0) return rc;

        const auto result = logisticsearch::cpp_runtime::analyze_file_bytes(test_path, 2U);
        if (const int rc = expect_true(result.ok, 2); rc != 0) return rc;
        if (const int rc = expect_true(result.error_code == logisticsearch::cpp_runtime::file_byte_metrics_error::none, 3); rc != 0) return rc;
        if (const int rc = expect_true(result.bytes_read == 5U, 4); rc != 0) return rc;
        if (const int rc = expect_true(result.chunks_read == 3U, 5); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.byte_count == 5U, 6); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.zero_byte_count == 1U, 7); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.newline_count == 1U, 8); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.ascii_printable_count == 1U, 9); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.high_bit_byte_count == 2U, 10); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.fnv1a64_non_crypto == 17377968997435760381ull, 11); rc != 0) return rc;
    }

    {
        const std::array<unsigned char, 0> bytes{};
        if (const int rc = expect_true(write_bytes(empty_path, bytes.data(), bytes.size()), 12); rc != 0) return rc;

        const auto result = logisticsearch::cpp_runtime::analyze_file_bytes(empty_path, 4096U);
        if (const int rc = expect_true(result.ok, 13); rc != 0) return rc;
        if (const int rc = expect_true(result.bytes_read == 0U, 14); rc != 0) return rc;
        if (const int rc = expect_true(result.chunks_read == 0U, 15); rc != 0) return rc;
        if (const int rc = expect_true(result.metrics.fnv1a64_non_crypto == 14695981039346656037ull, 16); rc != 0) return rc;
    }

    {
        const auto result = logisticsearch::cpp_runtime::analyze_file_bytes(test_path, 0U);
        if (const int rc = expect_true(!result.ok, 17); rc != 0) return rc;
        if (const int rc = expect_true(result.error_code == logisticsearch::cpp_runtime::file_byte_metrics_error::invalid_chunk_size, 18); rc != 0) return rc;
    }

    {
        const auto result = logisticsearch::cpp_runtime::analyze_file_bytes(test_path, logisticsearch::cpp_runtime::max_file_byte_metrics_chunk_size + 1U);
        if (const int rc = expect_true(!result.ok, 19); rc != 0) return rc;
        if (const int rc = expect_true(result.error_code == logisticsearch::cpp_runtime::file_byte_metrics_error::invalid_chunk_size, 20); rc != 0) return rc;
    }

    {
        const auto missing_path = temp_root / "logisticsearch_file_byte_metrics_missing_file.bin";
        std::filesystem::remove(missing_path);
        const auto result = logisticsearch::cpp_runtime::analyze_file_bytes(missing_path, 1024U);
        if (const int rc = expect_true(!result.ok, 21); rc != 0) return rc;
        if (const int rc = expect_true(result.error_code == logisticsearch::cpp_runtime::file_byte_metrics_error::path_is_not_regular_file, 22); rc != 0) return rc;
    }

    {
        const auto result = logisticsearch::cpp_runtime::analyze_file_bytes(temp_root, 1024U);
        if (const int rc = expect_true(!result.ok, 23); rc != 0) return rc;
        if (const int rc = expect_true(result.error_code == logisticsearch::cpp_runtime::file_byte_metrics_error::path_is_not_regular_file, 24); rc != 0) return rc;
    }

    std::filesystem::remove(test_path);
    std::filesystem::remove(empty_path);

    return 0;
}
