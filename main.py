import requests
import json
import eel
import socket
import speedtest
import datetime
import geocoder
import folium
import threading
import time
from collections import deque
import psutil


def calc_ul_dl(rate, dt=3, interface="Беспроводная сеть"):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        last_tot = tot
        time.sleep(dt)
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [
            (now - last) / (t1 - t0) / 1024.0
            for now, last in zip(tot, last_tot)
        ]
        rate.append((ul, dl))
        t0 = time.time()


def print_rate(rate):
    try:
        return "Upload Speed: {0:.0f} kB/s / Download Speed: {1:.0f} kB/s".format(*rate[-1])
    except IndexError:
        return "UL: - kB/s/ DL: - kB/s"


def return_rate(rate):
    try:
        return rate[-1]
    except IndexError:
        return [0, 0]


def connections():
    cons = [connection[5] for connection in (psutil.net_connections())]
    nons = cons.count('NONE')
    establisheds = cons.count('ESTABLISHED')
    listens = cons.count('LISTEN')
    time_waits = cons.count('TIME_WAIT')
    traffic = {
        'None': 'None: ' + str(nons),
        'Established': 'Established: ' + str(establisheds),
        'Listen': 'Listen: ' + str(listens),
        'Time_Wait': 'Time_Wait: ' + str(time_waits)
    }
    return traffic


def get_map():
    ip = geocoder.ip("me")
    location = ip.latlng
    m = folium.Map(location=location, zoom_start=10)
    folium.Marker(location).add_to(m)
    m.save("Web/map.html")
    return ip


info = []


def get_info(transferrate):
    dt = datetime.datetime.now()
    data = {}
    # data["ip"] = socket.gethostbyname("me")
    data["ip"] = '0'
    data['i'] = dt.second
    data["proxy"] = ''
    data["speed"] = print_rate(transferrate)
    u, d = return_rate(transfer_rate)
    if len(info) > 60:
        info.pop(0)
    info.append({
        "tm": dt.hour * 3600 + dt.minute * 60 + dt.second,
        "up": float('{:.1f}'.format(u)),
        "dn": float('{:.1f}'.format(d))
    })
    data["information"] = info
    data["time"] = f'{dt.hour}:{dt.minute}:{dt.second}'
    data["traffic"] = connections()
    with open('Web/info.json', 'r+') as f:
        json.dump(data, f)
        f.truncate()


get_map()
# eel.init('Web')
# eel.start('main.html', size=(800, 500))
transfer_rate = deque(maxlen=1)
t = threading.Thread(target=calc_ul_dl, args=(transfer_rate,))
t.daemon = True
t.start()
run = True
while run:
    print(return_rate(transfer_rate))
    get_info(transfer_rate)
    time.sleep(1)
