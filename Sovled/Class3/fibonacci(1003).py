N = int(input())
fibonacci_list = [(1, 0), (0, 1)]

for i in range(39):
    zero_value = fibonacci_list[i][0] + fibonacci_list[i][1]
    one_value = fibonacci_list[i + 1][0] + fibonacci_list[i + 1][1]

    fibonacci_list.append((zero_value, one_value))

for i in range(N):
    index = int(input())
    first = fibonacci_list[index][0]
    second = fibonacci_list[index][1]
    print(first, second)