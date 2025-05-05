sequence = []
a,b = 0,1
for i in range(1, 100, 1):
    sequence.append(a)
    a,b = b, b + a
i += 1

print(sequence)
