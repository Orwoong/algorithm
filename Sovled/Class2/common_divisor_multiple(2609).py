first, second = map(int, input().split())

def gcd(a, b):
    for i in range(min(first, second), 0, -1):
        if first % i == 0 and second % i == 0:
            return i
    return 0

def lcm(a, b):
    for i in range(max(first, second), (first * second) + 1):
        if i % first == 0 and i % second == 0:
            return i
    return 0

print(gcd(first, second))
print(lcm(first, second))