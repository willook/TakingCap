from flask import Flask
import argparse
import cv2
import threading
import random
import threading
from utils import Timer

vid = cv2.VideoCapture("templates\\04_gray.avi")
outputFrame80 = None
lock = threading.Lock()

class Soldier(threading.Thread):
    def __init__(self, id, team_name, position, n_wall, fps=2):
        threading.Thread.__init__(self)
        self.id = id
        self.team_name = team_name
        self.position = position
        self.n_wall = n_wall
        self.point = [random.randint(0,n_wall-1), random.randint(0,n_wall-1)]
        self.timer = Timer(fps)

    def step(self):
        self.point = [random.randint(0, self.n_wall-1), random.randint(0, self.n_wall-1)]

    def observe(self):
        return None

    def run(self):
        while True:
            self.timer.wait()
            observation = self.observe()
            self.step()

def main(args):
    app = Flask(__name__)

    soldier = Soldier(id=0,team_name=args.team_name,position=args.position, n_wall=5)
    soldier.daemon = True
    soldier.start()

    @app.route("/")
    def index():
        # return the response generated along with the specific media
        # type (mime type)
        return soldier.team_name[0] + soldier.position[0] + " " + " ".join([str(x) for x in soldier.point])

    # start the flask app
    app.run(host=args.ip, port=args.port, debug=True, threaded=True, use_reloader=False)


if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                    help="ip address of the device")
    parser.add_argument("-o", "--port", type=int, default="8101",
                    help="ephemeral port number of the server (1024 to 65535)")
    parser.add_argument("-t", "--team_name", type=str, help="blue or red")
    parser.add_argument("-p", "--position", type=str, help="leader or member")


    args = parser.parse_args()
    main(args)