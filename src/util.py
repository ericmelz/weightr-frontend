import pandas as pd
import requests


DEVELOPMENT_ENV = 'dev.docker'
DEVELOPMENT_ENV_TO_WEIGHT_URL = {
    'dev': 'http://localhost/local-weight',
    'dev.docker': 'http://localhost/k3d-weight',
    'prod': 'http://weightr-backend/weight'
}
WEIGHT_URL = DEVELOPMENT_ENV_TO_WEIGHT_URL.get(DEVELOPMENT_ENV, 'http://localhost/local-weight')


def load_weight_data(session_id):
    resp = requests.get(WEIGHT_URL, params={"session_id": session_id})
    if resp.status_code == 200:
        data = resp.json()
        df = pd.DataFrame(data)

        df['Date'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('Date', inplace=True)
        df.drop(columns='timestamp', inplace=True)
        df.rename(columns={'weight_lbs': 'Weight (lb)'}, inplace=True)
        df['Year'] = df.index.year
        df['Day of Year'] = df.index.dayofyear
        return df
    else:
        # TODO make this better
        raise Exception(f"Error while fetching data: {resp.status_code}\n")
