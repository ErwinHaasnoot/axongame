a = range(5)
b = range(6,10)

print [(i,j) for i in a for j in b if j == 6]
