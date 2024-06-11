# Program Analysis Basis 2
import random
x = random.randrange(1, 10) # 1 is inclusive and 10 is exclusive
result = "yes"
if x < 5:
    result = "no"
if x == 10:
    result = "may be"

print(result)

# Over approximation: "yes", "no" and "may be"
# consider all paths( that are feasible based on limited knowledge 
# about randrange() method)
# Under approximation: "yes" (Execute once)
#  Sound and complete: "yes" , "no" (only two feasible paths)