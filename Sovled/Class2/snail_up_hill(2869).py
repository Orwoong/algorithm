# 정상에서는 미끄러지지 않는다!
# 올라가야 할 거리 = destination - down(올라가는 거리 > 내려가는 거리이기 때문에 정상에서는 미끄러지지 않기 때문에)
# 하루에 올라갈 수 있는 거리 = up - down

import math
up, down, destination = map(int, input().split())

day = (destination-down) / (up- down)
# 나머지가 0으로 떨어지게 되면 낮에 정상에 도착하게 되며
# 나머지가 0이 아닌 경우는 미끄러짐
print(math.ceil(day))