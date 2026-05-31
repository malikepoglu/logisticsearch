#include <stdio.h>

#include "logisticsearch_c_runtime/version.h"

int main(void) {
    printf(
        "{"
        "\"runtime\":\"%s\","
        "\"surface\":\"%s\","
        "\"version\":\"%s\","
        "\"status\":\"ok\""
        "}\n",
        logisticsearch_c_runtime_name(),
        logisticsearch_c_runtime_surface(),
        logisticsearch_c_runtime_version_string()
    );

    return 0;
}
