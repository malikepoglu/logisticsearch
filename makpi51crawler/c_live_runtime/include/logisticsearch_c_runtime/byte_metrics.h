#ifndef LOGISTICSEARCH_C_RUNTIME_BYTE_METRICS_H
#define LOGISTICSEARCH_C_RUNTIME_BYTE_METRICS_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct logisticsearch_c_byte_metrics {
    uint64_t byte_count;
    uint64_t zero_byte_count;
    uint64_t newline_count;
    uint64_t ascii_printable_count;
    uint64_t high_bit_byte_count;
    uint64_t fnv1a64_non_crypto;
} logisticsearch_c_byte_metrics;

logisticsearch_c_byte_metrics logisticsearch_c_analyze_bytes(
    const unsigned char* data,
    size_t size
);

#ifdef __cplusplus
}
#endif

#endif
