#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "logisticsearch_c_runtime/file_byte_metrics.h"

static int expect_true(int condition, int code) {
    return condition ? 0 : code;
}

static int write_bytes(const char* path, const unsigned char* data, size_t size) {
    FILE* output = fopen(path, "wb");
    size_t written = 0u;

    if (output == NULL) {
        return 0;
    }

    written = fwrite(data, 1u, size, output);

    if (fclose(output) != 0) {
        return 0;
    }

    return written == size;
}

int main(void) {
    const char* test_path = "/tmp/logisticsearch_c_file_byte_metrics_test.bin";
    const char* empty_path = "/tmp/logisticsearch_c_file_byte_metrics_empty.bin";

    {
        const unsigned char bytes[5] = {0x00u, 0x41u, 0x0au, 0x80u, 0xffu};
        const logisticsearch_c_file_byte_metrics_result result =
            (write_bytes(test_path, bytes, sizeof(bytes)) != 0)
                ? logisticsearch_c_analyze_file_bytes(test_path, 2u)
                : logisticsearch_c_analyze_file_bytes(NULL, 2u);

        int rc = 0;

        rc = expect_true(result.ok == 1, 1);
        if (rc != 0) return rc;
        rc = expect_true(result.error_code == LOGISTICSEARCH_C_FILE_BYTE_METRICS_OK, 2);
        if (rc != 0) return rc;
        rc = expect_true(result.bytes_read == 5u, 3);
        if (rc != 0) return rc;
        rc = expect_true(result.chunks_read == 3u, 4);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.byte_count == 5u, 5);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.zero_byte_count == 1u, 6);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.newline_count == 1u, 7);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.ascii_printable_count == 1u, 8);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.high_bit_byte_count == 2u, 9);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.fnv1a64_non_crypto == UINT64_C(17377968997435760381), 10);
        if (rc != 0) return rc;
    }

    {
        const unsigned char bytes[1] = {0u};
        const logisticsearch_c_file_byte_metrics_result result =
            (write_bytes(empty_path, bytes, 0u) != 0)
                ? logisticsearch_c_analyze_file_bytes(empty_path, 4096u)
                : logisticsearch_c_analyze_file_bytes(NULL, 4096u);

        int rc = 0;

        rc = expect_true(result.ok == 1, 11);
        if (rc != 0) return rc;
        rc = expect_true(result.bytes_read == 0u, 12);
        if (rc != 0) return rc;
        rc = expect_true(result.chunks_read == 0u, 13);
        if (rc != 0) return rc;
        rc = expect_true(result.metrics.fnv1a64_non_crypto == UINT64_C(14695981039346656037), 14);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_file_byte_metrics_result result =
            logisticsearch_c_analyze_file_bytes(test_path, 0u);

        int rc = 0;

        rc = expect_true(result.ok == 0, 15);
        if (rc != 0) return rc;
        rc = expect_true(result.error_code == LOGISTICSEARCH_C_FILE_BYTE_METRICS_INVALID_CHUNK_SIZE, 16);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_file_byte_metrics_result result =
            logisticsearch_c_analyze_file_bytes(test_path, LOGISTICSEARCH_C_FILE_BYTE_METRICS_MAX_CHUNK_SIZE + 1u);

        int rc = 0;

        rc = expect_true(result.ok == 0, 17);
        if (rc != 0) return rc;
        rc = expect_true(result.error_code == LOGISTICSEARCH_C_FILE_BYTE_METRICS_INVALID_CHUNK_SIZE, 18);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_file_byte_metrics_result result =
            logisticsearch_c_analyze_file_bytes("/tmp/logisticsearch_c_file_byte_metrics_missing_file.bin", 1024u);

        int rc = 0;

        rc = expect_true(result.ok == 0, 19);
        if (rc != 0) return rc;
        rc = expect_true(result.error_code == LOGISTICSEARCH_C_FILE_BYTE_METRICS_NOT_REGULAR_FILE, 20);
        if (rc != 0) return rc;
    }

    {
        const logisticsearch_c_file_byte_metrics_result result =
            logisticsearch_c_analyze_file_bytes("/tmp", 1024u);

        int rc = 0;

        rc = expect_true(result.ok == 0, 21);
        if (rc != 0) return rc;
        rc = expect_true(result.error_code == LOGISTICSEARCH_C_FILE_BYTE_METRICS_NOT_REGULAR_FILE, 22);
        if (rc != 0) return rc;
    }

    remove(test_path);
    remove(empty_path);

    return 0;
}
