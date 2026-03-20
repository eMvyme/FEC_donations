import donation_data


def pull_page_of_candidates(term, candidate_type, page):
    ''''term is the end of congress's term, candidiate type = (house = H, senate = S)'''
    params = {
        "page": page,
        "cycle": term,
        "office": candidate_type.upper(),
        "election_full": True,
        "sort": "name",
        "sort_hide_null": False,
        "sort_null_only": False,
        "sort_nulls_last": False,
    }

    json_candidates = donation_data.fec_api_call('/candidates/', params=params, results=False)
    pages = json_candidates['pagination']['pages']
    candidate_list_raw = [pages]
    for candidate in json_candidates['results']:
        candidate_dict = {
            "candidate_id": candidate["candidate_id"],
            "office_type": candidate["office"],
            "term": term,
            "state": candidate['state'],
            "district": candidate["district"],
            "name": candidate['name'],
        }
        candidate_list_raw.append(candidate_dict)
    return candidate_list_raw


def pull_all_candidates_term_type(term, candidate_type):
    page = 1
    first_raw_list = pull_page_of_candidates(term, candidate_type, page)
    total_pages = int(first_raw_list[0])
    first_raw_list.pop(0)
    list_of_candidates_term_type = [first_raw_list]
    page += 1
    while page <= total_pages:
        temp_raw_list = pull_page_of_candidates(term, candidate_type, page)
        temp_raw_list.pop(0)
        list_of_candidates_term_type.extend(temp_raw_list)
        page += 1
    return list_of_candidates_term_type


print(pull_all_candidates_term_type(2024, "s"))

