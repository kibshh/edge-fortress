#ifndef READINGS_H
#define READINGS_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DEVICE_ID_MAX_LEN           32u    /* Max len of Device ID string */
#define METRIC_MAX_LEN              32u    /* Max len of Metric string */
#define UNIT_MAX_LEN                8u     /* Max len of Unit string */
#define MAX_READINGS_PER_BATCH      8u     /* Max number of readings per batch */

/* Struct containing one sensor reading */
typedef struct 
{
    char device_id[DEVICE_ID_MAX_LEN];
    char metric[METRIC_MAX_LEN];
    float value;
    char unit[UNIT_MAX_LEN];
    /* Optionally: add timestamp field here if needed */
} Reading_t;

/* Struct containing batch sensor readings and count */
typedef struct
{
    Reading_t readings[MAX_READINGS_PER_BATCH];
    uint8_t count;
} ReadingBatch_t;

typedef enum
{
    RETVAL_SUCCESS,
    RETVAL_ERROR
} RetVal_e;

/**
 * Build JSON array for the given batch into out_buf.
 *
 * Example output:
 * [
 *   {"device_id":"esp32-001","metric":"temperature","value":23.500,"unit":"C"},
 *   {"device_id":"esp32-001","metric":"humidity","value":41.200,"unit":"%"}
 * ]
 *
 * Returns RetVal_e:
 *  RETVAL_SUCCESS (0) on success
 *  RETVAL_ERROR (1) if the error occured (e.g. output buffer was too small)
 */
RetVal_e Readings_BuildBatchJson(const ReadingBatch_t *batch, char *out_buf, size_t out_buf_size);

#ifdef __cplusplus
}
#endif

#endif // READINGS_H
