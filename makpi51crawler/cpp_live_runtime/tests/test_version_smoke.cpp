#include <cstring>

#include "logisticsearch_cpp_runtime/version.hpp"

int main() {
    if (std::strcmp(logisticsearch::cpp_runtime::runtime_name(), "logisticsearch_cpp_live_runtime") != 0) {
        return 1;
    }

    if (std::strcmp(logisticsearch::cpp_runtime::runtime_surface(), "makpi51crawler/cpp_live_runtime") != 0) {
        return 2;
    }

    if (std::strcmp(logisticsearch::cpp_runtime::version_string(), "0.1.0") != 0) {
        return 3;
    }

    if (logisticsearch::cpp_runtime::version_major() != 0) {
        return 4;
    }

    if (logisticsearch::cpp_runtime::version_minor() != 1) {
        return 5;
    }

    if (logisticsearch::cpp_runtime::version_patch() != 0) {
        return 6;
    }

    return 0;
}
