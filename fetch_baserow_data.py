import requests
import json

# Baserow API details
BASEROW_API_URL = "https://api.baserow.io/api/database/rows/table/{table_id}/?user_field_names=true"
BASEROW_TOKEN = "d24Fgp0biNFra1zobQoBkdffu32m8tou"
TABLE_ID = "431178"

# Fetch data from Baserow
headers = {
    "Authorization": f"Token {BASEROW_TOKEN}"
}
response = requests.get(BASEROW_API_URL.format(table_id=TABLE_ID), headers=headers)

if response.status_code == 200:
    data = response.json()
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Data fetched and saved to data.json")
else:
    print(f"Error fetching data: {response.status_code}")
