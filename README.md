# Valorant Store Watcher  👀 

Python script useful to check locally your valorant store. It uses the vaorant API
> As for now 2FA auth is not supported :(

### 🍕 Features:
1) Check **Valorant Points**
2) Check your **Radianite Points**
3) Check your **daily valorant shop**
4) Check **bundles**
5) Beautiful **GUI**

### ✍🏼 TODO:
- 2FA auth support
- multiple account support
- add alerts to favourite skins
- cross platform support

### 🌊 Visuals
<img width="1070" alt="Screenshot 2022-09-20 at 18 37 12" src="https://user-images.githubusercontent.com/81587335/191315227-241c5d38-4480-4723-964e-883ccce46176.png">
<img width="811" alt="GUIValoStoreWatcher" src="https://user-images.githubusercontent.com/81587335/191372428-c2ce5818-ebde-479e-be8b-7b952d8ffcea.png">

https://user-images.githubusercontent.com/81587335/191369188-0b056792-1445-450a-9859-31d8c6ac3fc1.mp4





### 📃 How to use:
- Install [this](https://www.dafont.com/valorant.font) font
- Install the dependencies
```python
pip install requests
pip install ssl
pip install urllib3
pip install collections
pip install configparser
pip install re
pip install rich
```
- Insert your riot credentials and your region (eu/na/...) in `config.ini` where there are the xxx
- Run `py valostorewatcher.py` or `python3 valostorewatcher.py` to check ur store without the gui
- Run `py valostorewatcher.py -gui` or `python3 valostorewatcher.py -gui` to check ur store with the gui

### Contriutions
Everything is welcomed :) If u want to add something feel free to do it and make a pull request ;)
