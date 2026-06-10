def decorator1(func):
    def wrapper(*a,**b):
        print("before fun")
        func(*a,**b)
        print("after fun") 
    return wrapper
@decorator1
def poda(a,b):
    print(a+b)
poda(10,20)