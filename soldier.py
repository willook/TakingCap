from flask import Flask
import argparse
import cv2
import random
import threading
import requests
import logging
import pandas as pd
import numpy as np

from utils import Timer
from model import make_model
# turn off flask verbos
log = logging.getLogger('werkzeug')
log.disabled = True

vid = cv2.VideoCapture("templates\\04_gray.avi")
outputFrame80 = None
lock = threading.Lock()

class Soldier(threading.Thread):
    def __init__(self, id, team_name, level, n_wall, recv_url, fps=0.5):
        threading.Thread.__init__(self)
        self.team_name = team_name
        self.level = level
        self.n_wall = n_wall
        self.recv_url = recv_url
        self.point = [random.randint(0,n_wall-1), random.randint(0,n_wall-1)]
        self.timer = Timer(fps)
        self.name = self.team_name[0] + str(self.level)
        #self.info = [] # 처음에 없으면 에러날 수 있음
        self.map_data = np.full((1,8), np.nan)

        self.num2move = {0: [-1, 0], #up
                         1: [0, 1],  #right
                         2: [1, 0],  #down
                         3: [0, -1],}#left
        if self.level == 2:
            df = pd.read_csv("data\\data7x7_1000.csv")
            dataset = df.to_numpy()[:, 1:]
            n_data = len(dataset)
            X = dataset[:, :-2]
            # print(X[:10])
            y1 = dataset[:, -2]
            y2 = dataset[:, -1]
            self.imp1, self.clf1 = make_model(X, y1)
            self.imp2, self.clf2 = make_model(X, y2)

    def random_step(self):
        det = random.random()
        move = [0,0]
        if det < 0.25:
            move[0] = 1
        elif det < 0.5:
            move[0] = -1
        elif det < 0.75:
            move[1] = 1
        else:
            move[1] = -1
        return move

    def step(self):
        if self.level == 1:
            move = [int(self.info[-2]), int(self.info[-1])]
        if self.level == 2:
            next_step = self.clf1.predict(self.imp1.transform(self.map_data))[0]
            move = self.num2move[next_step]

        if self.point[0] + move[0] >= 0 and self.point[0] + move[0] < self.n_wall:
            self.point[0] += move[0]
        if self.point[1] + move[1] >= 0 and self.point[1] + move[1] < self.n_wall:
            self.point[1] += move[1]

    def observe(self):
        if self.level == 1:
            try:
                # level 2로 부터 명령을 요청함
                resp = requests.get(self.recv_url + "level2", timeout=0.001)
                self.info = resp.text.split()
            except Exception as e:
                # 명령이 없음, 대기
                self.info = ["level2", self.name, "0", "0"]
            #return ""
        if self.level == 2:
            try:
                # 맵으로 부터 자기 이름의 객체가 알수 있는 정보를 요청함
                resp = requests.get(self.recv_url + self.name, timeout=0.001)
                self.info = resp.text.split()
            except Exception as e:
                # 맵으로 관측을 실패하더라도 gps는 있으므로 자기 위치는 알 수 있음
                self.info = ['map', self.name, str(self.point[0]), str(self.point[1])]

            # info를 통해 map_data 갱신, level 2만 필요
            for i in range(1,len(self.info), 3):
                name = self.info[i]
                ci = self.info[i+1]
                cj = self.info[i+2]
                if name == self.name:
                    self.map_data[0,0] = ci
                    self.map_data[0,1] = cj
                elif name[0] == self.name[0]:
                    self.map_data[0,2] = ci
                    self.map_data[0,3] = cj
                elif name[-1] == "2":
                    self.map_data[0,4] = ci
                    self.map_data[0,5] = cj
                else:
                    self.map_data[0,6] = ci
                    self.map_data[0,7] = cj

        print(self.name, "info:",self.info)


    def run(self):
        while True:
            self.timer.wait()
            self.observe()
            self.step()

def main(args):

    # soldier run
    soldier = Soldier(id=0,team_name=args.team_name,level=args.level,
                      n_wall=args.n_wall, recv_url=args.recv_url)
    soldier.daemon = True
    soldier.start()

    # solider's sender
    app = Flask(__name__)
    @app.route("/")
    def index():
        # return the response generated along with the specific media
        # type (mime type)
        return soldier.name + " " + " ".join([str(x) for x in soldier.point])

    @app.route("/level2")
    def level2():
        if soldier.level != 2:
            return ""

        next_step = soldier.clf2.predict(soldier.imp2.transform(soldier.map_data))[0]
        move = soldier.num2move[next_step]
        return " ".join(["level2", soldier.team_name[0]+"1", str(move[0]), str(move[1])])

    # start the flask app
    app.run(host=args.ip, port=args.port, debug=False, threaded=True, use_reloader=False)


if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                    help="ip address of the device")
    parser.add_argument("-r", "--recv_url", type=str, default="http://127.0.0.1:11100/",
                    help="ip to request to get information")
    parser.add_argument("-p", "--port", type=int, default="8101",
                    help="ephemeral port number of the server (1024 to 65535)")
    parser.add_argument("-t", "--team_name", type=str, help="blue or red")
    parser.add_argument("-l", "--level", type=int, help="2(leader) or 1(member)")
    parser.add_argument("-n", "--n_wall", type=int, default=5,help="number of wall")

    args = parser.parse_args()
    main(args)