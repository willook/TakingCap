import random
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from map import get_basic_map, put_map, show_map
from utils import update_leader, update_member
random.seed(0)
n_data = 300000
n_wall = 7

# random data gen
X_origin = np.zeros((n_data, 8), dtype=int)

for j in range(8):
    X_origin[0,j] = random.randint(0,n_wall-1)

for i in range(1,n_data):
    for j in range(0,8,2):
        det = random.random()
        #move = [0, 0]
        if det < 0.2:
            X_origin[i, j] = min(X_origin[i - 1, j] + 1, n_wall - 1)
            X_origin[i, j+1] = X_origin[i-1, j+1]
        elif det < 0.4:
            X_origin[i, j] = max(X_origin[i - 1, j] - 1, 0)
            X_origin[i, j + 1] = X_origin[i - 1, j + 1]
        elif det < 0.6:
            X_origin[i, j] = X_origin[i - 1, j]
            X_origin[i, j+1] = min(X_origin[i - 1, j+1] + 1, n_wall - 1)
        elif det < 0.8:
            X_origin[i, j] = X_origin[i - 1, j]
            X_origin[i, j + 1] = max(X_origin[i - 1, j + 1] - 1, 0)
        else:
            X_origin[i, j] = X_origin[i - 1, j]
            X_origin[i, j+1] = X_origin[i - 1, j+1]

# 관측 가능 정보 생성
X_obs = np.zeros((n_data, 8))
for i in range(n_data):
    for j in range(0,8,2):
        if X_origin[i,0] == X_origin[i,j] or X_origin[i,1] == X_origin[i,j+1]:
            X_obs[i, j] = X_origin[i, j]
            X_obs[i, j+1] = X_origin[i, j+1]
        else:
            X_obs[i, j] = np.nan
            X_obs[i, j+1] = np.nan

# 정답 데이터 생성
y = np.zeros((n_data, 2))
for i in range(n_data):

    # 리더 정답 후보, 모두 가능
    i_diff = X_origin[i, 0] - X_origin[i, 6]
    j_diff = X_origin[i, 1] - X_origin[i, 7]
    y_cand = update_leader(i_diff, j_diff)
    if X_origin[i, 0] == 0:
        y_cand[0] = 0
    if X_origin[i, 0] == n_wall - 1:
        y_cand[2] = 0
    if X_origin[i, 1] == n_wall - 1:
        y_cand[1] = 0
    if X_origin[i, 1] == 0:
        y_cand[3] = 0
    y[i, 0] = np.argmax(y_cand)

    # 팀원 정답 후보, 모두 가능
    i_diff = X_origin[i, 2] - X_origin[i, 4]
    j_diff = X_origin[i, 3] - X_origin[i, 5]
    y_cand = update_member(i_diff, j_diff)
    if X_origin[i, 2] == 0:
        y_cand[0] = 0
    if X_origin[i, 2] == n_wall - 1:
        y_cand[2] = 0
    if X_origin[i, 3] == n_wall - 1:
        y_cand[1] = 0
    if X_origin[i, 3] == 0:
        y_cand[3] = 0
    y[i, 1] = np.argmax(y_cand)
    '''
    basic_map = get_basic_map(7)
    basic_map = put_map(basic_map, 'r2', X_origin[i,0:2])
    basic_map = put_map(basic_map, 'r1', X_origin[i,2:4])
    basic_map = put_map(basic_map, 'b2', X_origin[i,4:6])
    basic_map = put_map(basic_map, 'b1', X_origin[i,6:8])
    show_map(basic_map)
    '''
# dataset 저장
dataset = np.hstack((X_obs,y))
dataset_origin = np.hstack((X_origin,y))

df = pd.DataFrame(dataset, columns = ['a2_i', 'a2_j', 'a1_i', 'a1_j',
                                    'b2_i', 'b2_j', 'b1_i', 'b1_j', 'y1', 'y2'])

df_origin = pd.DataFrame(dataset_origin, columns = ['a2_i', 'a2_j', 'a1_i', 'a1_j',
                                    'b2_i', 'b2_j', 'b1_i', 'b1_j', 'y1', 'y2'])

df.to_csv("data\\data7x7_"+str(n_data)+".csv")
df_origin.to_csv("data\\data7x7_"+str(n_data)+"_origin.csv")



