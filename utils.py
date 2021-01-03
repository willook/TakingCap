import time

class Timer():
    def __init__(self, fps):
        self.start_time = 0
        self.end_time = 0
        self.fps = fps
        self.wait_time = 1/self.fps

    def set_fps(self, fps):
        self.fps = fps
        self.wait_time = 1/self.fps

    def wait(self):
        self.end_time = time.time()
        sleep_time = self.wait_time - (self.end_time - self.start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.start_time = time.time()

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')