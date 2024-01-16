import json
from datetime import datetime
import csv
import requests

def get_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_content = response.text.lstrip(")]}'")
        return json.loads(json_content)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def extract_revision_data(element):
    change_number = element["_number"]
    revisions_object = element.get("revisions", {})

    for revision_key, revision_value in revisions_object.items():
        total_revisions = revision_value.get("_number")
        break

    return {"change_number": change_number, "total_revisions": total_revisions}

def get_checks_data(change_number, revision_number):
    checks_url = f"https://gerrit-review.googlesource.com/changes/{change_number}/revisions/{revision_number}/checks"
    return get_json_data(checks_url)

def process_checks_data(checks_json_data):
    rbe_gcp_started, rbe_gcp_state, rbe_gcp_start, rbe_gcp_end, rbe_bb_started, rbe_bb_state, rbe_bb_start, rbe_bb_end = None, None, None, None, None, None, None, None

    for check_data in checks_json_data:
        checker_name = check_data.get('checker_name', '')
        if 'RBE GCP Build/Tests' in checker_name:
            rbe_gcp_started = check_data.get('started')
            rbe_gcp_state = check_data.get('state')
            rbe_gcp_start = check_data.get('started')
            rbe_gcp_end = check_data.get('finished')
        elif 'RBE BB Build/Tests' in checker_name:
            rbe_bb_started = check_data.get('started')
            rbe_bb_state = check_data.get('state')
            rbe_bb_start = check_data.get('started')
            rbe_bb_end = check_data.get('finished')

    return rbe_gcp_started, rbe_gcp_state, rbe_gcp_start, rbe_gcp_end, rbe_bb_started, rbe_bb_state, rbe_bb_start, rbe_bb_end

def calculate_time_difference(start, end):
    if start and end:
        start = start[:-3]
        start_datetime = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        end = end[:-3]
        end_datetime = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        diff_datetime = end_datetime - start_datetime

        return diff_datetime.total_seconds(), round(diff_datetime.total_seconds() / 60, 2)
    else:
        return None, None

####### Main body
list_changes = "https://gerrit-review.googlesource.com/changes/?q=project:gerrit+AND+not+dir:polygerrit-ui+AND+branch:stable-3.7+AND+-age:4week&o=CURRENT_REVISION"
changes_json = get_json_data(list_changes)

if changes_json:
    changes = [extract_revision_data(element) for element in changes_json]
    print(f"The number of changes is {len(changes)}")

    changes_revisions = 0

    for change in changes:
        change_number = change["change_number"]
        total_revisions = change["total_revisions"]

        for revision_number in range(1, total_revisions + 1):
            checks_json_data = get_checks_data(change_number, revision_number)
            if any(check['checker_name'] == 'RBE GCP Build/Tests' for check in checks_json_data):
                if any(check['checker_name'] == 'RBE BB Build/Tests' for check in checks_json_data):
                    print("with BB")
                print(f"Processing change: {change_number} and revision: {revision_number}")
                changes_revisions = changes_revisions + 1

    print(f"The total number of records (changes*revision) is {changes_revisions}")
