# 주어진 정수 배열에서 모든 가능한 순열을 생성하는 프로그램을 작성하세요.
# 배열에는 중복된 숫자가 없다고 가정합니다.

# 요구사항: 주어진 배열의 모든 숫자를 사용하여 만들 수 있는 모든 순열을 출력합니다.
# 백트래킹 알고리즘을 사용하여 효율적으로 모든 가능성을 탐색합니다.

# 예시 입력: [1, 2, 3]
# 예시 출력:
# [1, 2, 3]
# [1, 3, 2]
# [2, 1, 3]
# [2, 3, 1]
# [3, 1, 2]
# [3, 2, 1]

# [1, 2, 3, 4]
# [1, 2, 4, 3]
# [1, 3, 2, 4]
# [1, 3, 4, 2]
# [1, 4, 2, 3]
# [1, 4, 3, 2]

# [1, 2, 3, 4, 5]
# [1, 2, 3, 5, 4]
# [1, 2, 4, 3, 5]
# [1, 2, 4, 5, 3]
# [1, 3, 2, 4, 5]
# [1, 3, 2, 5, 4]

# [1, 3, 4, 2]
# [1, 4, 2, 3]
# [1, 4, 3, 2]

def permutation(arr, r):
    # 1.
    arr = sorted(arr)
    used = [0 for _ in range(len(arr))]

    def generate(result, visited):
        # 2.
        if len(result) == r:
            print(result)
            return

        # 3.
        for i in range(len(arr)):
            if not visited[i]:
                result.append(arr[i])
                visited[i] = 1
                generate(result, visited)
                visited[i] = 0
                result.pop()

    generate([], used)

print(permutation([1, 2, 3], 3))