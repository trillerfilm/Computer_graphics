import math as m
class vector():
    # Класс вектора
    def __init__(self,x,y,z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def no(self):
        return m.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

    def normolize(self):
        # Вычисление нормали(Не актуально так как теперь считывается из файла)
        if self.no() != 0:
            x = self.x / self.no()
            y = self.y / self.no()
            z = self.z / self.no()
            return vector(x,y,z)
        else:
            return 0

    def __pow__(self, other):
        # перегрузка умножение векторов
        return vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def mul(self,other):
        return float(self.x) * float(other.x) + float(self.y) * float(other.y) + float(self.z) * float(other.z)
