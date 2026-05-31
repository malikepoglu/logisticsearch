#include <array>
#include <cstddef>
#include <string_view>

#include "logisticsearch_cpp_runtime/byte_metrics.hpp"

namespace {

int expect_true(bool condition, int code) {
    return condition ? 0 : code;
}

}  // namespace

int main() {
    {
        const auto metrics = logisticsearch::cpp_runtime::analyze_string_view("ABC\n");
        if (const int rc = expect_true(metrics.byte_count == 4U, 1); rc != 0) return rc;
        if (const int rc = expect_true(metrics.zero_byte_count == 0U, 2); rc != 0) return rc;
        if (const int rc = expect_true(metrics.newline_count == 1U, 3); rc != 0) return rc;
        if (const int rc = expect_true(metrics.ascii_printable_count == 3U, 4); rc != 0) return rc;
        if (const int rc = expect_true(metrics.high_bit_byte_count == 0U, 5); rc != 0) return rc;
        if (const int rc = expect_true(metrics.fnv1a64_non_crypto == 10637522710836388947ull, 6); rc != 0) return rc;
    }

    {
        const std::array<unsigned char, 5> bytes{{0x00u, 0x41u, 0x0au, 0x80u, 0xffu}};
        const auto metrics = logisticsearch::cpp_runtime::analyze_bytes(bytes.data(), bytes.size());
        if (const int rc = expect_true(metrics.byte_count == 5U, 7); rc != 0) return rc;
        if (const int rc = expect_true(metrics.zero_byte_count == 1U, 8); rc != 0) return rc;
        if (const int rc = expect_true(metrics.newline_count == 1U, 9); rc != 0) return rc;
        if (const int rc = expect_true(metrics.ascii_printable_count == 1U, 10); rc != 0) return rc;
        if (const int rc = expect_true(metrics.high_bit_byte_count == 2U, 11); rc != 0) return rc;
        if (const int rc = expect_true(metrics.fnv1a64_non_crypto == 17377968997435760381ull, 12); rc != 0) return rc;
    }

    {
        const auto metrics = logisticsearch::cpp_runtime::analyze_bytes(nullptr, 0U);
        if (const int rc = expect_true(metrics.byte_count == 0U, 13); rc != 0) return rc;
        if (const int rc = expect_true(metrics.fnv1a64_non_crypto == 14695981039346656037ull, 14); rc != 0) return rc;
    }

    {
        const auto metrics = logisticsearch::cpp_runtime::analyze_bytes(nullptr, 3U);
        if (const int rc = expect_true(metrics.byte_count == 3U, 15); rc != 0) return rc;
        if (const int rc = expect_true(metrics.zero_byte_count == 0U, 16); rc != 0) return rc;
        if (const int rc = expect_true(metrics.fnv1a64_non_crypto == 14695981039346656037ull, 17); rc != 0) return rc;
    }

    return 0;
}
