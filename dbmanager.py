import sqlite3

region = "oce"

def create_db():
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS summoner(gameName TEXT, tagLine TEXT, puuid TEXT, summonerLevel INTEGER, PRIMARY KEY (puuid))")
    #cur.execute("CREATE TABLE IF NOT EXISTS match(matchId TEXT, PRIMARY KEY (matchId))")
    #cur.execute("CREATE TABLE IF NOT EXISTS match_participant(puuid TEXT, matchId TEXT, FOREIGN KEY (puuid) REFERENCES summoner(puuid), FOREIGN KEY (matchId) REFERENCES match(matchId))")
    cur.execute("CREATE TABLE IF NOT EXISTS champion_mastery(puuid TEXT, championId INTEGER, championPoints INTEGER, championLevel INTEGER, FOREIGN KEY (puuid) REFERENCES summoner(puuid))")

    conn.commit()

def insert_summoner(gameName, tagLine, puuid, summonerLevel):
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO summoner(gameName, tagLine, puuid, summonerLevel) VALUES (?, ?, ?, ?)", (gameName, tagLine, puuid, summonerLevel))

    conn.commit()

def insert_champion_mastery(puuid, championId, championPoints, championLevel):
    conn = sqlite3.connect(f"db/{region}.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO champion_mastery(puuid, championId, championPoints, championLevel) VALUES (?, ?, ?, ?)", (puuid, championId, championPoints, championLevel))

    conn.commit()