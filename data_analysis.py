import json
import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = "intermediary data/master_election_list_processed.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

vote_pct = []
small_pct = []
receipt_pct = []

# Collect candidate-level data
for race in data.values():
    for c in race.get("candidates_in_race", []):
        vote_pct.append(c.get("vote_pct", 0))
        small_pct.append(c.get("small_donation_pct", 0))
        receipt_pct.append(c.get("receipt_pct", 0))

vote_pct = np.array(vote_pct)
small_pct = np.array(small_pct)
receipt_pct = np.array(receipt_pct)

# Pearson correlations
corr_small = np.corrcoef(vote_pct, small_pct)[0, 1]
corr_receipts = np.corrcoef(vote_pct, receipt_pct)[0, 1]

print("Correlation: vote_pct vs small_donation_pct =", corr_small)
print("Correlation: vote_pct vs receipt_pct =", corr_receipts)

# Scatterplot 1
plt.figure()
plt.scatter(vote_pct, small_pct)
plt.xlabel("Vote %")
plt.ylabel("Small Donation %")
plt.title("Vote % vs Small Donation %")
plt.show()

# Scatterplot 2
plt.figure()
plt.scatter(vote_pct, receipt_pct)
plt.xlabel("Vote %")
plt.ylabel("Total Receipts %")
plt.title("Vote % vs Total Receipts %")
plt.show()
