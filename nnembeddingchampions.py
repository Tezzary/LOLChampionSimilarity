import dbmanager
import random
import json
import numpy as np

summoner_count = dbmanager.get_number_of_summoners()

epoch_size = 1000
champion_count = 10
epoch_count = 20

champion_data = json.load(open("champion_parsed.json"))

print(summoner_count)


def collect_account_data():
    summoners = dbmanager.select_random_summoners(epoch_size)
    random_champions = random.sample(champion_data, champion_count)
    for summoner in summoners:
        masteries = dbmanager.get_masteries(summoner)
        for champion in random_champions:
            champion_mastery = None
            for mastery in masteries:
                if mastery["championId"] == champion["id"]:
                    champion_mastery = mastery
            if champion_mastery is None:
                champion_mastery = {
                    "puuid": summoner["puuid"],
                    "championId": champion["id"],
                    "championPoints": 0,
                    "championLevel": 0
                }

    return summoners


def geometric_mean(champ1, champ2):
    pass

print(collect_account_data())