#include "http_client.h"
#include "readings.h"
#include <stdio.h>

void HttpClient_HttpPostReadings(const ReadingBatch_t *batch)
{
    printf("[http] post placeholder (%d readings)\n", batch->count);
}
