import pandas as pd
from difflib import SequenceMatcher

# Load
fec = pd.read_csv("house2024/FEC_bulkdata2.csv", dtype=str)
house = pd.read_csv("house2024/house_candidates.csv", dtype=str)

"""some of the names in FEC are messed up (missing commas, incomplete, no spaces) would increase data if cleaned up"""
fec = fec.dropna(subset=["clean_name"])

merged = house.merge(
    fec,
    on=["state", "district", "party"],
    how="left",
    suffixes=("house", "fec")
)
pd.set_option("display.max_columns", 10)
merged = merged.drop(columns=["status", "party_og", "name", "campaign_id", "totalvotes", "candidate_name", "party_full"])

"""fix so that I don't have any #N/A"""
merged = merged.dropna()

# print(merged)

key_cols = ["state", "district", "party", "year"]
match_cols = ["clean_namehouse", "clean_namefec"]


# --- Similarity function ---
def similarity(a, b):
    if pd.isna(a) or pd.isna(b):
        return 0.0
    return SequenceMatcher(None, str(a), str(b)).ratio()


# --- Compute similarity row-wise ---
merged = merged.copy()
merged["similarity_score"] = merged.apply(
    lambda row: similarity(row[match_cols[0]], row[match_cols[1]]),
    axis=1
)

# --- For each key, keep row with highest similarity ---
result = (
    merged.sort_values("similarity_score", ascending=False)
      .drop_duplicates(subset=key_cols, keep="first")
      .reset_index(drop=True)
)

result = result[result["similarity_score"] >= 0.65]

# 0.8 = 18188, looks good
# 0.5 = 20788, all wrong
# 0.65 = 19490, looks fine

# result now has:
# one row per unique 3-column key with the most closely matching text columns

print(result)
result.to_csv("merged.csv")
