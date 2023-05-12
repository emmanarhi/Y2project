
def save_game(world, filename):
    file = open(filename, "w")
    file.write("Player characters:\n")
    for play_char in world.get_play_chars():
        line = "{};{};{},{};{};{}\n".format(play_char.name, play_char.is_dead(),
                                            play_char.get_location().get_x(), play_char.get_location().get_y(),
                                            play_char.hp, play_char.energy)
        file.write(line)
    file.write("Enemy characters:\n")
    for enemy in world.get_enemies():
        line = "{};{};{},{};{};{}\n".format(enemy.name, enemy.is_dead(),
                                            enemy.get_location().get_x(), enemy.get_location().get_y(),
                                            enemy.hp, enemy.energy)
        file.write(line)
    file.close()
