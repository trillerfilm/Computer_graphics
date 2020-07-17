from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QImage, QPen, QColor, QPainter,QPixmap,qRgb
from PyQt5.QtCore import Qt
import sys
import re
import math as m
import numpy as np
import random
import time
from vectors import vector
from Points import Point

scr_x = 781  # Ширина картинки
scr_y = 521  # Высота картинки
global min_zbuf
min_zbuf = -9223372036854775807
global max_z
global half_scr_x
half_scr_x = 0
global half_scr_y
half_scr_y = 0
width = 781
global height
height = 650
global mas
mas = np.empty(shape=(10,),dtype=int)

class all_obj(object):
    # Класс содержащий все объекты и объявление операций над ними
    def  __init__(self):
        self.objects = []

    def add(self, elem):
        self.objects.append(elem)

    def turn_right(self,win):
        for k in self.objects:
            k.turn_right_point(win)

    def turn_left(self,win):
        for k in self.objects:
            k.turn_left_point(win)

    def turn_z_left(self,win):
        for k in self.objects:
            k.turn_z_left_point(win)

    def turn_z_right(self,win):
        for k in self.objects:
            k.turn_z_right_point(win)

    def turn_up(self,win):
        #Поворот вверх
        for k in self.objects:
            k.turn_up_point(win)

    def turn_down(self,win):
        # Поворот вниз
        for k in self.objects:
            k.get_turn_down(win)

    def clean(self):
        self.objects.clear()
    # Будут еще повороты вправо и влево + движение
global ligh
ligh = 255
global objects
# Глобальный объект содержащий все объекты сцены
objects = all_obj()



class MyWindow(QtWidgets.QMainWindow):
    # Класс окна PyQt5
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('untitled.ui', self)
        self.scene = QtWidgets.QGraphicsScene(3, 3, 781, 650)
        self.graphicsView.setScene(self.scene)
        #self.sld = verticalSlider(Qt.vertical,self)
        self.verticalSlider.valueChanged.connect(self.change)
        self.image = QImage(781, 650, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.checkBox.toggle()
        self.checkBox.stateChanged.connect(self.changeK)
        self.color_line = QColor(Qt.black)
        self.up.clicked.connect(self.show_modef)
        self.pushButton.clicked.connect(lambda: get_mod(self))
        self.turn.clicked.connect(lambda: self.for_turn_up())
        self.turn_d.clicked.connect(lambda: self.for_turn_down())
        self.right_2.clicked.connect(lambda: self.for_turn_right())
        self.left_2.clicked.connect(lambda: self.for_turn_left())
        self.z_left.clicked.connect(lambda: self.for_turn_z_left())
        self.z_right.clicked.connect(lambda: self.for_turn_z_right())
        self.delit.clicked.connect(lambda: self.dell())
        self.point = None
        self.flag = 1

    def dell(self):
        self.scene.clear()
        self.image = QImage(781, 650, QImage.Format_ARGB32_Premultiplied)
        objects.clean()

    def changeK(self, state):
        if state == Qt.Checked:
            self.flag = 1
        else:
            self.flag = 0
    def change(self):
        global ligh
        ligh = self.verticalSlider.value()

    def show_modef(self):
        if self.flag == 1:
            show_all_models2(self)
        else:
            show_all_models1(self)
    def Delete_all(self):
        # Очистка сцены
        self.scene.clear()
        self.image = QImage(781, 650, QImage.Format_ARGB32_Premultiplied)

    def update(self):
        #Обновление кадра
        pix = QPixmap(781, 650)
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)

    def for_turn_up(self):
        objects.turn_up(self)

    def for_turn_down(self):
        objects.turn_down(self)

    def for_turn_right(self):
        objects.turn_right(self)

    def for_turn_left(self):
        objects.turn_left(self)

    def for_turn_z_left(self):
        objects.turn_z_left(self)

    def for_turn_z_right(self):
        objects.turn_z_right(self)

