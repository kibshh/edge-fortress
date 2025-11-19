#include "readings.h"
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

/**
 * Helper to safely append to the buffer.
 * Returns RetVal_e: RETVAL_SUCCESS on success, RETVAL_ERROR if it would overflow.
 */
static RetVal_e AppendToBuffer(char *buf, size_t buf_size, size_t *offset, const char *fmt, ...)
{
    RetVal_e retval = RETVAL_ERROR;
    int written = 0;

    if(*offset < buf_size)
    {
        size_t left_space = buf_size - *offset;
        va_list args;
        va_start(args, fmt);
        written = vsnprintf(buf + *offset, left_space, fmt, args);
        va_end(args);
        if((written >= 0) && ((size_t)written < left_space))
        {
            retval = RETVAL_SUCCESS; /* Successful operation */
        }
    }

    *offset += (size_t)written;
    return retval;
}

RetVal_e Readings_BuildBatchJson(const ReadingBatch_t *batch, char *out_buf, size_t out_buf_size)
{
    RetVal_e retval = RETVAL_SUCCESS;

    if((NULL != batch) && (NULL != out_buf) && (0 != out_buf_size))
    {
        size_t offset = 0;
        out_buf[0] = '\0';

        /* Start JSON array */
        if(RETVAL_SUCCESS == AppendToBuffer(out_buf, out_buf_size, &offset, "["))
        {
            for(uint8_t i = 0; i < batch->count; ++i)
            {
                const Reading_t *r = &(batch->readings[i]);

                /* Add comma before all but the first element */
                if(i > 0)
                {
                    if(RETVAL_ERROR == AppendToBuffer(out_buf, out_buf_size, &offset, ","))
                    {
                        retval = RETVAL_ERROR;
                        break;
                    }
                }

                /* NOTE: This assumes device_id, metric, unit contain no quotes or special chars. */
                /* For sensor names and short IDs, that's OK. */
                if(RETVAL_ERROR == AppendToBuffer(out_buf, out_buf_size, &offset,
                                    "{\"device_id\":\"%s\",\"metric\":\"%s\",\"value\":%.3f,\"unit\":\"%s\"}",
                                    r->device_id,
                                    r->metric,
                                    r->value,
                                    r->unit)
                )
                {
                    retval = RETVAL_ERROR;
                    break;
                }
            }

            if(RETVAL_SUCCESS == retval)
            {
                /* End JSON array */
                if(RETVAL_ERROR == AppendToBuffer(out_buf, out_buf_size, &offset, "]"))
                {
                    retval = RETVAL_ERROR;
                }
            }
        }
        else
        {
            /* First write failed */
            retval = RETVAL_ERROR;
        }
    }
    else
    {
        /* Return error, wrong parameters are given */
        retval = RETVAL_ERROR;
    }

    return retval;
}
