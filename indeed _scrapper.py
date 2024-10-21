from apify_client import ApifyClient
import pandas as pd
import json
import os

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_qaNaAtiOJ8i3pQjQXjZqV6q3Hn0nUO0NDKVu")

# Prepare the Actor input
run_input = {
    "position": "web developer",
    "country": "US",
    "location": "San Francisco",
    "maxItems": 50,
    "parseCompanyDetails": False,
    "saveOnlyUniqueItems": True,
    "followApplyRedirects": False,
}
data=[]
# Run the Actor and wait for it to finish
run = client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)

# Fetch and collect Actor results from the run's dataset
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    data.append(item)

# If data, save data as JSON
if data:
    json_filename = "scraped_data.json"
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file created: {json_filename}")

# Convert the data to a Pandas DataFrame for CSV export
df = pd.DataFrame(data)
