import psutil
import time

initial = set(psutil.net_connections(kind='tcp'))
while True:
    time.sleep(1)
    current = set(psutil.net_connections(kind='tcp'))
    print(current.difference(initial))
