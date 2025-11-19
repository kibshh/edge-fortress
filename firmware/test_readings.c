#include <stdio.h>
#include <string.h>
#include "readings.h"

static void StrcpySafeWrap(char *dst, size_t dst_size, const char* src)
{
    if(0 != dst_size)
    {
        strncpy(dst, src, dst_size - 1);
        dst[dst_size - 1] = '\0';
    }
}

int main(void)
{
    int Result;

    ReadingBatch_t batch;
    batch.count = 0u;

    /* First reading: temperature */
    StrcpySafeWrap(batch.readings[batch.count].device_id, DEVICE_ID_MAX_LEN, "esp32-001");
    StrcpySafeWrap(batch.readings[batch.count].metric, METRIC_MAX_LEN, "temperature");
    batch.readings[batch.count].value = 23.5f;
    StrcpySafeWrap(batch.readings[batch.count].unit, UNIT_MAX_LEN, "C");
    batch.count++;

    /* Second reading: humidity */
    StrcpySafeWrap(batch.readings[batch.count].device_id, DEVICE_ID_MAX_LEN, "esp32-001");
    StrcpySafeWrap(batch.readings[batch.count].metric, METRIC_MAX_LEN, "humidity");
    batch.readings[batch.count].value = 41.2f;
    StrcpySafeWrap(batch.readings[batch.count].unit, UNIT_MAX_LEN, "%");
    batch.count++;

    char json_string[512];
    RetVal_e RetVal = Readings_BuildBatchJson(&batch, json_string, sizeof(json_string));
    if(RETVAL_ERROR == RetVal)
    {
        fprintf(stderr, "Error: JSON buffer too small or other failure.\n");
        Result = 1;
    }
    else
    {
        printf("%s\n", json_string);
        Result = 0;
    }
    return Result;
}
