from flask import Response
from flask import Flask
from flask import render_template
import argparse
import cv2
import threading

from utils import Timer

app = Flask(__name__)
vid = cv2.VideoCapture("templates\\04_gray.avi")
outputFrame80 = None
lock = threading.Lock()

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def make_frame_bytes():
    # grab global references to the video stream, output frame, and
    # lock variables
    global vid, outputFrame80, lock
    lock = threading.Lock()
    timer = Timer(15)

    # loop over frames from the video stream
    while True:
        # gray80 = tw.get_stream()
        ret, gray80 = vid.read()

        if not ret:
            vid = cv2.VideoCapture("templates\\04_gray.avi")
            continue
        timer.wait()
        gray80 = cv2.resize(gray80, (80, 60), interpolation=cv2.INTER_CUBIC)
        if gray80.shape[-1] == 3:
            gray80 = cv2.cvtColor(gray80, cv2.COLOR_BGR2GRAY)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame80 = gray80.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame80, lock
    timer = Timer(15)
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            outputFrame = outputFrame80
            if outputFrame is None:
                continue

            # encode the frame in jpeg format
            (flag, encodedImage) = cv2.imencode(".jpeg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        frame = bytearray(encodedImage)
        timer.wait()
        print("len(frame)", len(frame))
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n'
               b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
               b'\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/coordinate")
def coordinate():
	# return the response generated along with the specific media
	# type (mime type)
	return 'Hello, World!'


if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser .add_argument("-i", "--ip", type=str, default="127.0.0.1",
                    help="ip address of the device")
    parser .add_argument("-o", "--port", type=int, default="8002",
                    help="ephemeral port number of the server (1024 to 65535)")
    parser .add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = parser.parse_args()

    # start a thread that will perform motion detection
    t = threading.Thread(target=make_frame_bytes, args=())
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args.ip, port=args.port, debug=True, threaded=True, use_reloader=False)