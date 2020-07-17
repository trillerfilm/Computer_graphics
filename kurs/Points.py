class Point(object):
    # Класс точка содержащий координаты и нормаль к точке
    def __init__(self, x, y, z, norma):
        self.x = x

        self.y = y

        self.z = z

        self.norma = norma

    def copy(self):
        return Point(self.x, self.y, self.z)

    def swap(self, b):
        # Обмен значний точек
        self.x, b.x = b.x, self.x
        self.y, b.y = b.y, self.y
        self.z, b.z = b.z, self.z
        self.norma, b.norma = b.norma, self.norma

    def __sub__(self, other):
        # перегрузка вычитания
        return Point(self.x - other.x, self.y - other.y, self.z - other.z, self.norma)

    def __pow__(self, other):
        # перегрузка умножение векторов
        return Point(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x, self.norma )

    def __mul__(self,other):
        # перегрузка умножения
        return Point(self.x * other.x, self.y * other.y, self.z * other.z, self.norma)

    def __add__(self,other):
        # перегрузка сложения
        return Point(self.x + other.x,self.y + other.y,self.z + other.z, self.norma)