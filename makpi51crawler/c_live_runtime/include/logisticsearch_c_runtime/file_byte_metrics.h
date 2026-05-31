#ifndef LOGISTICSEARCH_C_RUNTIME_FILE_BYTE_METRICS_H
#define LOGISTICSEARCH_C_RUNTIME_FILE_BYTE_METRICS_H

#include <stddef.h>
#include <stdint.h>

#include "logisticsearch_c_runtime/byte_metrics.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum logisticsearch_c_file_byte_metrics_error {
    LOGISTICSEARCH_C_FILE_BYTE_METRICS_OK = 0,
    LOGISTICSEARCH_C_FILE_BYTE_METRICS_INVALID_CHUNK_SIZE = 1,
    LOGISTICSEARCH_C_FILE_BYTE_METRICS_NOT_REGULAR_FILE = 2,
    LOGISTICSEARCH_C_FILE_BYTE_METRICS_OPEN_FAILED = 3,
    LOGISTICSEARCH_C_FILE_BYTE_METRICS_READ_FAILED = 4,
    LOGISTICSEARCH_C_FILE_BYTE_METRICS_MEMORY_FAILED = 5
} logisticsearch_c_file_byte_metrics_error;

typedef struct logisticsearch_c_file_byte_metrics_result {
    int ok;
    logisticsearch_c_file_byte_metrics_error error_code;
    logisticsearch_c_byte_metrics metrics;
    uintmax_t bytes_read;
    size_t chunks_read;
} logisticsearch_c_file_byte_metrics_result;

#define LOGISTICSEARCH_C_FILE_BYTE_METRICS_MIN_CHUNK_SIZE 1u
#define LOGISTICSEARCH_C_FILE_BYTE_METRICS_MAX_CHUNK_SIZE (16u * 1024u * 1024u)

logisticsearch_c_file_byte_metrics_result logisticsearch_c_analyze_file_bytes(
    const char* path,
    size_t chunk_size
);

#ifdef __cplusplus
}
#endif

#endif
