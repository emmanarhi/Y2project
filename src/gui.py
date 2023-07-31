import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from main import load_map

from src.coordinates import Coordinates
from character_graphics_item import PlayerGraphicsItem, EnemyGraphicsItem
from direction import Direction
from save_game import *
from square_graphics_item import SquareGraphicsItem
import time


class MainMenu(QtWidgets.QWidget):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.chosen_world = 0
        self.init_main()

    def init_main(self):
        world1_button = QtWidgets.QPushButton("World1")
        world1_button.clicked.connect(lambda: self.play_game(1))
        world2_button = QtWidgets.QPushButton("World2")
        world2_button.clicked.connect(lambda: self.play_game(2))
        world3_button = QtWidgets.QPushButton("Make you own world")
        world3_button.clicked.connect(lambda: self.play_game(3))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(world1_button)
        layout.addWidget(world2_button)
        layout.addWidget(world3_button)

        self.setLayout(layout)
        self.setGeometry(100, 100, 200, 100)
        self.setWindowTitle('Main Menu')

    def play_game(self, world_num):
        self.chosen_world = load_map("../data/worlds.txt", world_num)
        if world_num != 3:
            self.gui.switch_to_game()
        else:
            self.gui.switch_to_editor()


class GUI(QtWidgets.QMainWindow):

    def __init__(self, square_size):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Strategy Game')
        self.show()

        self.scene = QtWidgets.QGraphicsScene(self)
        self.main_menu = MainMenu(self)
        self.setCentralWidget(self.main_menu)

        self.square_size = square_size
        self.edit_first = False

    def switch_to_game(self):
        self.world = self.main_menu.chosen_world

        self.view = GameView(self.scene, self.world, self)

        self.added_players = []
        self.player_graphics = []

        self.added_enemies = []
        self.enemy_graphics = []

        self.add_world_grid_items()
        self.add_player_graphic_items()
        self.add_enemy_graphic_items()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_characters)
        self.timer.start(100)

        if not self.edit_first:
            self.main_menu.hide()
        self.setCentralWidget(self.view)

        self.start_time = time.time()

    def switch_to_editor(self):
        self.edit_first = True
        self.world = self.main_menu.chosen_world

        self.edit_view = EditView(self.scene, self.world, self)

        self.added_players = []
        self.player_graphics = []

        self.added_enemies = []
        self.enemy_graphics = []

        self.add_world_grid_items()
        self.add_player_graphic_items()
        self.add_enemy_graphic_items()

        self.setCentralWidget(self.edit_view)
        self.main_menu.hide()



    def add_world_grid_items(self):
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                coords = Coordinates(x, y)
                sqr = self.world.get_square(coords)
                square = SquareGraphicsItem(x * self.square_size, y * self.square_size, self.square_size,
                                                     self.square_size, sqr)
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
            if play_char not in self.added_players:
                player_graphic = PlayerGraphicsItem(play_char, self.square_size)
                self.scene.addItem(player_graphic)
                self.added_players.append(play_char)
                self.player_graphics.append(player_graphic)

                player_graphic.text_item = QtWidgets.QGraphicsTextItem("{} {}".format(str(play_char.hp),
                                                                                      str(play_char.energy)),
                                                                       parent=player_graphic)

                player_graphic.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                player_graphic.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def add_enemy_graphic_items(self):
        for enemy in self.world.get_enemies():
            if enemy not in self.added_enemies:
                enemy_graphic = EnemyGraphicsItem(enemy, self.square_size)
                self.scene.addItem(enemy_graphic)
                self.added_enemies.append(enemy)
                self.enemy_graphics.append(enemy_graphic)

                enemy_graphic.text_item = QtWidgets.QGraphicsTextItem("{} {}".format(str(enemy.hp),
                                                                                     str(enemy.energy)),
                                                                      parent=enemy_graphic)

                enemy_graphic.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                enemy_graphic.setFlags(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def update_characters(self):
        for play_char in self.player_graphics:
            if play_char.char.is_dead():
                play_char.char.get_location_square().remove_play_char()
                play_char.text_item.hide()
                play_char.hide()
            else:
                play_char.updateAll()
                play_char.text_item.setPlainText("{} {}".format(str(play_char.char.hp), str(play_char.char.energy)))

        for enemy in self.enemy_graphics:
            if enemy.char.is_dead():
                enemy.char.get_location_square().remove_play_char()
                enemy.text_item.hide()
                enemy.hide()
            else:
                enemy.updateAll()
                enemy.text_item.setPlainText("{} {}".format(str(enemy.char.hp), str(enemy.char.energy)))

        if self.world.game_over() != 0:
            self.win_time = time.time()
            self.timer.stop()

            if self.world.game_over() == 1:
                self.game_won()
            elif self.world.game_over() == -1:
                self.game_lost()
        else:
            if not self.world.player_turn:
                self.world.enemy_turn()


    def game_won(self):
        win_time = self.win_time - self.start_time
        won_text = QtWidgets.QGraphicsTextItem("You won the game yippee\n It took {:.1f} seconds".format(win_time))
        won_text.setFont(QtGui.QFont("Arial", 24))
        won_text.setPos(150,200)
        self.scene.addItem(won_text)

    def game_lost(self):
        loss_text = QtWidgets.QGraphicsTextItem("You lost:(")
        loss_text.setFont(QtGui.QFont("Arial", 24))
        loss_text.setPos(150, 200)
        self.scene.addItem(loss_text)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Q:
            save_game(self.world, "../data/saved_game.txt")
            sys.exit()

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
        if event.key() == QtCore.Qt.Key.Key_Q:
            save_game(self.world, "/data/saved_game.txt")
            sys.exit()

        if self.world.player_turn:
            if self.selected_player is not None:
                if event.key() == QtCore.Qt.Key.Key_Right:
                    self.selected_player.char.move(Direction.EAST)
                elif event.key() == QtCore.Qt.Key.Key_Left:
                    self.selected_player.char.move(Direction.WEST)
                elif event.key() == QtCore.Qt.Key.Key_Up:
                    self.selected_player.char.move(Direction.NORTH)
                elif event.key() == QtCore.Qt.Key.Key_Down:
                    self.selected_player.char.move(Direction.SOUTH)
                self.world.player_turn = False
                if self.selected_player.char.is_dead():
                    self.selected_player = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())

            # Katsotaan, että mikä hahmo valittuna pelattavista hahmoista
            if isinstance(item, PlayerGraphicsItem):
                if item != self.selected_player:
                    if self.selected_player is not None:
                        self.selected_player.moving = False
                        self.selected_player.updateColor()

                    self.selected_player = item
                    self.selected_player.moving = True
                    self.selected_player.updateColor()
            elif isinstance(item, EnemyGraphicsItem):
                if self.selected_player is not None:
                    menu = QtWidgets.QMenu(self)
                    action1 = menu.addAction("Basic Attack")
                    action2 = menu.addAction("Charged Attack")
                    action = menu.exec(self.mapToGlobal(event.pos()))

                    if self.world.player_turn:
                        if action == action1:
                            if self.selected_player.char.basic_attack(item.char):
                                self.world.player_turn = False
                        elif action == action2:
                            if self.selected_player.char.charged_attack(item.char):
                                self.world.player_turn = False

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.selected_player is not None:
                menu = QtWidgets.QMenu(self)
                action1 = menu.addAction("Heal")
                action = menu.exec(self.mapToGlobal(event.pos()))

            if self.world.player_turn:
                if action == action1:
                    if self.selected_player.char.hp < 10:
                        self.selected_player.char.heal()
                        self.world.player_turn = False


