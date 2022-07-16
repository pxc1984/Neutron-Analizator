import psutil


def connections():
    cons = [connection[5] for connection in (psutil.net_connections())]
    nons = cons.count('NONE')
    establisheds = cons.count('ESTABLISHED')
    listens = cons.count('LISTEN')
    time_waits = cons.count('TIME_WAIT')
    return nons, establisheds, listens, time_waits
