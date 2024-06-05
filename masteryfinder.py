from apimanager import safe_make_request
from sendtoresults import write_to_json
from dotenv import load_dotenv
import os

load_dotenv()

initial_puuid = os.getenv("INITIAL_PUUID")

get_mastery_base = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"

result = safe_make_request(get_mastery_base + initial_puuid)

write_to_json(result, "mastery.json")