class EditView(GameView):
    def __init__(self, scene, world, gui):
        super().__init__(scene, world, gui)

    # Q saa taas pelin loppumaan ja S aloittaa pelin
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Q:
            sys.exit()
        if event.key() == QtCore.Qt.Key.Key_S:
            self.gui.switch_to_game()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())

            if isinstance(item, SquareGraphicsItem):
                print(item.brush().color().value())
                if item.brush().color().value() == QtGui.QColor(60, 150, 70).value():
                    item.setBrush(QtGui.QColor(165, 226, 224))
                    item.square.is_lava = False
                    item.square.is_tree = False
                    item.square.is_water = True
                elif item.brush().color().value() == QtGui.QColor(165, 226, 224).value():
                    item.setBrush(QtGui.QColor(242, 100, 60))
                    item.square.is_lava = True
                    item.square.is_water = False
                    item.square.is_tree = False
                elif item.brush().color().value() == QtGui.QColor(242, 100, 60).value():
                    item.setBrush(QtGui.QColor(120, 160, 120))
                    item.square.is_lava = False
                    item.square.is_water = False
                    item.square.is_tree = False
                elif item.brush().color().value() == QtGui.QColor(120, 160, 120).value():
                    item.setBrush(QtGui.QColor(60, 150, 70))
                    item.square.is_tree = True
                    item.square.is_lava = False
                    item.square.is_water = False
