cmake_minimum_required(VERSION 3.16)

project(logisticsearch_cpp_live_runtime
    VERSION 0.1.0
    DESCRIPTION "LogisticSearch isolated C++ live runtime surface"
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(logisticsearch_cpp_runtime STATIC
    src/version.cpp
)

target_include_directories(logisticsearch_cpp_runtime
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_options(logisticsearch_cpp_runtime
    PRIVATE
        -Wall
        -Wextra
        -Wpedantic
)

add_executable(logisticsearch_cpp_runtime_smoke
    tools/logisticsearch_cpp_runtime_smoke.cpp
)

target_link_libraries(logisticsearch_cpp_runtime_smoke
    PRIVATE
        logisticsearch_cpp_runtime
)

enable_testing()

add_executable(logisticsearch_cpp_runtime_version_test
    tests/test_version_smoke.cpp
)

target_link_libraries(logisticsearch_cpp_runtime_version_test
    PRIVATE
        logisticsearch_cpp_runtime
)

add_test(
    NAME logisticsearch_cpp_runtime_version_smoke
    COMMAND logisticsearch_cpp_runtime_version_test
)
