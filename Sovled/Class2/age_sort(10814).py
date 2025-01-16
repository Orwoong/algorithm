N = int(input())
member_list = [[] for _ in range(201)]

for _ in range(N):
    age, name = input().split()
    member_list[int(age)].append(name)

for i in range(len(member_list)):
    for j in range(len(member_list[i])):
        print(i, member_list[i][j])


