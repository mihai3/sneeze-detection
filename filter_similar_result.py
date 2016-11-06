#!/usr/bin/env python
# get "similar" results from API; keep those who are not really similar based on description

import json

filtered_results = []

with open("similar_result.json") as jf:
    results = json.load(jf)

    for similar_response in results:
        if "results" not in similar_response:
            continue  # malformed

        for result in similar_response["results"]:
            if result is None or "id" not in result: continue # malformed

            if "sneeze" not in result["description"].lower() and "sneeze" not in result["name"].lower() and result["duration"] < 8:
                filtered_results.append(result)

with open("not_really_similar.json", "w") as jof:
    json.dump(filtered_results, jof)