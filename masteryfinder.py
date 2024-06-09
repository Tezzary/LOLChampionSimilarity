from apimanager import safe_make_request
from sendtoresults import write_to_json
from dotenv import load_dotenv
import os
import json

load_dotenv()

get_mastery_base = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"


#to be set by the user to find the accounts that the mastery will be found for.
results_dir = "results_2" #to be set by the user
results_file = "puuids.json" #to be set by the user

with open(os.path.join("results", results_dir, results_file), "r") as f:
    puuids_file = json.load(f)

for search_depth in puuids_file["puuids"]:
    for puuid in search_depth:
        result = safe_make_request(get_mastery_base + puuid)
        player_mastery = []
        if result is None:
            print(f"Failed to get mastery for puuid {puuid}, skipping")
            continue
        for champion_data in result:
            champion = {
                "championId": champion_data["championId"],
                "championPoints": champion_data["championPoints"],
                "championLevel": champion_data["championLevel"],
            }
            player_mastery.append(champion)
             




write_to_json(result, "mastery.json")
