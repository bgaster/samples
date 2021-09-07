/**
 * Desc: Simple API for Tom's Oak/Mushroom project
 * Copyright: Benedict R. Gaster
 */

#pragma once

#define NUMBER_OF_VALUES_IN_READING 8

#ifdef __cplusplus
extern "C"
{
#endif
    // struct representing a single sample reading
    struct Sample
    {
        // timestamp for sample reading
        unsigned int timestamp;
        // values read for sample reading
        float values[NUMBER_OF_VALUES_IN_READING];
    };

    // Get the number of samples that are unread
    unsigned int get_number_samples();

    // Get any samples that are marked as unread
    // returns:
    //  number_samples marked as unread, 0 if there are none
    //  Pointer to array of samples

    // Note: Ownership of this memory held by the array is passed to the caller.
    //       Dealocate memory with free.
    struct Sample *get_samples(unsigned int *number_samples);

    // Store sample
    void put_sample(struct Sample *);

    // mark sample as read
    void mark_sample(unsigned int timestamp);

    // mark sample as not read
    void unmark_sample(unsigned int timestamp);
#ifdef __cplusplus
}
#endif