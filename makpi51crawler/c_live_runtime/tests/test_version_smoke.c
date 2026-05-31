#include <string.h>

#include "logisticsearch_c_runtime/version.h"

int main(void) {
    if (strcmp(logisticsearch_c_runtime_name(), "logisticsearch_c_live_runtime") != 0) {
        return 1;
    }

    if (strcmp(logisticsearch_c_runtime_surface(), "makpi51crawler/c_live_runtime") != 0) {
        return 2;
    }

    if (strcmp(logisticsearch_c_runtime_version_string(), "0.1.0") != 0) {
        return 3;
    }

    if (logisticsearch_c_runtime_version_major() != 0) {
        return 4;
    }

    if (logisticsearch_c_runtime_version_minor() != 1) {
        return 5;
    }

    if (logisticsearch_c_runtime_version_patch() != 0) {
        return 6;
    }

    return 0;
}
