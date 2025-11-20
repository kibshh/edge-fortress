#ifndef SENSOR_READINGS_H
#define SENSOR_READINGS_H

#include "readings.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Fill the ReadingBatch with actual sensor values.
 * For now, this is a dummy function that fills in fake values.
 * Later we will replace the internals with real sensor drivers.
 */
void SensorReadings_FillSensorReadings(ReadingBatch_t *batch);

#ifdef __cplusplus
}
#endif

#endif
