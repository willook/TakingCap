import threading
import requests

from utils import Timer

# soldier's port is 11101, 11102, 11103, 11104
# map's port is 11100

class HtmlGetter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.timer = Timer(5)

    def run(self):
        while True:
            for id in range(11101,11105):
                self.timer.wait()
                try:
                    url = 'http://127.0.0.1:'+str(id)+'/'
                    resp = requests.get(url, timeout=0.001)
                    print(url, resp.text)

                except Exception as e:
                    print(url, None)



t = HtmlGetter()
t.daemon = True
t.start()
input("")
print("### End ###")