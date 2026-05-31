#include <stddef.h>
#include <stdint.h>

#include "logisticsearch_c_runtime/byte_metrics.h"

static int expect_true(int condition, int code) {
    return condition ? 0 : code;
}

int main(void) {
    {
        const unsigned char bytes[5] = {0x00u, 0x41u, 0x0au, 0x80u, 0xffu};
        const logisticsearch_c_byte_metrics metrics =
            logisticsearch_c_analyze_bytes(bytes, sizeof(bytes));

        int rc = 0;

        rc = expect_true(metrics.byte_count == 5u, 1);
        if (rc != 0) return rc;
        rc = expect_true(metrics.zero_byte_count == 1u, 2);
        if (rc != 0) return rc;
        rc = expect_true(metrics.newline_count == 1u, 3);
        if (rc != 0) return rc;
        rc = expect_true(metrics.ascii_printable_count == 1u, 4);
        if (rc != 0) return rc;
        rc = expect_true(metrics.high_bit_byte_count == 2u, 5);
        if (rc != 0) return rc;
        rc = expect_true(metrics.fnv1a64_non_crypto == UINT64_C(17377968997435760381), 6);
        if (rc != 0) return rc;
    }

    {
        const unsigned char bytes[4] = {'A', 'B', 'A', '\n'};
        const logisticsearch_c_byte_metrics metrics =
            logisticsearch_c_analyze_bytes(bytes, sizeof(bytes));

        int rc = 0;

        rc = expect_true(metrics.byte_count == 4u, 7);
        if (rc != 0) return rc;
        rc = expect_true(metrics.zero_byte_count == 0u, 8);
        if (rc != 0) return rc;
        rc = expect_true(metrics.newline_count == 1u, 9);
        if (rc != 0) return rc;
        rc = expect_true(metrics.ascii_printable_count == 3u, 10);
        if (rc != 0) return rc;
        rc = expect_true(metrics.high_bit_byte_count == 0u, 11);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_byte_metrics metrics =
            logisticsearch_c_analyze_bytes(NULL, 0u);

        int rc = 0;

        rc = expect_true(metrics.byte_count == 0u, 12);
        if (rc != 0) return rc;
        rc = expect_true(metrics.fnv1a64_non_crypto == UINT64_C(14695981039346656037), 13);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_byte_metrics metrics =
            logisticsearch_c_analyze_bytes(NULL, 5u);

        int rc = 0;

        rc = expect_true(metrics.byte_count == 0u, 14);
        if (rc != 0) return rc;
        rc = expect_true(metrics.fnv1a64_non_crypto == UINT64_C(14695981039346656037), 15);
        if (rc != 0) return rc;
    }

    return 0;
}
