N, M = map(int, input().split())
card_list = list(map(int, input().split()))

result = 0

for i in range(0, N):
    for j in range(i + 1, N):
        for k in range(j + 1, N):
            sum_card = card_list[i] + card_list[j] + card_list[k]
            if sum_card <= M and sum_card > result:
                result = sum_card

print(result)
