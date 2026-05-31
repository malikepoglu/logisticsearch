#include "logisticsearch_c_runtime/file_byte_metrics.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#define LOGISTICSEARCH_C_FNV1A64_OFFSET_BASIS UINT64_C(14695981039346656037)
#define LOGISTICSEARCH_C_FNV1A64_PRIME UINT64_C(1099511628211)

static int logisticsearch_c_file_byte_metrics_valid_chunk_size(size_t chunk_size) {
    return chunk_size >= LOGISTICSEARCH_C_FILE_BYTE_METRICS_MIN_CHUNK_SIZE &&
        chunk_size <= LOGISTICSEARCH_C_FILE_BYTE_METRICS_MAX_CHUNK_SIZE;
}

static void logisticsearch_c_file_byte_metrics_update_fnv(
    logisticsearch_c_byte_metrics* metrics,
    const unsigned char* data,
    size_t size
) {
    size_t index = 0u;

    if (metrics == NULL || (data == NULL && size != 0u)) {
        return;
    }

    for (index = 0u; index < size; ++index) {
        metrics->fnv1a64_non_crypto ^= (uint64_t)data[index];
        metrics->fnv1a64_non_crypto *= LOGISTICSEARCH_C_FNV1A64_PRIME;
    }
}

static void logisticsearch_c_file_byte_metrics_merge_chunk(
    logisticsearch_c_byte_metrics* total,
    const logisticsearch_c_byte_metrics* chunk,
    const unsigned char* data,
    size_t size
) {
    if (total == NULL || chunk == NULL) {
        return;
    }

    total->byte_count += chunk->byte_count;
    total->zero_byte_count += chunk->zero_byte_count;
    total->newline_count += chunk->newline_count;
    total->ascii_printable_count += chunk->ascii_printable_count;
    total->high_bit_byte_count += chunk->high_bit_byte_count;

    logisticsearch_c_file_byte_metrics_update_fnv(total, data, size);
}

logisticsearch_c_file_byte_metrics_result logisticsearch_c_analyze_file_bytes(
    const char* path,
    size_t chunk_size
) {
    logisticsearch_c_file_byte_metrics_result result;
    struct stat path_stat;
    FILE* input = NULL;
    unsigned char* buffer = NULL;

    memset(&result, 0, sizeof(result));
    result.metrics.fnv1a64_non_crypto = LOGISTICSEARCH_C_FNV1A64_OFFSET_BASIS;

    if (!logisticsearch_c_file_byte_metrics_valid_chunk_size(chunk_size)) {
        result.error_code = LOGISTICSEARCH_C_FILE_BYTE_METRICS_INVALID_CHUNK_SIZE;
        return result;
    }

    if (path == NULL || stat(path, &path_stat) != 0 || !S_ISREG(path_stat.st_mode)) {
        result.error_code = LOGISTICSEARCH_C_FILE_BYTE_METRICS_NOT_REGULAR_FILE;
        return result;
    }

    input = fopen(path, "rb");
    if (input == NULL) {
        result.error_code = LOGISTICSEARCH_C_FILE_BYTE_METRICS_OPEN_FAILED;
        return result;
    }

    buffer = (unsigned char*)malloc(chunk_size);
    if (buffer == NULL) {
        fclose(input);
        result.error_code = LOGISTICSEARCH_C_FILE_BYTE_METRICS_MEMORY_FAILED;
        return result;
    }

    for (;;) {
        const size_t read_count = fread(buffer, 1u, chunk_size, input);

        if (read_count > 0u) {
            const logisticsearch_c_byte_metrics chunk =
                logisticsearch_c_analyze_bytes(buffer, read_count);

            logisticsearch_c_file_byte_metrics_merge_chunk(&result.metrics, &chunk, buffer, read_count);
            result.bytes_read += (uintmax_t)read_count;
            ++result.chunks_read;
        }

        if (read_count < chunk_size) {
            if (ferror(input)) {
                free(buffer);
                fclose(input);
                result.ok = 0;
                result.error_code = LOGISTICSEARCH_C_FILE_BYTE_METRICS_READ_FAILED;
                return result;
            }

            break;
        }
    }

    free(buffer);
    fclose(input);

    result.ok = 1;
    result.error_code = LOGISTICSEARCH_C_FILE_BYTE_METRICS_OK;
    return result;
}
