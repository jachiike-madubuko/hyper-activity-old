import pandas as pd
import requests
import json

# https://curlconverter.com/
cookies = {
    'leafly-location': '%7B%22coordinates%22%3A%7B%22latitude%22%3A45.6684%2C%22longitude%22%3A-111.2422%2C%22accuracy_radius%22%3A124%2C%22accuracy_radius_units%22%3A%22mi%22%7D%2C%22slug%22%3A%22bozeman-mt-us%22%2C%22sublocality%22%3A%22%22%2C%22city%22%3A%22Bozeman%22%2C%22state%22%3A%22Montana%22%2C%22country%22%3A%22United%20States%22%2C%22zip%22%3A%2259718%22%2C%22state_code%22%3A%22MT%22%2C%22country_code%22%3A%22US%22%2C%22formatted_location%22%3A%22Bozeman%2C%20MT%22%2C%22place_id%22%3A%22%22%2C%22isUserLocation%22%3Atrue%2C%22street%22%3A%7B%22name%22%3A%22%22%2C%22number%22%3A%22%22%7D%7D',
    'leafly.browser.session': 'eyJzcGxpdEtleSI6ImVmMTY4ZWQ0ZjMwYjBhYmFjNDc4ZTcxOGJiMDU1ZDE4IiwiaWQiOiJlZjE2OGVkNGYzMGIwYWJhYzQ3OGU3MThiYjA1NWQxOCJ9',
    'X-Leafly-Id': '04fd6a18-3413-4945-9531-cfcf9bd7522e',
    'userMedRecPreference': 'Rec',
}

headers = {
    'authority': 'consumer-api.leafly.com',
    'accept': 'application/json',
    'accept-language': 'en-GB,en;q=0.6',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'leafly-location=%7B%22coordinates%22%3A%7B%22latitude%22%3A45.6684%2C%22longitude%22%3A-111.2422%2C%22accuracy_radius%22%3A124%2C%22accuracy_radius_units%22%3A%22mi%22%7D%2C%22slug%22%3A%22bozeman-mt-us%22%2C%22sublocality%22%3A%22%22%2C%22city%22%3A%22Bozeman%22%2C%22state%22%3A%22Montana%22%2C%22country%22%3A%22United%20States%22%2C%22zip%22%3A%2259718%22%2C%22state_code%22%3A%22MT%22%2C%22country_code%22%3A%22US%22%2C%22formatted_location%22%3A%22Bozeman%2C%20MT%22%2C%22place_id%22%3A%22%22%2C%22isUserLocation%22%3Atrue%2C%22street%22%3A%7B%22name%22%3A%22%22%2C%22number%22%3A%22%22%7D%7D; leafly.browser.session=eyJzcGxpdEtleSI6ImVmMTY4ZWQ0ZjMwYjBhYmFjNDc4ZTcxOGJiMDU1ZDE4IiwiaWQiOiJlZjE2OGVkNGYzMGIwYWJhYzQ3OGU3MThiYjA1NWQxOCJ9; X-Leafly-Id=04fd6a18-3413-4945-9531-cfcf9bd7522e; userMedRecPreference=Rec',
    'if-none-match': 'W/"224a3f637e080602bd933b9d99864385"',
    'origin': 'https://www.leafly.com',
    'referer': 'https://www.leafly.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
    'x-app': 'web-web',
    'x-environment': 'prod',
}

response = requests.get('https://consumer-api.leafly.com/api/strain_playlists/v2?&skip=0&take=60&lat=45.6684&lon=-111.2422', cookies=cookies, headers=headers)

get_batch = lambda x: f'https://consumer-api.leafly.com/api/strain_playlists/v2?&skip={x*60}&take=60&lat=45.6684&lon=-111.2422'
strains_data = []


for i in range(103):
    url = get_batch(i)
    response = requests.get(url, cookies=cookies, headers=headers)
    data = response.json()
    try:
        strains_data.extend(iter(data['hits']['strain']))
    except Exception:
        print(f'failed to grab 60 at {60*i}')



# https://stackoverflow.com/a/41801708
strains_df = pd.concat([pd.json_normalize(v, sep='_') for v in strains_data])
strains_df.reset_index(drop=True, inplace=True)
strains_df.to_csv('strains.csv',index=False)

df = pd.read_csv('strains.csv')
print(df.head())