#include "http_client.h"
#include "readings.h"
#include <stdio.h>

void HttpClient_HttpPostReadings(const ReadingBatch_t *batch)
{
    char json_string[512];

    RetVal_e RetVal = Readings_BuildBatchJson(batch, json_string, sizeof(json_string));

    if(RETVAL_SUCCESS == RetVal)
    {
        printf("(http) Would POST the following JSON to /ingest_batch:\n");
        printf("%s\n", json_string);
    }
    else
    {
        printf("(http) ERROR: failed to build JSON (buffer too small?)\n");
    }
}
