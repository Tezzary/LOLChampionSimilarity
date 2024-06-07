from apimanager import safe_make_request
from dotenv import load_dotenv
import os
from sendtoresults import write_to_json

load_dotenv()

initial_puuid = os.getenv("INITIAL_PUUID")

matches_per_puuid_url = "https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/"

depth = 3
games_per_player = 1

puuids = [[] for i in range(depth + 1)]
puuids[0].append(initial_puuid)

match_ids_used = []

def puuid_already_used(puuid):
    for i in range(depth):
        if puuid in puuids[i]:
            return True
    return False

def get_recent_match_ids(puuid):
    return safe_make_request(matches_per_puuid_url + puuid + "/ids" + f"?count={games_per_player}&type=ranked")

def get_match_details(match_id):
    return safe_make_request("https://sea.api.riotgames.com/lol/match/v5/matches/" + match_id)

total_requests_made = 0

for i in range(depth):
    for puuid in puuids[i]:
        match_ids = get_recent_match_ids(puuid)
        total_requests_made += 1
        print(f"Total requests made: {total_requests_made}")
        for match_id in match_ids:
            if match_ids_used in match_ids:
                continue
            match_ids_used.append(match_id)
            details = get_match_details(match_id)
            total_requests_made += 1
            print(f"Total requests made: {total_requests_made}")
            for participant in details["info"]["participants"]:
                if not puuid_already_used(participant["puuid"]):
                    puuids[i + 1].append(participant["puuid"]) 

write_to_json({"puuids": puuids}, "puuids.json")