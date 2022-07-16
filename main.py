import requests
import eel
import json
import socket
import speedtest
import datetime
import geocoder
import folium
import psutil
# eel.init('Web')
# eel.start('main.html', size=(800, 500))


def connections():
    cons = [connection[5] for connection in (psutil.net_connections())]
    nons = cons.count('NONE')
    establisheds = cons.count('ESTABLISHED')
    listens = cons.count('LISTEN')
    time_waits = cons.count('TIME_WAIT')
    traffic = {
        'None': nons,
        'Established': establisheds,
        'Listen': listens,
        'Time_Wait': time_waits
    }
    return traffic


def get_new_speeds():
    speed_test = speedtest.Speedtest()
    speed_test.get_best_server()

    # Get ping (miliseconds)
    ping = speed_test.results.ping
    # Perform download and upload speed tests (bits per second)
    download = speed_test.download()
    upload = speed_test.upload()

    # Convert download and upload speeds to megabits per second
    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)

    return ping, download_mbs, upload_mbs


def get_map():
    ip = geocoder.ip("me")
    location = ip.latlng
    m = folium.Map(location=location, zoom_start=10)
    folium.CircleMarker(location=location, radius=50, color="red").add_to(m)
    folium.Marker(location).add_to(m)
    m.save("map.html")
    return ip


def get_info():
    dt = datetime.datetime.now()
    data = {}
    dt2 = {}
    data["ip"] = socket.gethostbyname(socket.gethostname())
    data["proxy"] = '1'
    data["ping"], data["speed_down"], data["speed_up"] = get_new_speeds()
    data["time"] = dt.hour*3600 + dt.minute*60 + dt.second
    data["traffic"] = connections()
    with open('info.json', 'r+') as f:
        json.dump(data, f)
        f.truncate()


get_info()
