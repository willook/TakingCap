### todo  
(완) solider를 leader와 member로 분리할 것 -> level로 구분하기로 함  
(완) member는 leader로 부터 command를 받도록 할 것  
(완) map은 요청자의 관측 결과를 송출 할 수 있도록 할 것  
(완) map.py에 flask 추가하고 b2, r2에 대한 요청 응답 작성  
(완) map.py 에서 게임 종료 조건 작성 및 적용  
(완) 한칸에 여러명 들어올수 있게 수정  
(완) 랜덤 데이터 생성  
(완) train test 코드 작성 측정  
(완) 모델 적용  
(완) data imputer 이전 데이터 저장으로 바꿔보기  
생성, 예측 시, data jitter 추가해보기  
예측 결과를 입력으로 생존 모델 추가해보기

### settings  
map 초기화 속도 1 fps  
병사들 이동 속도 0.5 fps  
맵 크기 7 x 7  
패킷 타임아웃 10ms  1ms에서 타임아웃남

### packet  
map->level2  
ex) map, b2, 2, 3, r1, 3, 1 # 직선 상 병사 위치, 본인 위치 포함하여 제공  
level2->level1  
ex) level2, b1, 0, -1 # 이동 방향, 수신사를 포함하여 제공  

### command  
cd C:\Users\jongwhoa\Desktop\projects\TakingCap  
conda activate py37base  
python map.py --n 7 --test True  

python soldier.py -p 11101 -t blue -l 2 -n 7 -r http://127.0.0.1:11100/  
python soldier.py -p 11102 -t blue -l 1 -n 7 -r http://127.0.0.1:11101/  
python soldier.py -p 11103 -t red  -l 2 -n 7 -r http://127.0.0.1:11100/  
python soldier.py -p 11104 -t red  -l 1 -n 7 -r http://127.0.0.1:11103/  

### result
setting: dataset, data7x7_300000.csv, model, randomforest10, save_data, True  
leader acc:  
&nbsp;&nbsp;* train: 96.86666666666667  
&nbsp;&nbsp;* test : 80.66666666666666  
team   acc:  
&nbsp;&nbsp;* train: 93.30000000000001  
&nbsp;&nbsp;* test : 62.980000000000004  
leader는 team이 근처에 오면 관측 가능하나 team은 leader를 관측하기 어려워 정확도가 낮은 것 같음  

### 논점
1. 상급자가 명령을 내렸으나 하급자가 명령을 못받았을 수 있음  
2. 상급자가 하급자의 위치를 정확하기 파악하기 어려움, 하급자는 gps가 없고, 얼마나 이동했는지 알기 어려움  
3. 하급자가 명령을 수행해도 상급자가 얼마나 명령을 수행했는지 상시 파악하기 어려움  
4. 예로 상급자가 하급자와 동시에 이동하기 위해 한칸 이동하라 했을 때, 
   하급자가 느리면 상급자는 다음 차례에 관측 시 하급자가 아직 안보일 수 있음  
5. 정보량이 매번 다른데 어떻게 처리했는지  
