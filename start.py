from py_clob_client.client import ClobClient
from dotenv import load_dotenv
import os
import json
import base64
import datetime

load_dotenv()

host: str = "https://clob.polymarket.com"
key: str = os.getenv("PolymarketSecret")
chain_id: int = 137

### Initialization of a client that trades directly from an EOA
client = ClobClient(host, key=key, chain_id=chain_id)
creds = client.create_or_derive_api_creds()

client.set_api_creds(creds)

def writeData():
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
                        listofMarket.append(market)
        if markets["next_cursor"] == "LTE=":
            break
        cursor = markets["next_cursor"]
    with open(f"markets.json", "w") as f:
      json.dump(listofMarket, f)



client.get_order_book("46233341984141805339503017327792472865621457040314248924266388854799239420097")



        




# print(client.get_sampling_markets())
# print(client.get_sampling_simplified_markets())

