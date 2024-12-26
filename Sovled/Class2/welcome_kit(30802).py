participant_count = int(input())
clothes_size_list = map(int, input().split())
clothes_bundle_count, pen_bundle_count = map(int, input().split())

order_clothes_bundle_count = 0

for clothes in clothes_size_list:
    order_clothes_bundle_count += clothes // clothes_bundle_count
    if clothes % clothes_bundle_count > 0:
        order_clothes_bundle_count += 1

order_pen_bundle_count = participant_count // pen_bundle_count
order_pen_rest_count = participant_count % pen_bundle_count

print(order_clothes_bundle_count)
print(order_pen_bundle_count, order_pen_rest_count)