class Obj(object):

    def __init__(self, mass1, mass2):
        # Инициализация
        self.points = mass1.copy()
        self.tri = mass2.copy()

    def copy(self):
    # метод копирования
        return Obj(self.points, self.tri)

    # Будут анологичные алгоритмы вращения вокруг других осей
    def turn_right_point(self, win):
        # Поворот вокруг оси оy вправо
        for j in self.points:
            x = j.x
            x = x - 325 / half_scr_y

            matr = np.matrix([[m.cos(m.pi / 30), 0, m.sin(m.pi / 30),0 ], \
                              [0,1 , 0, 0], \
                              [-m.sin(m.pi / 30), 0, m.cos(m.pi / 30),0],\
                              [0,0,0,1]])
            matr = np.linalg.inv(matr)
            vector_turn = np.matrix([j.norma.x,j.norma.y,j.norma.z,0])
            vector_turn = vector_turn.dot(matr)
            new_v = vector(vector_turn[0,0],vector_turn[0,1],vector_turn[0,2])
            new = Point(x*m.cos(m.pi/30)+j.z*m.sin(m.pi/30)+ 325 / half_scr_y,j.y,-x*m.sin(m.pi/30) + j.z*m.cos(m.pi/30),new_v)

            j.x = new.x
            j.z = new.z
            j.norma = new.norma
        if win.flag ==0:
            show_all_models1(win)
        else:
            show_all_models2(win)

    def turn_z_right_point(self,win):
        for j in self.points:
            x = j.x
            x = x - 325 / half_scr_y
            y = j.y
            y = y - 325 / half_scr_y

            matr = np.matrix([[m.cos(-m.pi / 30), -m.sin(-m.pi / 30), 0 , 0], \
                              [m.sin(-m.pi / 30), m.cos(-m.pi / 30), 0, 0], \
                              [0, 0, 1,0],\
                              [0, 0, 0, 1]])
            matr = np.linalg.inv(matr)
            vector_turn = np.matrix([j.norma.x,j.norma.y,j.norma.z,0])
            vector_turn = vector_turn.dot(matr)
            new_v = vector(vector_turn[0,0],vector_turn[0,1],vector_turn[0,2])
            new = Point(x*m.cos(-m.pi/30)-y*m.sin(-m.pi/30),x*m.sin(-m.pi/30) + y*m.cos(-m.pi/30),j.z,new_v)
            j.x = new.x + 325 / half_scr_y
            j.y = new.y + 325 / half_scr_y
            j.norma = new.norma
        if win.flag == 0:
            show_all_models1(win)
        else:
            show_all_models2(win)
    def turn_z_left_point(self,win):
        for j in self.points:
            x = j.x
            x = x - 325 / half_scr_y
            y = j.y
            y = y - 325 / half_scr_y

            matr = np.matrix([[m.cos(m.pi / 30), -m.sin(m.pi / 30), 0 , 0], \
                              [m.sin(m.pi / 30), m.cos(m.pi / 30), 0, 0], \
                              [0, 0, 1,0],\
                              [0, 0, 0, 1]])
            matr = np.linalg.inv(matr)
            vector_turn = np.matrix([j.norma.x,j.norma.y,j.norma.z,0])
            vector_turn = vector_turn.dot(matr)
            new_v = vector(vector_turn[0,0],vector_turn[0,1],vector_turn[0,2])
            new = Point(x*m.cos(m.pi/30)-y*m.sin(m.pi/30),x*m.sin(m.pi/30) + y*m.cos(m.pi/30),j.z,new_v)
            j.x = new.x + 325 / half_scr_y
            j.y = new.y +325 / half_scr_y
            j.norma = new.norma
        if win.flag == 0:
            show_all_models1(win)
        else:
            show_all_models2(win)

    def turn_left_point(self, win):
        # Поворот вокруг оси оy вправо
        for j in self.points:
            x = j.x
            x = x - 325 / half_scr_y

            matr = np.matrix([[m.cos(-m.pi / 30), 0, m.sin(-m.pi / 30),0 ], \
                              [0,1 , 0, 0], \
                              [-m.sin(-m.pi / 30), 0, m.cos(-m.pi / 30),0],\
                              [0,0,0,1]])
            matr = np.linalg.inv(matr)
            vector_turn = np.matrix([j.norma.x,j.norma.y,j.norma.z,0])
            vector_turn = vector_turn.dot(matr)
            new_v = vector(vector_turn[0,0],vector_turn[0,1],vector_turn[0,2])
            new = Point(x*m.cos(-m.pi/30)+j.z*m.sin(-m.pi/30)+ 325 / half_scr_y,j.y,-x*m.sin(-m.pi/30) + j.z*m.cos(-m.pi/30),new_v)
            j.x = new.x
            j.z = new.z
            j.norma = new.norma
        if win.flag == 0:
            show_all_models1(win)
        else:
            show_all_models2(win)


    def turn_up_point(self, win):
        # Поворот вокруг оси ох вверх
        for j in self.points:
            y = j.y
            y = y - 325 / half_scr_y
            matr = np.matrix([[1, 0, 0,0 ], \
                              [0, m.cos(m.pi / 30), m.sin(m.pi / 30),0], \
                              [0, -m.sin(m.pi / 30), m.cos(m.pi / 30),0],\
                              [0,0,0,1]])
            matr = np.linalg.inv(matr)
            vector_turn = np.matrix([j.norma.x,j.norma.y,j.norma.z,0])
            vector_turn = vector_turn.dot(matr)
            new_v = vector(vector_turn[0,0],vector_turn[0,1],vector_turn[0,2])

            new = Point(j.x, (y * m.cos(m.pi / 30) + j.z * m.sin(m.pi / 30))+325 / half_scr_y, -y * (m.sin(m.pi / 30)) + j.z * m.cos(m.pi / 30),new_v)

            j.y = new.y
            j.z = new.z
            j.norma = new.norma
        if win.flag == 0:
            show_all_models1(win)
        else:
            show_all_models2(win)
    #Поворот вокруг оси ох вниз
    def get_turn_down(self, win):
        for j in self.points:
                y = j.y
                y = y - 325 / half_scr_y
                matr = np.matrix([[1, 0, 0, 0], \
                                  [0, m.cos(-m.pi / 30), m.sin(-m.pi / 30), 0], \
                                  [0, -m.sin(-m.pi / 30), m.cos(-m.pi / 30), 0], \
                                  [0, 0, 0, 1]])
                matr = np.linalg.inv(matr)
                vector_turn = np.matrix([j.norma.x, j.norma.y, j.norma.z,0])
                vector_turn = vector_turn.dot(matr)
                new_v = vector(vector_turn[0, 0], vector_turn[0, 1], vector_turn[0, 2])
                new = Point(j.x, (y * m.cos(-m.pi / 30) + j.z * m.sin(-m.pi / 30))+325 / half_scr_y,-y * (m.sin(-m.pi / 30)) + j.z * m.cos(-m.pi / 30),new_v)
                j.y = new.y
                j.z = new.z
                j.norma = new.norma
        if win.flag == 0:
            show_all_models1(win)
        else:
            show_all_models2(win)




