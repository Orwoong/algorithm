from typing import List

def replaceElements(arr: List[int]) -> List[int]:
    if len(arr) == 0:
        return [-1]
    else:
        result = []
        i = 0
        while i < len(arr)-1:
            list = arr [ i+1: ]
            maximum_number = max(list)
            number_index = arr.index(maximum_number, i+1 , len(arr))
            print("Index %d" % number_index)
            for i in range(i, number_index):
                result.append(maximum_number)
            i = number_index
        result.append(-1)
        return result

print(replaceElements([17,18,5,4,6,1]))