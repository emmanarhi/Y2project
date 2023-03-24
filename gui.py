from PyQt6 import QtWidgets, QtCore, QtGui
from coordinates import Coordinates
from player_graphics_item import PlayerGraphicsItem


class GUI(QtWidgets.QMainWindow):

    def __init__(self, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.world = world
        self.added_characters = []
        self.player_graphics = []
        self.square_size = square_size
        self.init_window()

        self.add_world_grid_items()
        self.add_player_graphic_items()
        self.update_characters()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_characters)
        self.timer.start(10)

    def init_window(self):
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Strategy Game')
        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 700)

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

    def add_world_grid_items(self):
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                square = QtWidgets.QGraphicsRectItem(x * self.square_size, y * self.square_size, self.square_size, self.square_size)
                coords = Coordinates(x, y)
                sqr = self.world.get_square(coords)
                if sqr.is_tree_square():
                    square.setBrush(QtGui.QColor(60, 150, 70))
                    self.scene.addItem(square)
                elif sqr.is_water_square():
                    square.setBrush(QtGui.QColor(165, 226, 224))
                    self.scene.addItem(square)
                elif sqr.is_lava_square():
                    square.setBrush(QtGui.QColor(242, 100, 60))
                    self.scene.addItem(square)
                else:
                    square.setBrush(QtGui.QColor(120, 160, 120))
                    self.scene.addItem(square)

    def add_player_graphic_items(self):

        for play_char in self.world.get_play_chars():
            if play_char not in self.added_characters:
                player_graphic = PlayerGraphicsItem(play_char, self.square_size)
                self.scene.addItem(player_graphic)
                self.added_characters.append(play_char)
                self.player_graphics.append(player_graphic)

    def update_characters(self):
        for play_char in self.player_graphics:
            play_char.updateAll()
