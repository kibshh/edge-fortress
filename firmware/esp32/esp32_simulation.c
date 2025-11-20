#include <stdio.h>
#include "wifi.h"
#include "sensor_readings.h"
#include "http_client.h"

int main(void)
{
    printf("=== ESP32 firmware simulation ===\n");
    
    Wifi_WifiInit();
    ReadingBatch_t batch;
    SensorReadings_FillSensorReadings(&batch);
    HttpClient_HttpPostReadings(&batch);

    printf("=== simulation done ===\n");
    return 0;
}