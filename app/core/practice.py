def bisection_root(x):
    epsilon = 0.01
    low = 0
    high = x
    ans = (high + low) /2.0
    while abs(ans**2 - x) >= epsilon:
        if ans**2 < x:
            low = ans
        else:
            high = ans
        ans = (high + low) /2.0

    return ans

def sqrt_num_counter(n, epsilon):
    count = 0

    for i in range(n**3):
        sqrt = bisection_root(i)
        if abs(n-sqrt) < epsilon:
            print(i, sqrt)
            count += 1
    return count

print(sqrt_num_counter(10, 0.1))

