import json

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

    # List to store results
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

    # Iterate through each result and make HTTP requests
for change in changes:
    change_number = change["change_number"]
    total_revisions = change["total_revisions"]

    # Make N HTTP requests for each revision
    for n in range(1, total_revisions + 1):
        checks_url = f"https://gerrit-review.googlesource.com/changes/{change_number}/revisions/{n}/checks"

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
            print(f"Checks data for {change_number} - Revision {n}:")
            print(checks_json_data)
        else:
            print(f"Failed to retrieve checks data for {change_number} - Revision {n}. Status code: {checks_response.status_code}")

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
