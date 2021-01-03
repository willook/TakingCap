import random
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

n_data = 1000
n_wall = 7

# random data gen
X_origin = np.zeros((n_data, 8))

for j in range(8):
    X_origin[0,j] = random.randint(0,n_wall-1)

for i in range(1,n_data):
    for j in range(0,8,2):
        det = random.random()
        #move = [0, 0]
        if det < 0.25:
            X_origin[i, j] = min(X_origin[i - 1, j] + 1, n_wall - 1)
            X_origin[i, j+1] = X_origin[i-1, j+1]
        elif det < 0.5:
            X_origin[i, j] = max(X_origin[i - 1, j] - 1, 0)
            X_origin[i, j + 1] = X_origin[i - 1, j + 1]
        elif det < 0.75:
            X_origin[i, j] = X_origin[i - 1, j]
            X_origin[i, j+1] = min(X_origin[i - 1, j+1] + 1, n_wall - 1)
        else:
            X_origin[i, j] = X_origin[i - 1, j]
            X_origin[i, j+1] = max(X_origin[i - 1, j+1] - 1, 0)

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
    # 리더 정답
    i_diff = X_origin[i, 0] - X_origin[i, 6]
    j_diff = X_origin[i, 1] - X_origin[i, 7]
    if X_origin[i, 0]!=0 and X_origin[i, 0]!=n_wall-1 and abs(i_diff) > abs(j_diff):
        if i_diff < 0:
            y[i, 0] = 0  # up
        else:
            y[i, 0] = 2  # down
    else:
        if j_diff < 0:
            y[i, 0] = 1  # right
        else:
            y[i, 0] = 3  # left

    # 팀원 정답
    i_diff = X_origin[i, 2] - X_origin[i, 4]
    j_diff = X_origin[i, 3] - X_origin[i, 5]
    if X_origin[i, 0]!=0 and X_origin[i, 0]!=n_wall-1 and abs(i_diff) > abs(j_diff):
        if i_diff > 0:
            y[i, 1] = 0 # up
        else:
            y[i, 1] = 2 # down
    else:
        if j_diff > 0:
            y[i, 1] = 1 # right
        else:
            y[i, 1] = 3 # left

# dataset 저장
dataset = np.hstack((X_obs,y))
df = pd.DataFrame(dataset, columns = ['a2_i', 'a2_j', 'a1_i', 'a1_j',
                                    'b2_i', 'b2_j', 'b1_i', 'b1_j', 'y1', 'y2'])
df.to_csv("data\\data7x7_1000.csv")


