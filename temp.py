import json

with open("valid_election_list.json", "r") as f:
    master_election_list = json.load(f)


for election_id in master_election_list:
    if len(election_id["candidates_in_race"]) < 2:
        del election_id

with open("valid_election_list.json", "w") as f:
    json.dump(master_election_list, f, indent=4)
