def get_slope_and_intercept(x, y):
    sum_x = 0
    sum_y = 0
    sum_x_squared = 0
    sum_xy = 0

    n = len(x)
    for i in range(n):
        x_val = x[i]
        y_val = y[i]

        sum_x += x_val
        sum_x_squared += pow(x_val, 2)
        sum_xy += x_val * y_val
        sum_y += y_val

    # y = mx + b
    denominator  =  ((n * sum_x_squared) - pow(sum_x, 2))
    if denominator == 0:
        return 0, 0

    m = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x_squared) - pow(sum_x, 2))
    b = (sum_y - (m * sum_x)) / n
    return m, b