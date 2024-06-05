import json
from apimanager import safe_make_request
from dotenv import load_dotenv
import os

load_dotenv()

initial_puuid = os.getenv("INITIAL_PUUID")

base_url = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"

result = safe_make_request(base_url + initial_puuid)

with open ("test.json", "w") as f:
    json.dump(result, f, indent=4)

