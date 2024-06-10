import sqlite3
from dotenv import load_dotenv
import os

import apimanager

load_dotenv()

region = "oce"

def create_db():
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS summoner(puuid TEXT, used INTEGER, gameName TEXT, tagLine TEXT, summonerLevel INTEGER, tier TEXT, rank INTEGER, PRIMARY KEY (puuid))")
    cur.execute("CREATE TABLE IF NOT EXISTS match(matchId TEXT, PRIMARY KEY (matchId))")
    #cur.execute("CREATE TABLE IF NOT EXISTS match_participant(puuid TEXT, matchId TEXT, FOREIGN KEY (puuid) REFERENCES summoner(puuid), FOREIGN KEY (matchId) REFERENCES match(matchId))")
    cur.execute("CREATE TABLE IF NOT EXISTS champion_mastery(puuid TEXT, championId INTEGER, championPoints INTEGER, championLevel INTEGER, FOREIGN KEY (puuid) REFERENCES summoner(puuid))")

    conn.commit()

def insert_summoner(summoner):
    puuid = summoner["puuid"]
    gameName = summoner["gameName"]
    tagLine = summoner["tagLine"]
    summonerLevel = summoner["summonerLevel"]
    tier = summoner["tier"]
    rank = summoner["rank"]

    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO summoner(puuid, used, gameName, tagLine, summonerLevel, tier, rank) VALUES (?, 0, ?, ?, ?, ?, ?)", (puuid, gameName, tagLine, summonerLevel, tier, rank))

    conn.commit()

def insert_champion_mastery(mastery):
    puuid = mastery["puuid"]
    championId = mastery["championId"]
    championPoints = mastery["championPoints"]
    championLevel = mastery["championLevel"]
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO champion_mastery(puuid, championId, championPoints, championLevel) VALUES (?, ?, ?, ?)", (puuid, championId, championPoints, championLevel))

    conn.commit()

def insert_match(matchId):
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO match(matchId) VALUES (?)", (matchId,))

    conn.commit()

def summoner_exists(puuid):
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM summoner WHERE puuid = ?", (puuid,))
    return cur.fetchone() is not None

def match_exists(matchId):
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM match WHERE matchId = ?", (matchId,))
    return cur.fetchone() is not None

def select_unused_summoner():
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM summoner WHERE used = 0 LIMIT 1")
    summoner = cur.fetchone()
    summoner = {
        "puuid": summoner[0],
        "gameName": summoner[2],
        "tagLine": summoner[3],
        "summonerLevel": summoner[4],
        "tier": summoner[5],
        "rank": summoner[6]
    }
    return summoner

def mark_summoner_as_used(puuid):
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("UPDATE summoner SET used = 1 WHERE puuid = ?", (puuid,))

    conn.commit()

if __name__ == "__main__":
    create_db()
    initial_puuid = os.getenv("INITIAL_PUUID")
    summoner = apimanager.get_summoner_by_puuid(initial_puuid)
    if summoner is None:
        print("Failed to get summoner")
        exit()
    insert_summoner(summoner)

def get_number_of_summoners():
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM summoner")
    return cur.fetchone()[0]