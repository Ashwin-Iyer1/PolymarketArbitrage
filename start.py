from py_clob_client.client import ClobClient
from dotenv import load_dotenv
import os
import json
import base64
import datetime
import itertools 

load_dotenv()

host: str = "https://clob.polymarket.com"
key: str = os.getenv("PolymarketSecret")
chain_id: int = 137

### Initialization of a client that trades directly from an EOA
client = ClobClient(host, key=key, chain_id=chain_id)
creds = client.create_or_derive_api_creds()

client.set_api_creds(creds)

def writeData(data, name):
    with open(f"{name}.json", "w") as f:
      json.dump(data, f)


def getData(tag: str = None):
    today = datetime.datetime.now()
    #save to json
    num = 20000
    listofMarket = []
    cursor = base64.b64encode(str(num).encode()).decode()
    while True:
        markets = client.get_markets(next_cursor=cursor)
        for market in markets["data"]:
            if(market["end_date_iso"] != None):
                if(today < datetime.datetime.fromisoformat(market["end_date_iso"][:-1])):
                    if(market["is_50_50_outcome"] == False):
                        if(market["closed"] != True and market["active"] == True):
                            if tag != None:
                                if tag in market["tags"]:
                                    listofMarket.append(market)
                            else:
                                listofMarket.append(market)
        if markets["next_cursor"] == "LTE=":
            break
        cursor = markets["next_cursor"]
    return listofMarket





def parse_data(range: int, MarketsList: list, DTEMax: int, DTEMin: int):
    parsed_data = []

    for market in MarketsList:
        enddate = datetime.datetime.fromisoformat(market["end_date_iso"][:-1])
        startdate = datetime.datetime.fromisoformat(market["accepting_order_timestamp"][:-1])
        DTEcalc = datetime.datetime.fromisoformat(market["end_date_iso"][:-1]) - datetime.datetime.now()
        if market["end_date_iso"] != None:
            if(enddate - startdate > datetime.timedelta(days=range)):
                parsed_data.append(market)
    return parsed_data



def getMarket(market):
    return client.get_market(market)

def getTokenIDS(market):
    tokens = []
    for token in market["tokens"]:
        tokens.append(token["token_id"])
    return tokens

def getOrderBook(token):
    result = client.get_order_book(token)
    return result

def getPopularity(OrderBook):
    OrderBook.json()


with open("ParsedPoliticsMarkets.json", "r") as f:
    data = json.load(f)


def main():
    marketsSorted = {}
    for market in data:
        sample_data = getTokenIDS(market)
        for token in sample_data:
            new_data = getOrderBook(token)
            total = 0
            for order in new_data.bids:
                total += float(order.size)
            for order in new_data.asks:
                total += float(order.size)
            marketsSorted[market["condition_id"]] = total

    sortedDict = dict(sorted(marketsSorted.items(), key=lambda item: item[1], reverse=True))
    top5 = dict(list(sortedDict.items())[0: 5])
    for key in top5:
        print(key, top5[key])
        print("buy spread at " + str(getMarket(key)["tokens"][0]["price"]))

main()
# sample_data = getData("Politics")




# new_data = parse_data(14, sample_data, 5, 2)

# writeData(new_data, "ParsedPoliticsMarkets")




# print(client.get_sampling_markets())
# print(client.get_sampling_simplified_markets())

