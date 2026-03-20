import pandas as pd
import matplotlib.pyplot as plt
import donation_data as pull
import json, os

dataset = pd.read_csv("intermediary data/dataset_post2008.csv", dtype=str)
dataset = dataset.drop(columns=dataset.columns[0])

races = pd.read_csv("house2024/races_post2008.csv")

# the following are tests to make sure the data looks good

    # candidates per state
'''states = {}
for idx, row in dataset.iterrows():
    states[row["state"]] = states.get(row["state"], 0) + 1

print(states.items())

labels = list(states.keys())
sizes = list(states.values())

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()'''

    # candidates per party
'''parties = {}
for idx, row in dataset.iterrows():
    parties[row["party"]] = parties.get(row["party"], 0) + 1

print(parties.items())

labels = list(parties.keys())
sizes = list(parties.values())

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()'''

    # candidates by district
'''districts = {}
for idx, row in dataset.iterrows():
    districts[(row["state"] + row["district"])] = districts.get(row["state"] + row["district"], 0) + 1

print(districts.items())

labels = list(districts.keys())
sizes = list(districts.values())'''

    # candidates by year
'''candidates_p_year = {}
for idx, row in dataset.iterrows():
    candidates_p_year[(row["year"])] = candidates_p_year.get(row["year"], 0) + 1

print(candidates_p_year.items())

sum = 0
for i in range(2008,2024,2):
    sum += candidates_p_year[str(i)]

print(sum)'''


file_path = "intermediary data/master_election_list.json"

# check if the file exists
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        master_election_list = json.load(f)

# create a new master_election_list
else:
    grouped_candidates = (
        dataset.rename(columns={
            "FEC_ID": "fec_id",
            "candidatevotes": "votes"
        })
        .groupby("race_id")
        .apply(lambda df: df[["fec_id", "votes"]].to_dict("records"))
        .to_dict()
        )

    master_election_list = {
        race_id: {
            "total_votes": total_votes,
            "candidates_in_race": grouped_candidates.get(race_id, [])
        }
        for race_id, total_votes in zip(
            races["race_id"], races["total_votes"]
        )
    }

error_list = "error_list.json"

if os.path.exists(error_list):
    with open(error_list, "r") as f:
        error_list = set(json.load(f))

else: error_list = ['H6CA40275', 'H4FL14034']

save = 0
rate_check = 0
for election_id in master_election_list:
    term = int(election_id.split("_")[1])
    for candidate in master_election_list[election_id]["candidates_in_race"]:
        # find where I last left off
        if len(candidate) > 2:
            continue

        # if candidate["fec_id"] in error_list:
            # continue

        print(election_id, candidate["fec_id"])

        try:
            small_donations, total_receipts = pull.fec_id_to_donations(candidate["fec_id"], term)
        except TypeError:
            error_list.add(candidate["fec_id"])
            candidate["small_donations"] = "temp"
            candidate["total_receipts"] = "temp"
            continue

        else:
            candidate["small_donations"] = small_donations
            candidate["total_receipts"] = total_receipts

            if candidate["fec_id"] in error_list:
                error_list.remove(candidate["fec_id"])
            print("popped")
        save += 1

        if save >= 6:
            with open("intermediary data/master_election_list.json", "w") as f:
                json.dump(master_election_list, f, indent=4)
            with open("intermediary data/error_list.json", "w") as f:
                json.dump(list(error_list), f, indent=4)
            save = 0
        if rate_check > 500:
            break
