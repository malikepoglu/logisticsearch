#include "logisticsearch_c_runtime/byte_histogram.h"

#include <stddef.h>
#include <stdint.h>
#include <string.h>

static void logisticsearch_c_byte_histogram_finalize_distinct_count(
    logisticsearch_c_byte_histogram* histogram
) {
    uint16_t distinct = 0u;
    size_t index = 0u;

    if (histogram == NULL) {
        return;
    }

    for (index = 0u; index < LOGISTICSEARCH_C_BYTE_HISTOGRAM_BUCKET_COUNT; ++index) {
        if (histogram->buckets[index] != 0u) {
            ++distinct;
        }
    }

    histogram->distinct_byte_count = distinct;
}

logisticsearch_c_byte_histogram logisticsearch_c_analyze_byte_histogram(
    const unsigned char* data,
    size_t size
) {
    logisticsearch_c_byte_histogram histogram;
    size_t index = 0u;

    memset(&histogram, 0, sizeof(histogram));

    if (data == NULL && size != 0u) {
        return histogram;
    }

    for (index = 0u; index < size; ++index) {
        const size_t byte_value = (size_t)data[index];
        ++histogram.buckets[byte_value];
        ++histogram.total_count;
    }

    logisticsearch_c_byte_histogram_finalize_distinct_count(&histogram);
    return histogram;
}
