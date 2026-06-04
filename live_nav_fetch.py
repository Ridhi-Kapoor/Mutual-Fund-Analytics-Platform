import requests
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url)

print(response.status_code)

data = response.json()
print(data.keys())
print(data["meta"])


nav_df = pd.DataFrame(data["data"])
nav_df.head()

nav_df.to_csv(
    "data/raw/hdfc_top100_live_nav.csv",
    index=False
)

schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}
for name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    data = response.json()

    nav_df = pd.DataFrame(data["data"])

    file_name = f"data/raw/{name}_nav.csv"

    nav_df.to_csv(
        file_name,
        index=False
    )

    print(f"Saved {file_name}")