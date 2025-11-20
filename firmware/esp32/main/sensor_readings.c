#include "sensor_readings.h"
#include <string.h>

static void StrcpySafeWrap(char *dst, size_t dst_size, const char* src)
{
    if(0 != dst_size)
    {
        strncpy(dst, src, dst_size - 1);
        dst[dst_size - 1] = '\0';
    }
}

void SensorReadings_FillSensorReadings(ReadingBatch_t *batch)
{
    batch->count = 0u;

    /* Fake temperature */
    StrcpySafeWrap(batch->readings[batch->count].device_id, DEVICE_ID_MAX_LEN, "esp32-001");
    StrcpySafeWrap(batch->readings[batch->count].metric, METRIC_MAX_LEN, "temperature");
    batch->readings[batch->count].value = 24.9f;
    StrcpySafeWrap(batch->readings[batch->count].unit, UNIT_MAX_LEN, "C");
    batch->count++;

    /* Fake humidity */
    StrcpySafeWrap(batch->readings[batch->count].device_id, DEVICE_ID_MAX_LEN, "esp32-001");
    StrcpySafeWrap(batch->readings[batch->count].metric, METRIC_MAX_LEN, "humidity");
    batch->readings[batch->count].value = 42.8f;
    StrcpySafeWrap(batch->readings[batch->count].unit, UNIT_MAX_LEN, "%");
    batch->count++;
}