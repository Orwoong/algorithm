# 탐욕(그리디) 알고리즘을 통하여 구현 해보자
# 리스트에서 순서대로 회의 시간의 앞뒤를 구분하여 가장 많이 들어갈 수 있는 최대 값을 구해보자

list = [(0, 6), (1, 4), (3, 5), (3, 8), (5, 7), (8, 9)]
list1 = [(1, 3), (2, 4), (5, 8), (6, 10), (8, 11), (10, 12)]

def greedy_meeting(list):
    max_meeting = 0

    for i in range(len(list)):
        end = list[i][1]
        meeting_count = 1
        for j in range(i+1,len(list)):
            if list[j][0] >= end:
                meeting_count += 1
                end = list[j][1]
        max_meeting = max(max_meeting, meeting_count)

    return max_meeting

print(greedy_meeting(list))