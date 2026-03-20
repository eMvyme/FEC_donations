import requests
import json
from keys import FEC_API_KEY, BASE_URL


def fec_api_call(path, params=None, results=True):
    """Makes a GET request to the FEC API and returns the JSON response."""
    if params is None:
        params = {}

    # Add the API key to the parameters
    params['api_key'] = FEC_API_KEY

    full_url = f"{BASE_URL}{path}"

    try:
        response = requests.get(full_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        # print(response.url)

        # The FEC API often returns results under a 'results' key for lists of objects
        if 'results' in data and results is True:
            return data['results']
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6+
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError:
        print(f"Could not decode JSON from response: {response.text}")

    return None


def candidate_search(candidate, state):
    """finds the campaign id of congressperson"""

    params = {
        "q": candidate,
        "state": state,
        "sort": "name",
        "sort_hide_null": "false",
        "sort_null_only": "false",
        "sort_nulls_last": "false",
        "api_key": FEC_API_KEY,
    }
    # Search for Candidate name to get his candidate ID
    candidates = fec_api_call('/candidates', params=params)

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


def pull_candidate_donations_data(candidate, state, term):

    # pull api
    candidate_fec_id = candidate_search(candidate, state)
    fec_id_to_donations(candidate_fec_id, term)


def fec_id_to_donations(candidate_fec_id, term):
    params = {
        "page": 1,
        "election_full": False,
        "cycle": term,
        "sort": "-cycle",
        "sort_hide_null": False,
        "sort_null_only": False,
        "sort_nulls_last": False,
    }
    profile_fin_summary = fec_api_call(f"/candidate/{candidate_fec_id}/totals/", params=params)

    # pull data
    if profile_fin_summary:
        if len(profile_fin_summary) != 1:
            print(str(len(profile_fin_summary["results"])) + "IDs found")
        else:
            individual_unitemized_contributions = profile_fin_summary[0]["individual_unitemized_contributions"]
            total_receipts = profile_fin_summary[0]["receipts"]
            return individual_unitemized_contributions, total_receipts


# unit test->
# print(pull_candidate_donations_data("ro khanna", "CA", 2024))

'''small_donations, total_receipts = fec_id_to_donations('H4CA12055', 2014)
print(small_donations)
print(total_receipts)'''
