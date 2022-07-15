import requests
import eel
import json
import socket
import speedtest
import datetime
import geocoder

eel.init('Web')
eel.start('main.html', size=(800, 500))


def spt(option):
    st = speedtest.Speedtest()
    if option == 1:
        return round(st.download() / (2**20), 1)
    elif option == 2:
        return round(st.upload() / (2**20), 1)
    elif option == 3:
        servernames = []
        st.get_servers(servernames)
        return st.results.ping


def get_info():
    dt = datetime.time()
    with open('data.json', 'r+') as f:
        data = json.load(f)
        data["ip"] = socket.gethostname()
        data["proxy"] = '0'
        data["speed_up"] = spt(2)
        data["speed_down"] = spt(1)
        data["time"] = dt
        data["traffic"] = ['TCP', '192.168.198.72:50419', 'LAPTOP-AG9AGC10:65180', 'TIME_WAIT']
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part
