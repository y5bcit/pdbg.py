def function_one(a):
	for i in range(3):
		a += 1
	return a

def function_two(b):
	for i in range(3):
		b += 1
	return b

c = function_one(1)
d = function_two(2)
print(c)
print(d)

