## WATCHER IMPORTS ###
from distutils.command import check
from hashlib import new
from requests import session as sesh, get
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from collections import OrderedDict
from re import compile
import os
import configparser
config = configparser.ConfigParser()		
parentdir = os.path.dirname(__file__)
config.read("/".join([parentdir,"config.ini"]))
from rich.table import Table, box
from rich.console import Console

## GUI IMPORTS ##
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import ImageTk, Image
import json
from io import BytesIO
import urllib.request
from datetime import date
from itertools import cycle
from tkVideoPlayer import TkinterVideo
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gui", help = "Display or not the GUI window")
args = vars(parser.parse_args())

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def url_image(link, size, skinname):
    longs = ['vandal', 'phantom', 'operator', 'shorty', 'frenzy', 'sheriff', 'ghost', 'stinger', 'spectre', 'bucky', 'judge', 'bulldog', 'marshall', 'ares', 'odin']
    theweapon = (skinname.split(" ")[-1:][0]).lower()
    checklong = theweapon in longs
    if checklong == True: #weapons
        pixels_x, pixels_y = 150, 45
    else:
        if size == 'big': #bundle
            pixels_x, pixels_y = 547, 237
        else: #melees
            pixels_x, pixels_y = 100, 45
    with urllib.request.urlopen(link) as u:
        raw_data = u.read()
    image = Image.open(BytesIO(raw_data)).resize((pixels_x, pixels_y))
    return ImageTk.PhotoImage(image)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

