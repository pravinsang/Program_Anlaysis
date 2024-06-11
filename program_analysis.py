# Program Analysis Basis 1
import random
x = random.randrange(1, 10)
result = x ** 2                 # result = x * x
print(result)

#OverApproximation: 1^2 to 10^2
#Under Approximation: 4
#Sound and complete : 1^2 to 9^2