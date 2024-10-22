# 레이저는 여는 괄호와 닫는 괄호의 인접한 쌍 ‘( ) ’ 으로 표현된다. 또한, 모든 ‘( ) ’는 반드시 레이저를 표현한다.
# 쇠막대기의 왼쪽 끝은 여는 괄호 ‘ ( ’ 로, 오른쪽 끝은 닫힌 괄호 ‘) ’ 로 표현된다.

# 쇠 막대기가 어떻게 구성되는지 알아야 함
# 쇠 막대기의 시작과 끝점을 알아야 할까?

iron_list = input()

def iron_stick(list):
    stack = []
    result = 0

    for i in range(len(list)):
        if list[i] == '(':
            stack.append(i)
        else:
            last = stack.pop()
            if list[i-1] == '(':
                result += len(stack)
            else:
                result += 1

    return result

print(iron_stick(iron_list))


# 문제 파악이 제일 중요한데 패턴이 어떻게 되는지와 주어진 문제의 조건들을 유심히 살펴 볼 것
# 주어진 그림을 파악해보는 것도 중요하며 너무 어렵게 생각하지 말기