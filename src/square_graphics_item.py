from PyQt6 import QtWidgets, QtGui, QtCore


class SquareGraphicsItem(QtWidgets.QGraphicsRectItem):

    def __init__(self, x, y, w, h, square):
        super().__init__(x, y, w, h)
        self.square = square