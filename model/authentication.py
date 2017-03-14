from config.options import AUTH_JSON
import json


class ConnectionParameters:
    def __init__(self, **kwargs):
        self.consumer_key = kwargs.get("consumer_key", "")
        self.consumer_secret = kwargs.get("consumer_secret", "")

        self.access_token = kwargs.get("access_token", "")
        self.access_token_secret = kwargs.get("access_token_secret", "")


def get_accounts():
    result = []
    with open(AUTH_JSON) as fp:
        accounts = json.load(fp)
        for account in accounts["accounts"]:
            params = {
              "consumer_key": account["consumer_key"],
              "consumer_secret": account["consumer_secret"],
              "access_token": account["access_token"],
              "access_token_secret": account["access_token_secret"]
            }
            conn_params = ConnectionParameters(**params)
            result.append(conn_params)
    return result
