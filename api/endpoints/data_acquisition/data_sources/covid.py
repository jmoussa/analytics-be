import json

import pandas as pd
import requests

from ....cache import REDIS
from ....config import Config


class CovidAggregator:
    def __init__(self):
        self.states_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

    def get_data(self, limit: int) -> dict:
        states_data = self.get_states_data_from_cache()
        if limit > 0:
            states_data = states_data[:limit]
        return states_data

    def get_states_data(self) -> dict:
        response = requests.get(self.states_url)
        csv_data = response.content.decode("utf-8")
        df = pd.read_csv(csv_data)
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        return parsed

    def get_states_data_from_cache(self) -> dict:
        result = REDIS.get("covid_states_data")
        if result:
            return json.loads(result)
        else:
            result = self.get_states_data()
            self.set_states_data_to_cache(result)
            return result

    def set_states_data_to_cache(self, data: dict):
        REDIS.set("covid_states_data", data, ex=Config.REDIS_EXPIRE)