def zero_div(a, b):
    # Деление на 0
    return float(a)/b if b else 0

def Bres_int(win, d1, d2):
    min_m = min(half_scr_x, half_scr_y)
    # Отрисовка прямой по алгоритму Брезенхема
    #print(d1.x,d2.x)
    #x1 = int(d1.x * min_m/abs(1 - (d1.z/(max_z + 10)))) +150
    #y1 = 650 - int(d1.y * min_m/(1 - (d1.z/(max_z + 10))))
    #x2 = int(d2.x * min_m/abs(1 - (d2.z/(max_z + 10)))) +150
    #y2 = 650 - int(d2.y * min_m/(1 - (d2.z/(max_z + 10))))
    x1 = int(d1.x * min_m +150)
    y1 = 650 - int(d1.y * min_m)
    x2 = int(d2.x * min_m) + 150
    y2 = 650 - int(d2.y * min_m)
    if x1 == x2 and y1 == y2:
        win.image.setPixel(x1, y1, win.pen.color().rgb())
    else:
        dX = x2 - x1
        dY = y2 - y1
        if dX<0:
            SX = -1
        else:
            SX = 1
        if dY<0:
            SY = -1
        else:
            SY = 1
        dX = abs(dX)
        dY = abs(dY)

        x = x1
        y = y1

        change = False
        if dX < dY:
            dX, dY = dY, dX
            change = True
        e = 2*dY - dX

        i = 1
        while i <= dX:
            win.image.setPixel(x, y, win.pen.color().rgb())
            if e >= 0:
                if change == False:
                    y += SY
                else:
                    x += SX
                e -= 2*dX
            if e < 0:
                if change == False:
                    x += SX
                else:
                    y += SY
                e += 2*dY
            i += 1


