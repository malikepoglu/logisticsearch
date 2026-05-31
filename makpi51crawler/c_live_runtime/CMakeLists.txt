cmake_minimum_required(VERSION 3.16)

project(logisticsearch_c_live_runtime
    VERSION 0.1.0
    DESCRIPTION "LogisticSearch isolated C live runtime surface"
    LANGUAGES C
)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_library(logisticsearch_c_runtime STATIC
    src/version.c
    src/byte_histogram.c
)

target_include_directories(logisticsearch_c_runtime
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_options(logisticsearch_c_runtime
    PRIVATE
        -Wall
        -Wextra
        -Wpedantic
)

add_executable(logisticsearch_c_runtime_smoke
    tools/logisticsearch_c_runtime_smoke.c
)

target_link_libraries(logisticsearch_c_runtime_smoke
    PRIVATE
        logisticsearch_c_runtime
)

enable_testing()

add_executable(logisticsearch_c_runtime_version_test
    tests/test_version_smoke.c
)

target_link_libraries(logisticsearch_c_runtime_version_test
    PRIVATE
        logisticsearch_c_runtime
)

add_test(
    NAME logisticsearch_c_runtime_version_smoke
    COMMAND logisticsearch_c_runtime_version_test
)

add_executable(logisticsearch_c_runtime_byte_histogram_test
    tests/test_byte_histogram.c
)

target_link_libraries(logisticsearch_c_runtime_byte_histogram_test
    PRIVATE
        logisticsearch_c_runtime
)

add_test(
    NAME logisticsearch_c_runtime_byte_histogram
    COMMAND logisticsearch_c_runtime_byte_histogram_test
)
