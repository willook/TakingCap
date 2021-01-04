[todo]
생성, 예측 시, data jitter 추가해보기

[settings]
map 초기화 속도 1 fps
병사들 이동 속도 0.5 fps
맵 크기 7 x 7

[packet]
map->level2
ex) map, b2, 2, 3, r1, 3, 1 # 직선 상 병사 위치, 본인 위치 포함하여 제공
level2->level1
ex) level2, b1, 0, -1 # 이동 방향, 수신사를 포함하여 제공


[command]
cd C:\Users\jongwhoa\Desktop\projects\TakingCap
conda activate py37base
python map.py --n 7 --test True

# 옵션에서 leader member는 뺄수 있게 할 것
python soldier.py -p 11101 -t blue -l 2 -n 7 -r http://127.0.0.1:11100/
python soldier.py -p 11102 -t blue -l 1 -n 7 -r http://127.0.0.1:11101/
python soldier.py -p 11103 -t red  -l 2 -n 7 -r http://127.0.0.1:11100/
python soldier.py -p 11104 -t red  -l 1 -n 7 -r http://127.0.0.1:11103/

[result]
setting: dataset, data7x7_300000.csv, model, randomforest10, save_data, True
leader acc:
  train: 96.86666666666667
  test : 80.66666666666666
team   acc:
  train: 93.30000000000001
  test : 62.980000000000004

[논점]
1. 상급자가 명령을 내렸으나 하급자가 명령을 못받았을 수 있음
2. 상급자가 하급자의 위치를 정확하기 파악하기 어려움, 하급자는 gps가 없고, 얼마나 이동했는지 알기 어려움
3. 하급자가 명령을 수행해도 상급자가 얼마나 명령을 수행했는지 상시 파악하기 어려움
4. 예로 상급자가 하급자와 동시에 이동하기 위해 한칸 이동하라 했을 때, 
   하급자가 느리면 상급자는 다음 차례에 관측 시 하급자가 아직 안보일 수 있음
5. 정보량이 매번 다른데 어떻게 처리했는지


