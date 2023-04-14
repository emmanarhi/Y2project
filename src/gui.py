from PyQt6 import QtWidgets, QtCore, QtGui

from src.coordinates import Coordinates
from player_graphics_item import PlayerGraphicsItem
from direction import Direction


class MainMenu(QtWidgets.QWidget):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.init_main()

    def init_main(self):
        play_button = QtWidgets.QPushButton("Play")
        play_button.clicked.connect(self.play_game)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(play_button)

        self.setLayout(layout)
        self.setGeometry(100, 100, 200, 100)
        self.setWindowTitle('Main Menu')

    def play_game(self):
        self.gui.switch_to_game()


class GUI(QtWidgets.QMainWindow):

    def __init__(self, world, square_size):
        super().__init__()
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
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Strategy Game')
        self.show()

        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.main_menu = MainMenu(self)
        self.setCentralWidget(self.main_menu)

        self.view = GameView(self.scene, self.world, self)

    def switch_to_game(self):
        self.main_menu.hide()
        self.setCentralWidget(self.view)

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
                print(self.player_graphics)
                player_graphic.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                player_graphic.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def update_characters(self):
        for play_char in self.player_graphics:
            play_char.updateAll()

    def selected_player(self):
        for play_char in self.player_graphics:
            if play_char.is_moving():
                return play_char


class GameView(QtWidgets.QGraphicsView):
    def __init__(self, scene, world, gui):
        super().__init__(scene)

        self.world = world
        self.scene = scene
        self.gui = gui
        self.selected_player = None

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

    def keyPressEvent(self, event):
        print(self.scene)
        self.selected_player = self.gui.selected_player()
        print(self.selected_player)
        if self.selected_player is not None:
            if event.key() == QtCore.Qt.Key.Key_Right:
                self.selected_player.play_char.move(Direction.EAST)
            elif event.key() == QtCore.Qt.Key.Key_Left:
                self.selected_player.play_char.move(Direction.WEST)
            elif event.key() == QtCore.Qt.Key.Key_Up:
                self.selected_player.play_char.move(Direction.NORTH)
            elif event.key() == QtCore.Qt.Key.Key_Down:
                self.selected_player.play_char.move(Direction.SOUTH)