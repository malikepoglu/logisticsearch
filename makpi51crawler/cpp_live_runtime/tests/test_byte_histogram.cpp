#include <array>
#include <cstddef>
#include <string_view>

#include "logisticsearch_cpp_runtime/byte_histogram.hpp"

namespace {

int expect_true(bool condition, int code) {
    return condition ? 0 : code;
}

}  // namespace

int main() {
    {
        const std::array<unsigned char, 6> bytes{{0x00u, 0x00u, 0x0au, 0x41u, 0x41u, 0xffu}};
        const auto histogram = logisticsearch::cpp_runtime::analyze_byte_histogram(bytes.data(), bytes.size());

        if (const int rc = expect_true(histogram.total_count == 6U, 1); rc != 0) return rc;
        if (const int rc = expect_true(histogram.distinct_byte_count == 4U, 2); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[0x00u] == 2U, 3); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[0x0au] == 1U, 4); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[0x41u] == 2U, 5); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[0xffu] == 1U, 6); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[0x42u] == 0U, 7); rc != 0) return rc;
    }

    {
        constexpr std::string_view sample = "ABA\n";
        const auto histogram = logisticsearch::cpp_runtime::analyze_string_view_histogram(sample);

        if (const int rc = expect_true(histogram.total_count == 4U, 8); rc != 0) return rc;
        if (const int rc = expect_true(histogram.distinct_byte_count == 3U, 9); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[static_cast<unsigned char>('A')] == 2U, 10); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[static_cast<unsigned char>('B')] == 1U, 11); rc != 0) return rc;
        if (const int rc = expect_true(histogram.buckets[static_cast<unsigned char>('\n')] == 1U, 12); rc != 0) return rc;
    }

    {
        const auto histogram = logisticsearch::cpp_runtime::analyze_byte_histogram(nullptr, 0U);

        if (const int rc = expect_true(histogram.total_count == 0U, 13); rc != 0) return rc;
        if (const int rc = expect_true(histogram.distinct_byte_count == 0U, 14); rc != 0) return rc;
    }

    {
        const auto histogram = logisticsearch::cpp_runtime::analyze_byte_histogram(nullptr, 5U);

        if (const int rc = expect_true(histogram.total_count == 0U, 15); rc != 0) return rc;
        if (const int rc = expect_true(histogram.distinct_byte_count == 0U, 16); rc != 0) return rc;
    }

    return 0;
}
