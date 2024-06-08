from apimanager import safe_make_request
from dotenv import load_dotenv
import os
from sendtoresults import write_to_json
from time import time
load_dotenv()

initial_puuid = os.getenv("INITIAL_PUUID")

matches_per_puuid_url = "https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/"

depth = 100
games_per_player = 100
exit_player_count = 10000000

requests_per_minute = 50 # Riot API rate limit

#honestly not sure if these calculations actually make sense/are correct, but they should be close enough idk if the 11's are right.
print("Maximum total requests: " + str((games_per_player*11) ** depth))
print("Maximum total puuids: " + str((games_per_player*10) ** (depth + 1)))
print("Maximum total time: " + str((games_per_player*11) ** depth / requests_per_minute) + " minutes")

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

def get_total_puuids():
    return sum([len(puuids[i]) for i in range(depth + 1)])

def save_to_file(filename):
    countPerDepth = [len(puuids[i]) for i in range(depth + 1)]
    totalCount = sum(countPerDepth)

    print("")
    print("Total count: " + str(totalCount))
    print("Count per depth: " + str(countPerDepth))

    print("Time taken: " + str((time() - start_time) / 60) + " minutes")
    print("Total requests made: " + str(total_requests_made))

    write_to_json({"totalRequests": total_requests_made, "totalCount": totalCount, "countPerDepth": countPerDepth, "puuids": puuids}, filename)

backup_every = 1000

def update_requests_made():
    global total_requests_made
    total_requests_made += 1
    print(f"Total requests made: {total_requests_made}", end="\r")

start_time = time()

for i in range(depth):
    for puuid in puuids[i]:
        
        match_ids = get_recent_match_ids(puuid)
        update_requests_made()

        for match_id in match_ids:
            if match_ids_used in match_ids:
                continue
            match_ids_used.append(match_id)

            details = get_match_details(match_id)
            update_requests_made()

            for participant in details["info"]["participants"]:
                if not puuid_already_used(participant["puuid"]):
                    puuids[i + 1].append(participant["puuid"]) 
                    total_puuids = get_total_puuids()
                    if total_puuids % backup_every == 0:
                        write_to_json(f"puuids_backup_{total_puuids}.json")
                    if total_puuids == exit_player_count:
                        save_to_file(f"puuids_completed_{exit_player_count}.json")
                        print(f"Exiting early {exit_player_count} reached")
                        exit()

print("Reacher terminal depth without reaching exit player count")
save_to_file(f"puuids_completed_{get_total_puuids()}.json")