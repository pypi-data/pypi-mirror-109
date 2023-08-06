class cal():
    def __init__(self,a, b):
       self.a = a
       self.b = b

    def mul(self):
        return self.a * self.b


a = float(input("a:"))
b = float(input("b:"))
obj = cal(a, b)

print(obj.mul())
