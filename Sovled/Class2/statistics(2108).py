import sys
from decimal import Decimal, ROUND_HALF_UP

# Decimal(0.15 * N).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
N = int(input())

inputs = [int(sys.stdin.readline()) for _ in range(N)]

class Statistics:
    def __init__(self, inputs):
        self.inputs = inputs

    def arithmetic_mean(self):
        value = sum(self.inputs) / len(self.inputs)
        rounding = Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        if rounding == -0:
            rounding = 0

        return rounding

    def median_value(self):
        sorted_inputs = sorted(self.inputs)
        return sorted_inputs[len(sorted_inputs) // 2]

    def most_number_count(self):
        dict = {}
        for number in self.inputs:
            value = dict.get(number, 0)
            dict.update({number: value + 1})

        max_value = max(dict.items(), key=lambda item: item[1])
        list_with_max_value = [item for item in dict.items() if item[1] == max_value[1]]
        sorted_list = sorted(list_with_max_value, key=lambda item: item[0])

        if len(list_with_max_value) > 1:
            return sorted_list[1][0]
        else:
            return sorted_list[0][0]

    def gap_max_min(self):
        max_number = max(self.inputs)
        min_number = min(self.inputs)
        return max_number-min_number

statistics = Statistics(inputs)

print(statistics.arithmetic_mean())
print(statistics.median_value())
print(statistics.most_number_count())
print(statistics.gap_max_min())