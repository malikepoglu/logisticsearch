#pragma once

namespace logisticsearch::cpp_runtime {

constexpr int version_major() noexcept { return 0; }
constexpr int version_minor() noexcept { return 1; }
constexpr int version_patch() noexcept { return 0; }

const char* runtime_name() noexcept;
const char* runtime_surface() noexcept;
const char* version_string() noexcept;

}  // namespace logisticsearch::cpp_runtime
