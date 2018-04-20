from coinhub import models
import datetime
import json
import requests


# Class to pull data from a specific exchange
class CoinDataPuller():
    exchange_url = ""
    exchange_data = {}

    def __init__(self, url):
        self.exchange_url = url

    # collect the data from the api
    def collect_new_data(self):
        return_data = requests.get(self.exchange_url)
        self.exchange_data = json.loads(return_data.text)
        for item in self.exchange_data:
            for key in item:
                if item[key] is None:
                    item[key] = "0"

    # store the data from coin market cap in two tables
    def save_all(self):
        
        for coin in self.exchange_data:
            # update our current data table
            updates = {"circulating_supply": float(coin["available_supply"]),
                       "market_cap": float(coin["market_cap_usd"]),
                       "name": coin["name"],
                       "price": float(coin["price_usd"]),
                       "price_change_day": float(coin["percent_change_24h"]),
                       "price_change_hour": float(coin["percent_change_1h"]),
                       "price_change_week": float(coin["percent_change_7d"]),
                       "rank": coin["rank"],
                       "volume": float(coin["total_supply"])}
            models.CurrentCoinInfo.objects.update_or_create(symbol=coin["symbol"],
                                                 defaults=updates)

            # Update our storage of old data
            previous_data = models.GraphData(
                    circulating_supply=float(coin["available_supply"]),
                    time_collected = datetime.datetime.fromtimestamp(
                            int(coin["last_updated"])),
                    historical_price=float(coin["price_usd"]),
                    market_cap=float(coin["market_cap_usd"]),
                    name=coin["name"],
                    volume=float(coin["total_supply"]))
            previous_data.save()

    def save(self):
        return self.save_all()
