import ccxt
import time
from coinhub import models


# store best price data in db
def save_data(coin_type, update):
    models.ExchangeInfo.objects.update_or_create(name=coin_type,
                                                 defaults=update)

# Find the best price to sell/buy for a currency type and store in db
def collect():

    exchanges = ccxt.exchanges
    coin_types = ["XRP/ETH","XRP/BTC",'ETH/BTC','BTC/ETH'] # add more currencies to config file

    for coin_type in coin_types:
        buy_low_price = 99999999999.0
        buy_low_ex = ""
        sell_high_price = 0.0
        sell_high_ex = ""
        found = False

        # look at each exchange for the best price
        for exchange in exchanges:
            exchange_name = eval ('ccxt.%s ()' % exchange)
            try:
                data = exchange_name.fetch_ticker(coin_type)

                # check if price is better
                if float(data['info']['buy']) < buy_low_price:
                    buy_low_price = float(data['info']['buy']) 
                    buy_low_ex = exchange
                    found = True
                if float(data['info']['sell']) > sell_high_price:
                    sell_high_price = float(data['info']['sell']) 
                    sell_high_ex = exchange
                    found  = True
            except:        
                pass

        # if we found a new best then we update the db
        if found:
            update = {"name": coin_type,
                      "buy_price": buy_low_price,
                      "buy_ex": buy_low_ex,
                      "sell_price": sell_high_price,
                      "sell_ex": sell_high_ex}
            save_data(coin_type, update)

        time.sleep(3) # limit api calls


if __name__ == "__main__":
    collect()