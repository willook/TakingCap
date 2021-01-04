import time
import numpy as np
def update_leader(i_diff, j_diff):
    y_cand = np.ones(4)
    i_move = i_diff
    j_move = j_diff
    if abs(i_move) > abs(j_move):
        i_move = (i_move / abs(i_move) * 2) if i_move !=0 else 0
        j_move = (j_move / abs(j_move) * 1) if j_move !=0 else 0
    elif abs(i_move) < abs(j_move):
        i_move = (i_move / abs(i_move) * 1) if i_move !=0 else 0
        j_move = (j_move / abs(j_move) * 2) if j_move !=0 else 0
    else:
        i_move = (i_move / abs(i_move) * 1) if i_move !=0 else 0
        j_move = (j_move / abs(j_move) * 1) if j_move !=0 else 0
    if i_move > 0:
        y_cand[2] += i_move
    if i_move < 0:
        y_cand[0] += abs(i_move)
    if i_move == 0:
        y_cand[[0,2]] += 1
    if j_move > 0:
        y_cand[1] += j_move
    if j_move < 0:
        y_cand[3] += abs(j_move)
    if j_move == 0:
        y_cand[[1, 3]] += 1
    return y_cand

def update_member(i_diff, j_diff):
    y_cand = np.ones(4)
    i_move = i_diff
    j_move = j_diff
    if abs(i_move) > abs(j_move):
        i_move = (i_move / abs(i_move) * 2) if i_move != 0 else 0
        j_move = (j_move / abs(j_move) * 1) if j_move != 0 else 0
    elif abs(i_move) < abs(j_move):
        i_move = (i_move / abs(i_move) * 1) if i_move != 0 else 0
        j_move = (j_move / abs(j_move) * 2) if j_move != 0 else 0
    else:
        i_move = (i_move / abs(i_move) * 1) if i_move != 0 else 0
        j_move = (j_move / abs(j_move) * 1) if j_move != 0 else 0

    if i_move > 0:
        y_cand[0] += i_move
    if i_move < 0:
        y_cand[2] += abs(i_move)
    if i_move == 0:
        y_cand[[0, 2]] += 1
    if j_move > 0:
        y_cand[3] += j_move
    if j_move < 0:
        y_cand[1] += abs(j_move)
    if j_move == 0:
        y_cand[[1, 3]] += 1
    return y_cand

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