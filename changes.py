import json
from datetime import datetime

import requests

url = "https://gerrit-review.googlesource.com/changes/?q=project:gerrit+AND+not+dir:polygerrit-ui+AND+branch:master+AND+-age:4week&o=CURRENT_REVISION"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Remove the prefix ")]}'" from the response content
    json_content = response.text.lstrip(")]}'")

    # Parse the modified JSON data
    json_data = json.loads(json_content)

    # List to store changes
    changes = []

    # Iterate through each element in json_data
    for element in json_data:
        # Extract _number from the main object
        change_number = element["_number"]

        # Extract _number and sha1 from the revisions object
        revisions_object = element.get("revisions", {})
        total_revisions = None

        # Loop through the nested revisions object
        for revision_key, revision_value in revisions_object.items():
            total_revisions = revision_value.get("_number")
            revisions_sha1 = revision_key
            break  # Assuming there is only one revision, you can modify as needed

        # Append results to the list
        changes.append({"change_number": change_number, "total_revisions": total_revisions})

        # Print the changes
        # for change in changes:
        #     print(change)

    print(f"The number of results is {len(changes)}")

    changes_revisions = []
        # Iterate through each result and make HTTP requests
    for change in changes[:10]:
        change_number = change["change_number"]
        total_revisions = change["total_revisions"]

        # List to store changes
        # Make N HTTP requests for each revision
        for revision_number in range(1, total_revisions + 1):
            checks_url = f"https://gerrit-review.googlesource.com/changes/{change_number}/revisions/{revision_number}/checks"

            # Send a GET request to the checks URL
            checks_response = requests.get(checks_url)

            # Check if the request was successful (status code 200)
            if checks_response.status_code == 200:
                # Parse the JSON data
                # Remove the prefix ")]}'" from the response content
                checks_json_content = checks_response.text.lstrip(")]}'")

                # Parse the modified JSON data
                checks_json_data = json.loads(checks_json_content)

                # Now you can work with the checks JSON data as needed
                print(f"Checks data for {change_number} - Revision {revision_number}:")

                rbe_gcp_state = None
                rbe_gcp_start = None
                rbe_gcp_end = None
                rbe_bb_state = None
                rbe_bb_start = None
                rbe_bb_end = None

            # Loop through checks data to find relevant information
                for check_data in checks_json_data:
                    checker_name = check_data.get('checker_name', '')
                    if 'RBE GCP Build/Tests' in checker_name:
                        rbe_gcp_state = check_data.get('state')
                        rbe_gcp_start = check_data.get('started')
                        rbe_gcp_end = check_data.get('finished')
                    elif 'RBE BB Build/Tests' in checker_name:
                        rbe_bb_state = check_data.get('state')
                        rbe_bb_start = check_data.get('started')
                        rbe_bb_end = check_data.get('finished')

                if rbe_gcp_start and rbe_gcp_end:
                    rbe_gcp_start = rbe_gcp_start[:-3]
                    gcp_start_datetime = datetime.strptime(rbe_gcp_start, '%Y-%m-%d %H:%M:%S.%f')
                    rbe_gcp_end = rbe_gcp_end[:-3]
                    gcp_end_datetime = datetime.strptime(rbe_gcp_end, '%Y-%m-%d %H:%M:%S.%f')

                    # Calculate the difference in seconds
                    gcp_time_difference_seconds = (gcp_end_datetime - gcp_start_datetime).total_seconds()

                if rbe_bb_start and rbe_bb_end:
                    rbe_bb_start = rbe_bb_start[:-3]
                    bb_start_datetime = datetime.strptime(rbe_bb_start, '%Y-%m-%d %H:%M:%S.%f')
                    rbe_bb_end = rbe_bb_end[:-3]
                    bb_end_datetime = datetime.strptime(rbe_bb_end, '%Y-%m-%d %H:%M:%S.%f')

                    # Calculate the difference in seconds
                    bb_time_difference_seconds = (bb_end_datetime - bb_start_datetime).total_seconds()


                changes_revisions.append({
                    "change_number": change_number,
                    "revision_number": revision_number, # to fix
                    "rbe_gcp_state": rbe_gcp_state,
                    # "rbe_gcp_start": rbe_gcp_start,
                    # "rbe_gcp_end": rbe_gcp_end,
                    "rbe_gcp_time_seconds": gcp_time_difference_seconds,
                    "rbe_bb_state": rbe_bb_state,
                    # "rbe_bb_start": rbe_bb_start,
                    # "rbe_bb_end": rbe_bb_end,
                    "rbe_bb_time_seconds": bb_time_difference_seconds,
                })

            else:
                print(f"Failed to retrieve checks data for {change_number} - Revision {revision_number}. Status code: {checks_response.status_code}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

print(changes_revisions)