def show_all_models1(win):
    # Отображение объектов с тонировкой
    win.Delete_all()
    qwe = 0
    new = QColor()
    # Инициализация z-буфера.
    zbufer = np.full(width * (height+1),-10000)
    # Инициализация  луча света(возможно заменю на vector )
    light_dir = vector(0, 0, -1)
    for k in objects.objects:
        # перебор всех объектов
        start_time = time.clock()
        for i in k.tri:
            qwe = triangle(i, win, zbufer,qwe,light_dir)
        print("{:g} s".format(time.clock() - start_time))

    win.update()

def show_all_models2(win):
    #Отображаем все модели их каркасами
    win.Delete_all()
    new = QColor()
    for k in objects.objects:
        for i in k.tri:
            new.setRgb(0,0,0)
            karkas(i, win)
    win.update()


def karkas(coords, win):
    # Отрисовка каркаса объекта прямыми.
    t1, t2, t3 = sorted(coords, key=lambda p: p.y)
    a = Point(t1.x, t1.y, t1.z, t1.norma)
    b = Point(t2.x, t2.y, t2.z, t1.norma)
    c = Point(t3.x, t3.y, t3.z, t1.norma)

    Bres_int(win, a, b)
    Bres_int(win, b, c)
    Bres_int(win, c, a)

def triangle(coords, win, zbufer,rte,light_dir):

    new = QColor()
    #Отрисовка поверхности треугольниками. Внимание тут будет дописан Гуро!!!
    a = Point(coords[0].x, coords[0].y, coords[0].z, coords[0].norma)
    b = Point(coords[1].x, coords[1].y, coords[1].z, coords[1].norma)
    c = Point(coords[2].x, coords[2].y, coords[2].z, coords[2].norma)

    min_m = min(half_scr_x,half_scr_y)
    # Преобразование координат к экранным
    a.x = int(a.x * min_m )+ 150
    a.y = 650 - int(a.y * min_m )
    a.z = a.z * min_m
    b.x = int(b.x * min_m ) + 150
    b.y = 650 - int(b.y * min_m )
    b.z = b.z * min_m
    c.x = int(c.x * min_m ) +150
    c.y = 650 - int(c.y * min_m )
    c.z = c.z * min_m
    #Сортировка по возростанию y
    a,b,c = sorted([a,b,c], key=lambda p: p.y)

    I1 = ligh * light_dir.mul(a.norma)
    I2 = ligh * light_dir.mul(b.norma)
    I3 = ligh * light_dir.mul(c.norma)
    # Вырожденный треугольник
    if a.y == b.y and a.y == c.y:
        return rte
    win.pen.setColor(new)

    total_height = c.y - a.y
    win.pen.setColor(new)
    # Цикл по всем строкам треугольника. Каждую строку закрашиваем.
    for i in range(total_height):
        # Сначала вычисляем границы строки
        test = (i > b.y - a.y) or(b.y == a.y)

        if test:
            seg = c.y - b.y
        else:
            seg = b.y - a.y
        first = Point(i/total_height, 1, 1,0)

        if test:
            second = Point((i - b.y + a.y)/seg, 1, 1,0)
        else:
            second = Point(i/seg, 1, 1,0)
        al = a + (c - a) * first

        if test:
            bl = b + (c - b) * second
        else:
            bl = a + (b - a) * second

        #линейная интерполяция
        if test == False and a.y != b.y:
            Ia = abs(I1 + ((I2 - I1)/(b.y - a.y))*(i))
        elif test and b.y != c.y:
            Ia = abs(I2 + ((I3 - I2)/(c.y - b.y))*(a.y + i - b.y))
        else:
            Ia = abs(I1 + (I2 - I1) * (i))
        if (c.y != a.y):
            Ib = abs(I1 + ((I3 - I1)/(c.y - a.y))*(i))
        else:
            Ib =abs( I1 + (I3 - I1) * (i))
        if al.x > bl.x:
            al, bl = bl, al
        else:
            Ia, Ib = Ib, Ia

        # Идём от одной вычесленной границы до другой
        # Пока нет защиты от выхода за границы экрана.
        for j in range(int(al.x),int(bl.x)+1):

            if al.x == bl.x:
                phi = 1
            else:
                phi = (j - al.x)/(bl.x - al.x)

            p = Point(j,a.y+i,al.z + (bl.z-al.z)*phi,0)
            idx = int(p.x+p.y*width)
            # Применяем z-буфер


            if (bl.x - al.x) == 0:
                I = abs(Ia + (Ib - Ia)*(p.x-al.x))
            else:
                I = abs(Ia + (Ib - Ia)/(bl.x - al.x)*(p.x - al.x))
            #new.setRgb( int(I),int(I),int(I))
            try:
                if (zbufer[idx] < p.z):
                    zbufer[idx] = p.z

                    #win.image.setPixel(p.x, p.y, win.pen.color().rgb())
                    if p.x < 780 and p.x > 0 and p.y< 650 and p.y > 0:

                        win.image.setPixel(p.x, p.y,qRgb(int(I), int(I), int(I)))
            except:
                return rte
    return rte

