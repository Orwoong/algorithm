import sys

N = int(input())
list = [set() for _ in range(51)]

for i in range(N):
    word = sys.stdin.readline().rstrip()
    word_len = len(word)
    list[word_len].add(word)

for i in range(len(list)):
    if len(list[i]) > 0:
        list[i] = sorted(list[i], reverse=True)
        for j in range(len(list[i])):
            print(list[i].pop())
