import requests
import eel
import speedtest

eel.init('Web')

eel.start('main.html', size=(800, 500))


def get_info():
    f = open('info.json', 'w')
    # Код

    f.close()
