#include "logisticsearch_c_runtime/byte_metrics.h"

#include <stddef.h>
#include <stdint.h>
#include <string.h>

#define LOGISTICSEARCH_C_FNV1A64_OFFSET_BASIS UINT64_C(14695981039346656037)
#define LOGISTICSEARCH_C_FNV1A64_PRIME UINT64_C(1099511628211)

logisticsearch_c_byte_metrics logisticsearch_c_analyze_bytes(
    const unsigned char* data,
    size_t size
) {
    logisticsearch_c_byte_metrics metrics;
    size_t index = 0u;

    memset(&metrics, 0, sizeof(metrics));
    metrics.fnv1a64_non_crypto = LOGISTICSEARCH_C_FNV1A64_OFFSET_BASIS;

    if (data == NULL && size != 0u) {
        return metrics;
    }

    for (index = 0u; index < size; ++index) {
        const unsigned char byte_value = data[index];

        ++metrics.byte_count;

        if (byte_value == 0u) {
            ++metrics.zero_byte_count;
        }

        if (byte_value == (unsigned char)'\n') {
            ++metrics.newline_count;
        }

        if (byte_value >= 0x20u && byte_value <= 0x7eu) {
            ++metrics.ascii_printable_count;
        }

        if (byte_value >= 0x80u) {
            ++metrics.high_bit_byte_count;
        }

        metrics.fnv1a64_non_crypto ^= (uint64_t)byte_value;
        metrics.fnv1a64_non_crypto *= LOGISTICSEARCH_C_FNV1A64_PRIME;
    }

    return metrics;
}
