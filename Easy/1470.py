#Leetcode
#1470. Shuffle the Array

def shuffle_first(nums: [int], n: int) -> [int]:
    first_nums_list = nums[0:n]
    last_nums_list = nums[n:len(nums)]

    result = []
    for i in range(n):
        result.append(first_nums_list[i])
        result.append(last_nums_list[i])

    return result

print(shuffle_first([1,2,3,4,4,3,2,1], 4))

def shuffle_final(nums: [int], n: int) -> [int]:
    result = []
    for i in range(n):
        result.append(nums[i])
        result.append(nums[n + i])

    return result

print(shuffle_final([1,2,3,4,4,3,2,1], 4))