def MainGui():
    window = Tk()
    window.geometry("779x417")
    window.configure(bg = "#081527")
    window.title('Valorant Store Watcher')

    dailyshop = json.load(open("/".join([parentdir,'dailyshop.json'])))
    bundle_name = dailyshop['Bundle']['bundle_name']
    bundle_image = dailyshop['Bundle']['bundle_image']
    bundle_price = dailyshop['Bundle']['bundle_price']
    skin1_image = dailyshop['Skins']['skin1']['skin1_image']
    skin1_name = dailyshop['Skins']['skin1']['skin1_name']
    skin1_price = dailyshop['Skins']['skin1']['skin1_price']
    skin1_video = dailyshop['Skins']['skin1']['skin1_video']
    skin2_image = dailyshop['Skins']['skin2']['skin2_image']
    skin2_name = dailyshop['Skins']['skin2']['skin2_name']
    skin2_price = dailyshop['Skins']['skin2']['skin2_price']
    skin2_video = dailyshop['Skins']['skin2']['skin2_video']
    skin3_image = dailyshop['Skins']['skin3']['skin3_image']
    skin3_name = dailyshop['Skins']['skin3']['skin3_name']
    skin3_price = dailyshop['Skins']['skin3']['skin3_price']
    skin3_video = dailyshop['Skins']['skin3']['skin3_video']
    skin4_image = dailyshop['Skins']['skin4']['skin4_image']
    skin4_name = dailyshop['Skins']['skin4']['skin4_name']
    skin4_price = dailyshop['Skins']['skin4']['skin4_price']
    skin4_video = dailyshop['Skins']['skin4']['skin4_video']
    valorant_points_amount = dailyshop['ValorantPoints_amount']
    radianite_points_amount = dailyshop['RadianitePoints_amount']

    def videoPlayer(videolink):
        videoplayerwindow = Tk()
        videoplayerwindow.geometry("500x280")
        videoplayer = TkinterVideo(master=videoplayerwindow, scaled=True)
        videoplayer.load(rf"{videolink}")
        videoplayer.pack(expand=True, fill="both")
        videoplayer.play() # play the video
        videoplayerwindow.mainloop()

    canvas = Canvas(
        window,
        bg = "#081527",
        height = 417,
        width = 779,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        22.0,
        280.0,
        anchor="nw",
        text="VALORANT",
        fill="#DC3D4B",
        font=("VALORANT", 64 * -1)
    )

    canvas.create_text(
        197.0,
        342.0,
        anchor="nw",
        text="SHOP",
        fill="#DC3D4B",
        font=("VALORANT", 64 * -1)
    )

    image_image_1 = url_image(bundle_image, 'big', bundle_name)
    image_1 = canvas.create_image(
        295.0,
        146.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("valopoints.png"))
    image_2 = canvas.create_image(
        610.0,
        180.0,
        image=image_image_2
    )

    canvas.create_text(
        628.0,
        175.0,
        anchor="nw",
        text=skin2_price,
        fill="#FFFFFF",
        font=("VALORANT", 13 * -1)
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("valopoints.png"))
    image_3 = canvas.create_image(
        610.0,
        300.0,
        image=image_image_3
    )

    canvas.create_text(
        628.0,
        295.0,
        anchor="nw",
        text=skin3_price,
        fill="#FFFFFF",
        font=("VALORANT", 13 * -1)
    )

    canvas.create_text(
        601.0,
        375.0,
        anchor="nw",
        text=skin3_name,
        fill="#FFFFFF",
        font=("VALORANT", 12 * -1)
    )

    canvas.create_text(
        417.0,
        375.0,
        anchor="nw",
        text=skin4_name,
        fill="#FFFFFF",
        font=("VALORANT", 12 * -1)
    )

    image_image_4 = url_image(skin1_image, 'melee', skin1_name)
    image_4 = canvas.create_image(
        663.0,
        73.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(file=relative_to_assets("valopoints.png"))
    image_5 = canvas.create_image(
        610.0,
        50.0,
        image=image_image_5
    )

    canvas.create_text(
        628.0,
        45.0,
        anchor="nw",
        text=skin1_price,
        fill="#FFFFFF",
        font=("VALORANT", 13 * -1)
    )

    canvas.create_text(
        681.0,
        11.0,
        anchor="nw",
        text=date.today().strftime("%d/%m/%Y"),
        fill="#FFFFFF",
        font=("VALORANT", 12 * -1)
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("valopoints.png"))
    image_6 = canvas.create_image(
        64.0,
        366.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("valopoints.png"))
    image_7 = canvas.create_image(
        535.0,
        244.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("radianite.png"))
    image_8 = canvas.create_image(
        64.0,
        391.0,
        image=image_image_8
    )

    canvas.create_text(
        82.0,
        361.0,
        anchor="nw",
        text=valorant_points_amount,
        fill="#FFFFFF",
        font=("VALORANT", 13 * -1)
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("valopoints.png"))
    image_9 = canvas.create_image(
        419.0,
        300.0,
        image=image_image_9
    )

    canvas.create_text(
        437.0,
        295.0,
        anchor="nw",
        text=skin4_price,
        fill="#FFFFFF",
        font=("VALORANT", 13 * -1)
    )

    canvas.create_text(
        486.0,
        237.0,
        anchor="nw",
        text=bundle_price,
        fill="#FFFFFF",
        font=("VALORANT", 15 * -1)
    )

    canvas.create_text(
        82.0,
        386.0,
        anchor="nw",
        text=radianite_points_amount,
        fill="#FFFFFF",
        font=("VALORANT", 13 * -1)
    )

    canvas.create_text(
        40.0,
        229.0,
        anchor="nw",
        text=bundle_name,
        fill="#FFFFFF",
        font=("VALORANT", 24 * -1)
    )

    canvas.create_text(
        601.0,
        103.0,
        anchor="nw",
        text=skin1_name,
        fill="#FFFFFF",
        font=("VALORANT", 12 * -1)
    )

    canvas.create_text(
        601.0,
        236.0,
        anchor="nw",
        text=skin2_name,
        fill="#FFFFFF",
        font=("VALORANT", 12 * -1)
    )

    image_image_10 = url_image(skin2_image, '', skin2_name)
    image_10 = canvas.create_image(
        668.0,
        209.0,
        image=image_image_10
    )

    image_image_11 = url_image(skin3_image, '', skin3_name)
    image_11 = canvas.create_image(
        670.9556884765625,
        341.7883071899414,
        image=image_image_11
    )

    image_image_12 = url_image(skin4_image, '', skin4_name)
    image_12 = canvas.create_image(
        476.0,
        341.0,
        image=image_image_12
    )
    window.resizable(False, False)
    window.mainloop()
    
    with open("/".join([parentdir,'dailyshop.json']), 'r+') as jsf: jsf.truncate(0)

## VALOSTORE WATCHER ##
def checker():
    acc =  config['LOGIN']
    username = acc['riot_username']
    password = acc['password']
    region = acc['region']
    if username == 'xxx':
        print('Please insert a riot username in config.ini')
    if password == 'xxx':
        print('Please insert a password in config.ini')
    if region == 'xxx':
        print('Please insert a region in config.ini')
    headers = OrderedDict({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*",
        'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)'
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
        'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)',
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
        'User-Agent': 'RiotClient/58.0.0.4640299.4552318 rso-auth (Windows;10;;Professional, x64)',
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
    with session.get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{puuid}', headers=headers2, json=json2) as r:
        data = r.json()
    weapon_fetch = get(f'https://valorant-api.com/v1/weapons/skinlevels')
    weapon_fetch = weapon_fetch.json()
    of_data = get(f"https://pd.{region}.a.pvp.net/store/v1/offers/", headers=headers2)
    offers_data = of_data.json()
    # with open('offersdata.json', 'a') as f: f.write(json.dumps(offers_data, indent = 4))
    GetPoints = get(f"https://pd.{region}.a.pvp.net/store/v1/wallet/{sub}",headers=headers2)
    ValorantPoints = GetPoints.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
    Radianite = GetPoints.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]

    ## bundles ##

    bundles_uuid = [] ## list of current bundles
    bundle_prices = []
    feautured_bundles = data['FeaturedBundle']
    time = convert_time(feautured_bundles['BundleRemainingDurationInSeconds'])
    if len(feautured_bundles['Bundles']) > 1:
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
    bundles_images = []
    current_bundles = []
    for bundle in bundles_uuid:
        with session.get(f'https://valorant-api.com/v1/bundles/{bundle}', headers=headers) as r:
            data = r.json()
        current_bundles.append(data['data']['displayName'])
        bundles_images.append(data['data']['displayIcon'])

    ## DISPLAY ##
    if not args['gui']:
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
    else:
        def write_json(new_data, filename="/".join([parentdir,'dailyshop.json'])):
            with open(filename, 'r+') as file:
                file.seek(0)
                json.dump(new_data, file, indent=4)
        
        shop = {
            "Bundle":{
                "bundle_name": current_bundles[0],
                "bundle_image": bundles_images[0],
                "bundle_price": str(bundle_prices[0])
            },
            "Skins":{
                "skin1":{
                    "skin1_name": skin_names[0],
                    "skin1_image": skin_images[0],
                    "skin1_price": singleweapons_prices[0],
                    "skin1_video": skin_videos[0],
                },
                "skin2":{
                    "skin2_name": skin_names[1],
                    "skin2_image": skin_images[1],
                    "skin2_price": singleweapons_prices[1],
                    "skin2_video": skin_videos[1],
                },
                "skin3":{
                    "skin3_name": skin_names[2],
                    "skin3_image": skin_images[2],
                    "skin3_price": singleweapons_prices[2],
                    "skin3_video": skin_videos[2],
                },
                "skin4":{
                    "skin4_name": skin_names[3],
                    "skin4_image": skin_images[3],
                    "skin4_price": singleweapons_prices[3],
                    "skin4_video": skin_videos[3],
                }
            },
            "ValorantPoints_amount": ValorantPoints,
            "RadianitePoints_amount": Radianite,
        }

        write_json(shop)
        MainGui()

checker()
