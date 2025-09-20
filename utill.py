def print_mult_table(a, b):
    for i in range(a, b+1):
        for j in range(1, 13):
            if (i * j) % 2 == 0:
                print(f"{i} x {j} = {i*j}")


print_mult_table(5, 20)

students = [
    {'name': 'Mark', 'grade': 'A'},
    {'name': 'John', 'grade': 'B'},
    {'name': 'Peter', 'grade': 'C'},
    {'name': 'Mary', 'grade': 'A'}
]
print(students)

count_A = 0
for s in students: 
    if s['grade'] == 'A':
        count_A += 1

print("จำนวนนักเรียนที่ได้เกรด A ทั้งหมด:", count_A)
