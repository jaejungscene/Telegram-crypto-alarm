class Temp:
    def __init__(self, x) -> None:
        self.x = x

    def func(self):
        print(self.x)
        self.y = self.x+2
        print(self.y)


temp = Temp(321)
print(getattr(temp, 'x'))
temp.func()
print(getattr(temp, 'y'))
