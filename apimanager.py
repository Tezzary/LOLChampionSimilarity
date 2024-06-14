import requests
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

api_key = os.getenv("API_KEY")

def params_to_string(params):
    if len(params) == 0:
        return ""
    return "&".join([f"{k}={v}" for k, v in params.items()])

def make_request(endpoint, params={}):
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(endpoint + params_to_string(params), headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()

def safe_make_request(endpoint, params={}):
    while True:
        try:
            return make_request(endpoint, params)
        except Exception as e:
            print(e)
            if (e.args[0] == 429):
                retry_timer = 5
                print("Rate limited, retrying in " + str(retry_timer) + " seconds")
                sleep(retry_timer)
            else:
                return None

def get_summoner_by_puuid(puuid):
    account_data = safe_make_request("https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/" + puuid)
    if account_data is None:
        return None
    summoner_data = safe_make_request("https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid)
    if summoner_data is None and type(summoner_data["id"]) is str:
        return None
    league_data = safe_make_request("https://oc1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_data["id"])
    print(summoner_data["id"])
    print(league_data)
    if league_data is None:
        return None
    
    if len(league_data) == 0:
        league_data.append({
            "queueType": "RANKED_SOLO_5x5",
            "tier": "UNRANKED",
            "rank": "I"
        })

    #normally index = 0, but sometimes index 0 is "CHERRY" which I think might be arena, idk either way thats why this exists
    ranked_5v5_index = None
    for i in range(len(league_data)):
        if league_data[i]["queueType"] == "RANKED_SOLO_5x5":
            ranked_5v5_index = i
            break
    if ranked_5v5_index is None:
        return None
    
    rank = league_data[ranked_5v5_index]["rank"]

    if rank == "I":
        rank = 1
    elif rank == "II":
        rank = 2
    elif rank == "III":
        rank = 3
    elif rank == "IV":
        rank = 4

    return {
        "puuid": puuid,
        "gameName": account_data["gameName"],
        "tagLine": account_data["tagLine"],
        "summonerLevel": summoner_data["summonerLevel"],
        "tier": league_data[ranked_5v5_index]["tier"],
        "rank": rank,
    }

def get_mastery_by_puuid(puuid):
    masteries = safe_make_request("https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/" + puuid)
    if masteries is None:
        return None
    organised_masteries = []
    for mastery in masteries:
        organised_masteries.append({
            "puuid": puuid,
            "championId": mastery["championId"],
            "championPoints": mastery["championPoints"],
            "championLevel": mastery["championLevel"]
        })
    return organised_masteries
