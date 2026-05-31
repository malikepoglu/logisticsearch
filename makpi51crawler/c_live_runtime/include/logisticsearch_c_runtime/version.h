#ifndef LOGISTICSEARCH_C_RUNTIME_VERSION_H
#define LOGISTICSEARCH_C_RUNTIME_VERSION_H

#ifdef __cplusplus
extern "C" {
#endif

int logisticsearch_c_runtime_version_major(void);
int logisticsearch_c_runtime_version_minor(void);
int logisticsearch_c_runtime_version_patch(void);

const char* logisticsearch_c_runtime_name(void);
const char* logisticsearch_c_runtime_surface(void);
const char* logisticsearch_c_runtime_version_string(void);

#ifdef __cplusplus
}
#endif

#endif /* LOGISTICSEARCH_C_RUNTIME_VERSION_H */
