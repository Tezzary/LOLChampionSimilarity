import os
import json

path = "results"

def write_to_json(results, filename):
    with open(os.path.join(path, filename), "w") as f:
        json.dump(results, f, indent=4)