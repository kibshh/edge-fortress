#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

#include "readings.h"

#ifdef __cplusplus
extern "C" {
#endif

void HttpClient_HttpPostReadings(const ReadingBatch_t *batch);

#ifdef __cplusplus
}
#endif

#endif