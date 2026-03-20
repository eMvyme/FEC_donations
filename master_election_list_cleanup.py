import json

INPUT_FILE = "intermediary data/master_election_list.json"
OUTPUT_FILE = "intermediary data/master_election_list_processed.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

filtered = {}

for race_id, race in data.items():
    candidates = race.get("candidates_in_race", [])
    total_votes_reported = race.get("total_votes", 0)

    # Remove races with one candidate
    if len(candidates) <= 1:
        continue

    # Convert votes to int
    for c in candidates:
        c["votes"] = int(c.get("votes", 0))

    # Sum candidate votes
    vote_sum = sum(c["votes"] for c in candidates)

    # Remove races where listed votes < 90% of total_votes
    if total_votes_reported == 0 or vote_sum < 0.9 * total_votes_reported:
        continue

    # Totals across candidates
    total_small = sum(c.get("small_donations", 0) for c in candidates)
    total_receipts = sum(c.get("total_receipts", 0) for c in candidates)

    # Add percentages
    for c in candidates:
        c["vote_pct"] = c["votes"] / vote_sum if vote_sum else 0
        c["small_donation_pct"] = (
            c.get("small_donations", 0) / total_small if total_small else 0
        )
        c["receipt_pct"] = (
            c.get("total_receipts", 0) / total_receipts if total_receipts else 0
        )

    filtered[race_id] = race

with open(OUTPUT_FILE, "w") as f:
    json.dump(filtered, f, indent=4)

print("Original races:", len(data))
print("Remaining races:", len(filtered))