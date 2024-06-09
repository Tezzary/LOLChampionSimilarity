import os
import json

username_path = "results"

def get_next_dir():
    i = 0
    while True:
        if not os.path.exists(os.path.join(username_path, f"results_{i}")):
            return f"results_{i}"
        i += 1

next_dir = get_next_dir()

os.makedirs(os.path.join(username_path, next_dir))

def write_to_json(results, filename):
    with open(os.path.join(username_path, next_dir, filename), "w") as f:
        json.dump(results, f, indent=4)
        