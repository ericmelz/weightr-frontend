import pandas as pd
import requests


def load_weight_data(session_id):
    resp = requests.get("http://localhost/weight", params={"session_id": session_id})
    if resp.status_code == 200:
        data = resp.json()
        df = pd.DataFrame(data, columns=['timestamp', 'weight'])

        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('datetime', inplace=True)
        df.drop(columns='timestamp', inplace=True)
        return df
    else:
        # TODO make this better
        raise Exception(f"Error while fetching data: {resp.status_code}")
