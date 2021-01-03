import threading
import requests
import os
from flask import Flask
import logging
import argparse

from utils import Timer, str2bool

# turn off flask verbos
log = logging.getLogger('werkzeug')
log.disabled = True

# soldier's port is 11101, 11102, 11103, 11104
# map's port is 11100
ip2name = {101:'b2',
           102:'b1',
           103:'r2',
           104:'r1',
           }
points = {}

class Sender(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

    def get_info(self, name1):
        if not name1 in points:
            return ""
        point1 = points[name1]
        info = ["map"]
        for name2, point2 in points.items():
            #if name1 == name2:
            #    continue
            if point1[0] != point2[0] and point1[1] != point2[1]:
                continue
            info.extend([name2, str(point2[0]), str(point2[1])])
        return " ".join(info)

    def run(self):
        global points
        app = Flask(__name__)

        @app.route("/b2")
        def b2():
            return self.get_info('b2')

        @app.route("/r2")
        def r2():
            return self.get_info('r2')

        app.run(host=self.ip, port=self.port, debug=False, threaded=True, use_reloader=False)


class Map(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.timer = Timer(5)

    def run(self):
        global points
        while True:
            for id in range(11101,11105):
                self.timer.wait()
                try:
                    url = 'http://127.0.0.1:'+str(id)+'/'
                    resp = requests.get(url, timeout=0.001)
                    #print(url, resp.text)
                    name, i, j = resp.text.split()
                    points[name] = [int(i), int(j)]
                except Exception as e:
                    pass
                    #print(url, None)

def get_basic_map(n_map):
    row1 = [' '] + ['-'] * (n_map * 8 - 1)
    #row1.append('\n')
    #row1 = ''.join(row1)
    row2 = ['|', '\t'] * (n_map+1)
    #row2.append('\n')
    #row2 = ''.join(row2)
    basic_map = [row1]
    for _ in range(n_map):
        basic_map.append(row2.copy())
        basic_map.append(row2.copy())
        basic_map.append(row1.copy())

    #basic_map = [row1] + [row2, row2, row1] * (n_map)
    #print("".join(basic_map))
    return basic_map

def put_map(basic_map, name, point):
    i, j = point
    mi = 1+3*i
    mj = 1+2*j
    print(basic_map[mi][mj],len(basic_map[mi][mj]))
    if len(basic_map[mi][mj]) > 5:
        mi += 1
    basic_map[mi][mj] = basic_map[mi][mj].strip('\t') + name + ' \t'
    return basic_map

def show_map(basic_map):
    os.system("cls")
    for row in basic_map:
        print("".join(row))

def is_done(points):
    if 'r1' in points and 'b2' in points and points['r1'] == points['b2']:
        return True
    if 'b1' in points and 'r2' in points and points['b1'] == points['r2']:
        return True
    return False

def show(n_wall, test):
    global points
    timer = Timer(fps=1)
    while True:
        timer.wait()
        basic_map = get_basic_map(n_wall)
        for name, point in points.items():
            basic_map = put_map(basic_map, name, point)
        show_map(basic_map)
        if not test and is_done(points):
            break
    print("done.")

def main(args):
    map = Map()
    map.daemon = True
    map.start()

    sender = Sender(ip=args.ip, port=args.port)
    sender.daemon = True
    sender.start()

    show(args.n_wall, args.test)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                        help="ip address of the device")
    parser.add_argument("-p", "--port", type=int, default="11100",
                        help="ephemeral port number of the server (1024 to 65535)")
    parser.add_argument("-n", "--n_wall", type=int, default=7, help="number of wall")
    parser.add_argument("-t", "--test", type=str2bool, default=False, help="test mode")

    args = parser.parse_args()
    main(args)