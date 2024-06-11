import json

#open champion_ids.json and redump it with indent 4

with open("champion.json", "r") as f:
    data = json.load(f)
    #with open("champion_parsed.json", "w") as f:
        #json.dump(data, f, indent=4)
    
    champion_objs = data["data"]
    champion_data = []
    for key in champion_objs:
        champion_data.append({
            "id": champion_objs[key]["key"],
            "name": champion_objs[key]["name"],
            "full": champion_objs[key]["image"]["full"],
            "sprite": champion_objs[key]["image"]["sprite"],
        })
    with open("champion_parsed.json", "w") as f:
        json.dump(champion_data, f, indent=4)

