import pandas as pd
import donation_data as pull


def find_id_from_csv(candidate, state_po):
    """finds the campaign id of congressperson"""

    params = {
        "q": candidate.lower(),
        "sort": "name",
        "office": "H",
        "state": state_po,
        "sort_hide_null": "false",
        "sort_null_only": "false",
        "sort_nulls_last": "false",
    }
    # Search for Candidate name to get his candidate ID
    candidates = pull.fec_api_call('/candidates/search/', params=params)

    # Assuming the first result is the correct one, print the candidate ID
    candidate_id = None

    if candidates:
        if len(candidates) != 1:
            print(str(len(candidates)) + "IDs found")
        for each_candidate in candidates:
            candidate_id = each_candidate['candidate_id']
            print(f"Found your candidate! Candidate ID: {each_candidate['candidate_id']}")
        return candidate_id

    if not candidate_id:
        print("Could not find candidate ID. Please check the name or refine the search.")


df = pd.read_csv('house2024/house_candidates.csv')
test_candidate_row = 9997

tracked_candidates = 0
for row in range(pd.options.display.max_rows):
    if df.iloc[row]["writein"] == False:
        if find_id_from_csv(df.iloc[row]["candidate_name"], df.iloc[row]["state_po"]) != None:
            tracked_candidates += 1
            print(df.iloc[row]["candidate_name"])

        else: print("test")
    else:
        print("writein")
        tracked_candidates += 1
