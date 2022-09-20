from requests import session as sesh, get
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from collections import OrderedDict
from re import compile
import configparser
config = configparser.ConfigParser()		
config.read("config.ini")
from rich.table import Table, box
from rich.console import Console

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=PROTOCOL_TLSv1_2)

def convert_time(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60
   return "%02d:%02d:%02d" % (hour, min, sec) 

def price_retriver(skinUuid, offers_data):
    for row in offers_data["Offers"]:
        if row["OfferID"] == skinUuid:
            for cost in row["Cost"]:
                return row["Cost"][cost]

def checker():
    acc =  config['LOGIN']
    username = acc['riot_username']
    password = acc['password']
    headers = OrderedDict({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*",
        'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)'
    })
    session = sesh()
    session.headers = headers
    session.mount('https://', TLSAdapter())
    data = {
        "client_id": "play-valorant-web-prod",
        "nonce": "1",
        "redirect_uri": "https://playvalorant.com/opt_in",
        "response_type": "token id_token",
        'scope': 'account openid',
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
    }
    r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    r2 = session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    data = r2.json()
    if "access_token" in r2.text:
        pattern = compile(
            'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(data['response']['parameters']['uri'])[0]
        token = data[0]

    elif "auth_failure" in r2.text:
        print("banned")
    else:
        print("Failed. Probably u have 2FA activated")
    headers = {
        'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
        'Authorization': f'Bearer {token}',
    }
    r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
    entitlement = r.json()['entitlements_token']
    r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    data = r.json()
    puuid = data['sub']
    name = data['acct']['game_name']+'#'+data['acct']['tag_line']
    sub = r.text.split('sub":"')[1].split('"')[0]

    ## GET SKINS ##

    headers2 = {'Authorization': f'Bearer {token}', 'X-Riot-Entitlements-JWT': entitlement, 'Content-Type': 'text/plain'}
        
    json2 = [puuid]
    with session.get(f'https://pd.eu.a.pvp.net/store/v2/storefront/{puuid}', headers=headers2, json=json2) as r:
        data = r.json()
    weapon_fetch = get(f'https://valorant-api.com/v1/weapons/skinlevels')
    weapon_fetch = weapon_fetch.json()
    of_data = get(f"https://pd.eu.a.pvp.net/store/v1/offers/", headers=headers2)
    offers_data = of_data.json()
    GetPoints = get(f"https://pd.eu.a.pvp.net/store/v1/wallet/{sub}",headers=headers2)
    ValorantPoints = GetPoints.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
    Radianite = GetPoints.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]

    ## bundles ##

    bundles_uuid = [] ## list of current bundles
    bundle_prices = []
    feautured_bundles = data['FeaturedBundle']
    time = convert_time(feautured_bundles['BundleRemainingDurationInSeconds'])
    if len(feautured_bundles['Bundle']) > 1:
        bundles = [feautured_bundles['Bundles'][0], feautured_bundles['Bundles'][1]]
        for element in bundles: 
            bundle_uuid = element['DataAssetID']
            bundles_uuid.append(bundle_uuid)
            n = 0
            all_prices=[] 
            for i in range(len(element['Items'])):
                bundle_item_price = element['Items'][n]['DiscountedPrice']
                all_prices.append(bundle_item_price)
                n = n+1
            bundle_prices.append(sum(all_prices)) # price of the bundle
                
    else:
        bundles = [feautured_bundles['Bundle']]
        for element in bundles: 
                    bundle_uuid = element['DataAssetID']
                    bundles_uuid.append(bundle_uuid)
                    n = 0
                    all_prices=[] 
                    for i in range(len(element['Items'])):
                        bundle_item_price = element['Items'][n]['DiscountedPrice']
                        all_prices.append(bundle_item_price)
                        n = n+1
                    bundle_prices.append(sum(all_prices)) # price of the bundle

     ## daily shop ##
    singleweapons_prices = []
    daily_shop = data['SkinsPanelLayout']
    daily_items = daily_shop['SingleItemOffers'] # list of daily items
    for skin in daily_items:
        for row in weapon_fetch["data"]:
            if skin == row["uuid"]:
                skin_price = price_retriver(skin, offers_data)
                singleweapons_prices.append(skin_price) # prices of daily items

    skin_names = []
    skin_images = []
    skin_videos = []
    for item in daily_items:
        with session.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item}', headers=headers) as r:
            data = r.json()
        skin_names.append(data['data']['displayName']) # names of daily items
        skin_images.append(data['data']['displayIcon']) # images of of daily items
        skin_videos.append(data['data']['streamedVideo']) # videos of daily items

    ## bundles part 2 ##
    current_bundles = []
    for bundle in bundles_uuid:
        with session.get(f'https://valorant-api.com/v1/bundles/{bundle}', headers=headers) as r:
            data = r.json()
        current_bundles.append(data['data']['displayName'])

    ## DISPLAY ##
    table_one = Table(box=box.HORIZONTALS, show_header=True, header_style='bold #2070b2')
    table_one.add_column('Skin', justify='left')
    table_one.add_column('Price', justify='center')
    table_one.add_column('Visual', justify='center')
    n = 0
    for i in range(4):
        table_one.add_row(skin_names[n], str(singleweapons_prices[n]), skin_images[n])
        n = n+1

    table_two = Table(box=box.HORIZONTALS, show_header=True, header_style='bold #2070b2')
    table_two.add_column('Bundle', justify='left')
    table_two.add_column('Price', justify='center')
    table_two.add_column('Time Left', justify='center')
    n = 0
    for i in range(len(current_bundles)):
        table_two.add_row(current_bundles[n], str(bundle_prices[n]), str(time))
        n +=1
    for i in range(4-len(current_bundles)):
        table_two.add_row()

    table = Table(box=box.HEAVY_EDGE, show_header=True, title=f" ╔══ [bold]{name}'S DAILY STORE[/bold]\n ╠════ Valorant Points: [#2070b2]{ValorantPoints} VP [/#2070b2] \n ╚══════ Radianite Points: [#2070b2] {Radianite} R [/#2070b2]")
    table.add_column('DAILY ITEMS', justify='center')
    table.add_column('BUNDLES', justify='center')
    table.add_row(table_one, table_two)
    console = Console()
    console.print(table)

checker()
