have_card_count = int(input())
have_card = map(int, input().split())
number_card_count = int(input())
number_card = map(int, input().split())

dic_card = {}
result_have_card_count = []

for card in have_card:
    if card not in dic_card:
        dic_card[card] = 1
    else:
        dic_card[card] += 1

for card in number_card:
    if card not in dic_card:
        result_have_card_count.append(0)
    else:
        result_have_card_count.append(dic_card[card])

print(" ".join(map(str, result_have_card_count)))