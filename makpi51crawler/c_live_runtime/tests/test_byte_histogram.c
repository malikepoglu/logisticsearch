#include <stddef.h>
#include <stdint.h>

#include "logisticsearch_c_runtime/byte_histogram.h"

static int expect_true(int condition, int code) {
    return condition ? 0 : code;
}

int main(void) {
    {
        const unsigned char bytes[6] = {0x00u, 0x00u, 0x0au, 0x41u, 0x41u, 0xffu};
        const logisticsearch_c_byte_histogram histogram =
            logisticsearch_c_analyze_byte_histogram(bytes, sizeof(bytes));

        int rc = 0;

        rc = expect_true(histogram.total_count == 6u, 1);
        if (rc != 0) return rc;
        rc = expect_true(histogram.distinct_byte_count == 4u, 2);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[0x00u] == 2u, 3);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[0x0au] == 1u, 4);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[0x41u] == 2u, 5);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[0xffu] == 1u, 6);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[0x42u] == 0u, 7);
        if (rc != 0) return rc;
    }

    {
        const unsigned char bytes[4] = {'A', 'B', 'A', '\n'};
        const logisticsearch_c_byte_histogram histogram =
            logisticsearch_c_analyze_byte_histogram(bytes, sizeof(bytes));

        int rc = 0;

        rc = expect_true(histogram.total_count == 4u, 8);
        if (rc != 0) return rc;
        rc = expect_true(histogram.distinct_byte_count == 3u, 9);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[(unsigned char)'A'] == 2u, 10);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[(unsigned char)'B'] == 1u, 11);
        if (rc != 0) return rc;
        rc = expect_true(histogram.buckets[(unsigned char)'\n'] == 1u, 12);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_byte_histogram histogram =
            logisticsearch_c_analyze_byte_histogram(NULL, 0u);

        int rc = 0;

        rc = expect_true(histogram.total_count == 0u, 13);
        if (rc != 0) return rc;
        rc = expect_true(histogram.distinct_byte_count == 0u, 14);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_byte_histogram histogram =
            logisticsearch_c_analyze_byte_histogram(NULL, 5u);

        int rc = 0;

        rc = expect_true(histogram.total_count == 0u, 15);
        if (rc != 0) return rc;
        rc = expect_true(histogram.distinct_byte_count == 0u, 16);
        if (rc != 0) return rc;
    }

    return 0;
}
