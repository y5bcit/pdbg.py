def function1(a):
    if a > 0:
        return a + function1(a - 1)
    else:
        return 0

print(function1(5))
