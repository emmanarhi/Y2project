from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from direction import Direction


class CharacterGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, char, square_size):
        super(CharacterGraphicsItem, self).__init__()

        self.char = char
        self.moving = False
        self.square_size = square_size
        brush = QtGui.QBrush(1)
        self.setBrush(brush)
        if self.char.name == "normal":
            self.constructTriangleVertices()
        elif self.char.name == "shooter":
            self.constructDiamondVertices()
        else:
            self.contructSquareVertices()
        self.updateAll()

        self.text_item = None

    def constructTriangleVertices(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(self.square_size/2, 0)) # Tip
        triangle.append(QtCore.QPointF(0, self.square_size)) # Bottom-left
        triangle.append(QtCore.QPointF(self.square_size, self.square_size)) # Bottom-right

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

        # Set the origin of transformations to the center of the triangle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)

    def constructDiamondVertices(self):
        diamond = QtGui.QPolygonF()

        diamond.append(QtCore.QPointF(0, self.square_size / 2))
        diamond.append(QtCore.QPointF(self.square_size / 2, self.square_size))
        diamond.append(QtCore.QPointF(self.square_size, self.square_size / 2))
        diamond.append(QtCore.QPointF(self.square_size / 2, 0))

        self.setPolygon(diamond)

        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def contructSquareVertices(self):
        square = QtGui.QPolygonF()

        square.append(QtCore.QPointF(0, 0))
        square.append(QtCore.QPointF(0, self.square_size))
        square.append(QtCore.QPointF(self.square_size, self.square_size))
        square.append(QtCore.QPointF(self.square_size, 0))


        self.setPolygon(square)

        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def updateAll(self):
        if not self.char.is_dead():
            self.updatePosition()
            self.updateRotation()
            self.updateColor()
        else:
            self.hide()

    def updateColor(self):
        pass

    def updatePosition(self):
        location_x = self.char.get_location().get_x()
        location_y = self.char.get_location().get_y()
        if location_x == 0 and location_y == 0:
            self.setPos(0, 0)
        else:
            self.setX(location_x * self.square_size)
            self.setY(location_y * self.square_size)


    def updateRotation(self):
        facing = self.char.get_facing()
        if facing == (1, 0):
            self.setRotation(90)
        elif facing == (0, -1):
            self.setRotation(0)
        elif facing == (-1, 0):
            self.setRotation(-90)
        else:
            self.setRotation(180)

    def is_moving(self):
        return self.moving


class PlayerGraphicsItem(CharacterGraphicsItem):
    def __init__(self, char, square_size):
        super(PlayerGraphicsItem, self).__init__(char, square_size)
        self.text_item = None

    def updateColor(self):
        if self.moving:
            self.setBrush((QtGui.QColor(255, 200, 200)))
        else:
            self.setBrush((QtGui.QColor(200, 255, 200)))


class EnemyGraphicsItem(CharacterGraphicsItem):
    def __init__(self, char, square_size):
        super(EnemyGraphicsItem, self).__init__(char, square_size)
        self.text_item = None

    def updateColor(self):
        self.setBrush((QtGui.QColor(255, 100, 100)))
