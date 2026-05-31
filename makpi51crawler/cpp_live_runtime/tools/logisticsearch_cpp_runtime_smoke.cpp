#include <iostream>
#include <string_view>

#include "logisticsearch_cpp_runtime/byte_metrics.hpp"
#include "logisticsearch_cpp_runtime/version.hpp"

int main() {
    constexpr std::string_view sample = "LogisticSearch\n";
    const auto metrics = logisticsearch::cpp_runtime::analyze_string_view(sample);

    std::cout
        << "{"
        << "\"runtime\":\"" << logisticsearch::cpp_runtime::runtime_name() << "\","
        << "\"surface\":\"" << logisticsearch::cpp_runtime::runtime_surface() << "\","
        << "\"version\":\"" << logisticsearch::cpp_runtime::version_string() << "\","
        << "\"byte_metrics_sample_bytes\":" << metrics.byte_count << ","
        << "\"byte_metrics_sample_newlines\":" << metrics.newline_count << ","
        << "\"status\":\"ok\""
        << "}"
        << '\n';

    return 0;
}
