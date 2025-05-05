input_1 = int(input('tell me your first number: '))
input_2 = int(input('tell me your second number: '))

print('menu')
print('1. add')
print('2. subtract')

i = int(input('your selection menu: '))

while i <=3: 
    if i == 1:
        output = input_1 + input_2
        print(output)
    if i == 2:
        output = input_1 - input_2 
        print(output)
    i += 1
    
print('finish')