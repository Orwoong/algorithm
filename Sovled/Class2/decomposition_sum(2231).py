N = int(input())

result_list = []

for number in range(N-1, 0, -1):
    decomposition_number_list = list((map(int, str(number))))

    decomposition_number = number + sum(decomposition_number_list)
    if decomposition_number == N:
        result_list.append(number)

if not result_list:
    print(0)
else:
    print(min(result_list) if len(result_list) > 0 else result_list[0])