def normolize_all(points):
    for i in points:
        i.norma.normolize()


class for_normals():
    def __init__(self):
        self.for_no = []

    def get_medium(self):
        sumx = 0
        sumy = 0
        sumz = 0
        for i in range(len(self.for_no)):
            sumx += self.for_no[i].x
            sumy += self.for_no[i].y
            sumz += self.for_no[i].z
        return vector(sumx/len(self.for_no),sumy/len(self.for_no),sumz/len(self.for_no))

def get(win, min_x, min_y, min_z, len,quantity,fname):
    # Ещё раз считываем obj файл, для записи точек(с нормалями), и разбиения на треугольники.
    if (min_x > 0):
        min_x = 0
    if (min_y > 0):
        min_y = 0
    if (min_z > 0):
        min_z = 0
    f = open(fname, 'r')
    new = QColor()
    lines = f.read()
    i = 0
    j = 0
    k = 0
    points = np.empty(shape = (len,), dtype = Point)
    triangl_normals = np.empty(shape = (len,), dtype= for_normals)
    for l in range(len):
        triangl_normals[l] = for_normals()
    world_coords = np.empty(shape = (3,), dtype= Point)
    communication = np.empty(shape = (quantity,), dtype = Point)
    normals = np.empty(shape = (len,), dtype = vector)
    for line in lines.split('\n'):

        try:
            v, x, y, z = re.split('\s+', line)

        except:
            try:
                v, x, y, z = re.split('\s+', line[:-1])
            except:
                continue

        if v == 'v':
            points[i] = Point(float(x) - min_x, float(y) - min_y, float(z) - min_z, None)

            i += 1
        if v == 'f':
            world_coords[0] = points[int(x.split('/')[0]) - 1]
            world_coords[1] = points[int(y.split('/')[0]) - 1]
            world_coords[2] = points[int(z.split('/')[0]) - 1]
            n = (world_coords[2] - world_coords[0]) ** (world_coords[1] - world_coords[0])
            n =  vector(n.x,n.y,n.z)
            q = n.normolize()
            triangl_normals[int(x.split('/')[0]) - 1].for_no.append(q)
            triangl_normals[int(y.split('/')[0]) - 1].for_no.append(q)
            triangl_normals[int(z.split('/')[0]) - 1].for_no.append(q)
            communication[j] = [points[int(i.split('/')[0])-1] for i in (x, y, z)]
            j += 1
    for i in range(len):
        points[i].norma = triangl_normals[i].get_medium()
    normolize_all(points)
    subject = Obj(points, communication)
    objects.add(subject)

    if win.flag == 0:
        show_all_models1(win)
    else:
        show_all_models2(win)
    f.close()
def get_mod(win):
    # Считывание obj файла и вычисление множителя размера и сдвиг в положительные координаты.
    fname = QtWidgets.QFileDialog.getOpenFileName(win, 'Open file', '/home')[0]
    print(fname)
    global half_scr_x
    global half_scr_y
    global max_z
    f = open(fname, 'r')
    lines = f.read()
    len = 0
    quantity = 0
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    min_z = 0
    max_z = 0
    for line in lines.split('\n'):
        try:
            v, x, y, z = re.split('\s+', line)
        except:
            continue

        if v == 'v':

            x = float(x)
            y = float(y)
            z = float(z)
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if z < min_z:
                min_z = z
            if z > max_z:
                max_z = z
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            len += 1
        if v == 'f':
            quantity += 1

    mod = max((max_x+abs(min_x)),(max_y+abs(min_y)))

    half_scr_x = 781/mod
    half_scr_y = 521/mod
    f.close()
    get(win, min_x, min_y, min_z, len, quantity,fname)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()