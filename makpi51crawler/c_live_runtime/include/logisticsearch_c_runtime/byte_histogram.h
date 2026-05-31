#ifndef LOGISTICSEARCH_C_RUNTIME_BYTE_HISTOGRAM_H
#define LOGISTICSEARCH_C_RUNTIME_BYTE_HISTOGRAM_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define LOGISTICSEARCH_C_BYTE_HISTOGRAM_BUCKET_COUNT 256u

typedef struct logisticsearch_c_byte_histogram {
    uint64_t buckets[LOGISTICSEARCH_C_BYTE_HISTOGRAM_BUCKET_COUNT];
    uint64_t total_count;
    uint16_t distinct_byte_count;
} logisticsearch_c_byte_histogram;

logisticsearch_c_byte_histogram logisticsearch_c_analyze_byte_histogram(
    const unsigned char* data,
    size_t size
);

#ifdef __cplusplus
}
#endif

#endif
