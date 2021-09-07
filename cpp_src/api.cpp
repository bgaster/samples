#include "restclient-cpp/restclient.h"
#include <nlohmann/json.hpp>

#include <cstdlib>
#include <vector>
#include <iostream>
#include <string>

#include <api.h>

using json = nlohmann::json;

extern "C"
{
    // Get the number of samples that are unread
    unsigned int get_number_samples()
    {
        RestClient::Response r = RestClient::get("http://3.10.74.167:6789/api/get_number_samples/");
        //TODO: add check that valid JSON, etc.
        auto recv = json::parse(r.body);
        return recv["number_of_samples"].get<unsigned int>();
    }

    // Get any samples that are marked as unread
    // returns:
    //  number_samples marked as unread, 0 if there are none
    // Note: Ownership of this memory held by the array is passed to the caller.
    //       Dealocate memory with free.
    Sample *get_samples(unsigned int *number_samples)
    {
        *number_samples = get_number_samples();
        // are there any samples to process
        if (*number_samples == 0)
        {
            return nullptr;
        }

        // malloc as we need to return and pass ownership to C
        auto samples = static_cast<Sample *>(malloc(*number_samples * sizeof(Sample)));

        auto r = RestClient::get("http://3.10.74.167:6789/api/get_samples/");

        auto recv = json::parse(r.body);

        auto s = recv["samples"].get<std::vector<json>>();

        int index = 0;
        for (auto sample : s)
        {
            samples[index].timestamp = sample["timestamp"].get<unsigned int>();
            auto values = sample["values"].get<std::vector<json>>();

            int i = 0;
            for (auto v : values)
            {
                std::string str = v.get<std::string>();
                samples[index].values[i++] = std::stof(str);
            }

            index++;
        }

        return samples;
    }

    // Store sample
    void put_sample(struct Sample *sample)
    {
        std::vector<std::string> values;
        for (int i = 0; i < NUMBER_OF_VALUES_IN_READING; i++)
        {
            values.push_back(std::to_string(sample->values[i]));
        }

        json s;
        s["timestamp"] = sample->timestamp;
        s["values"] = values;

        auto r = RestClient::put(
            "http://3.10.74.167:6789/api/put_sample/" + std::to_string(sample->timestamp),
            "application/json",
            s.dump());
    }

    // mark sample as read
    void mark_sample(unsigned int timestamp)
    {
        auto r = RestClient::put(
            "http://3.10.74.167:6789/api/mark_sample/" + std::to_string(timestamp),
            "text/plain",
            "mark");
    }

    // unmark sample as read
    void unmark_sample(unsigned int timestamp)
    {
        auto r = RestClient::put(
            "http://3.10.74.167:6789/api/unmark_sample/" + std::to_string(timestamp),
            "text/plain",
            "mark");
    }
}