from apimanager import safe_make_request
from dotenv import load_dotenv
import os

load_dotenv()

initial_puuid = os.getenv("INITIAL_PUUID")

matches_per_puuid_url = "https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/"

used_puuids = []
puuids = []

depth = 1

def get_recent_match_ids(puuid):
    return safe_make_request(matches_per_puuid_url + puuid + "/ids" + "?count=3")

def get_match_details(match_id):
    return safe_make_request("https://sea.api.riotgames.com/lol/match/v5/matches/" + match_id)
for i in range(depth):
    match_ids = get_recent_match_ids(initial_puuid)
    for match_id in match_ids:
        details = get_match_details(match_id)
        for participant in details["info"]["participants"]:
            if participant["puuid"] not in used_puuids and participant["puuid"] not in puuids:
                puuids.append(participant["puuid"])
        print(get_match_details(match_id))
    puuids.append(initial_puuid)
    initial_puuid = result[0]
print(get_recent_match_ids(initial_puuid))
'''
with open ("test.json", "w") as f:
    json.dump(result, f, indent=4)
'''