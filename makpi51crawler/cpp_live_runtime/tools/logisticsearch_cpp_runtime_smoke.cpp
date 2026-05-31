#include <iostream>

#include "logisticsearch_cpp_runtime/version.hpp"

int main() {
    std::cout
        << "{"
        << "\"runtime\":\"" << logisticsearch::cpp_runtime::runtime_name() << "\","
        << "\"surface\":\"" << logisticsearch::cpp_runtime::runtime_surface() << "\","
        << "\"version\":\"" << logisticsearch::cpp_runtime::version_string() << "\","
        << "\"status\":\"ok\""
        << "}"
        << '\n';

    return 0;
}
