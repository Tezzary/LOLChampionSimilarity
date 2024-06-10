from apimanager import safe_make_request, get_summoner_by_puuid, get_mastery_by_puuid
import dbmanager

from dotenv import load_dotenv
import os
from time import time

load_dotenv()

initial_puuid = os.getenv("INITIAL_PUUID")

matches_per_puuid_url = "https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/"

games_per_player = 100
exit_player_count = 100000

def get_recent_match_ids(puuid):
    return safe_make_request(matches_per_puuid_url + puuid + "/ids" + f"?count={games_per_player}&type=ranked")

def get_match_details(match_id):
    return safe_make_request("https://sea.api.riotgames.com/lol/match/v5/matches/" + match_id)

start_time = time()

while True:
    summoner = dbmanager.select_unused_summoner()
    if summoner is None:
        print("No more unused summoners")
        break
    
    print(summoner)
    dbmanager.mark_summoner_as_used(summoner["puuid"])

    match_ids = get_recent_match_ids(summoner["puuid"])
    if match_ids is None:
        print(f"Failed to get match ids for puuid {summoner['puuid']}, skipping")
        continue

    for match_id in match_ids:
        if dbmanager.match_exists(match_id):
            continue
        dbmanager.insert_match(match_id)
 
        details = get_match_details(match_id)
        if details is None:
            print(f"Failed to get match details for match id {match_id}, skipping")
            continue
        for participant in details["info"]["participants"]:
            puuid = participant["puuid"]
            if dbmanager.summoner_exists(puuid):
                continue
            summoner = get_summoner_by_puuid(puuid)
            if summoner is None:
                print(f"Failed to get summoner for puuid {puuid}, skipping")
                continue
            dbmanager.insert_summoner(summoner)

            masteries = get_mastery_by_puuid(puuid)
            if masteries is None:
                print(f"Failed to get masteries for puuid {puuid}, skipping")
                continue
            for mastery in masteries:
                dbmanager.insert_champion_mastery(mastery)
    
    if dbmanager.get_number_of_summoners() >= exit_player_count:
        break

print("Done, met exit condition of " + str(exit_player_count) + " players")
print("Time taken: " + str((time() - start_time) / 60) + " minutes")