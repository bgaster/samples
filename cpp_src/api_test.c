/**
 * Desc: Test example for Tom's Oak/Mushroom project
 * Copyright: Benedict R. Gaster
 */
#include <stdlib.h>
#include <stdio.h>

#include <api.h>

int main()
{
    // struct Sample sample;
    // sample.timestamp = 5;
    // sample.values[0] = 0.23f;
    // sample.values[1] = 1.23f;
    // sample.values[2] = 2.23f;
    // sample.values[3] = 3.23f;
    // sample.values[4] = 4.23f;
    // sample.values[5] = 5.23f;
    // sample.values[6] = 6.23f;
    // sample.values[7] = 7.23f;

    // put_sample(&sample);

    unmark_sample(4);

    unsigned int number_samples = 0;
    struct Sample *samples = get_samples(&number_samples);
    if (number_samples != 0)
    {
        printf("Samples returned:\n");
        for (unsigned int i = 0; i < number_samples; i++)
        {
            printf("  Timestamp: %d\n", samples[i].timestamp);
            printf("  Values:\n");
            for (int j = 0; j < NUMBER_OF_VALUES_IN_READING; j++)
            {
                printf("       %f\n", samples[i].values[j]);
            }
        }
    }
    free(samples);

    return 0;
}