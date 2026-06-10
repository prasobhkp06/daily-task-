def calculate_grade(name,*marks):
    for i in marks:
        if i<0 or i>100:
            raise InvalidMarkError("Enter a Valid Mark")
    for i in marks:
        if i>=90:
            grade="A"
        elif i>=75:
            grade="B"
        elif i>=50:
            grade="C"
        else:
            grade="D"
    Average=sum(marks)/len(marks)
    print("Name: ",name)
    print("Grade: ",grade)
    print("Average: ",Average)

class InvalidMarkError(Exception):
    pass
try:
    calculate_grade(input("Enter Name: "),*[int(input(f"enter mark {i+1}: ")) for i in range(5)])
except InvalidMarkError as e:
    print(e)
else:
    print("Success")
finally:
    print("Done")