from PyQt6 import QtWidgets, QtGui, QtCore
from player import Player
from direction import Direction


class PlayerGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, play_char, square_size):
        super(PlayerGraphicsItem, self).__init__()

        self.play_char = play_char
        self.square_size = square_size
        brush = QtGui.QBrush(1) # 1 for even fill
        self.setBrush(brush)
        self.constructTriangleVertices()
        self.updateAll()


    def constructTriangleVertices(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(self.square_size/2, 0)) # Tip
        triangle.append(QtCore.QPointF(0, self.square_size)) # Bottom-left
        triangle.append(QtCore.QPointF(self.square_size, self.square_size)) # Bottom-right
        triangle.append(QtCore.QPointF(self.square_size/2, 0)) # Tip

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

        # Set the origin of transformations to the center of the triangle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)

    def updateAll(self):
        self.updatePosition()
        self.updateRotation()
        self.updateColor()

    def updatePosition(self):
        location_x = self.play_char.get_location().get_x()
        location_y = self.play_char.get_location().get_y()
        if location_x == 0 and location_y == 0:
            self.setPos(0, 0)
        else:
            self.setX(location_x * self.square_size)
            self.setY(location_y * self.square_size)

    def updateRotation(self):
        facing = self.play_char.get_facing()
        if facing == (1, 0):
            self.setRotation(90)
        elif facing == (0, -1):
            self.setRotation(0)
        elif facing == (-1, 0):
            self.setRotation(-90)
        else:
            self.setRotation(180)

    def updateColor(self):
        self.setBrush((QtGui.QColor(200, 255, 200)))

    def mousePressEvent(self, *args, **kwargs):
        self.play_char.move_forward()
