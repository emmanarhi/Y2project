class AI:
    def __init__(self):
        self.best_utilities = [0]
        self.best_enemy = None
        self.best_utility
    def choose_enemy(self, enemies, players):
        for enemy in enemies:
            utility_sum = sum(UtilityAI.select_action(enemy, players))
            best_utility_sum = sum(self.best_utilities)
            if utility_sum > best_utility_sum:
                self.best_utility = UtilityAI.best_action
                self.best_enemy = enemy

    def execute_command(self):




class UtilityAI:
    def __init__(self, enemy, players):
        self.best_action = None
        self.enemy = enemy

    def dist_and_dir(self, enemy, players):
        # Funktio etsii pienimmän etäisyyden läheiseen pelaajaan ja suunnan sinne
        # Tähän pitää muistaa unit testit
        distances = []
        directions = []

        for player in players:
            distance = enemy.get_location().get_distance(player.get_location())
            direction = enemy.get_location().get_direction(player.get_location())

            distances.append(distance)
            directions.append(direction)

        min_distance = min(distances)
        index = distances.index(min_distance)
        the_direction = directions[index]
        return min_distance, the_direction

    def select_action(self, enemy, players):
        move_utility = self.move_utility(enemy, players)
        attack_utility = self.attack_utility(enemy, players)
        heal_utility = self.heal_utility(enemy, players)
        utilities = [move_utility, attack_utility, heal_utility]

        if max(move_utility, attack_utility, heal_utility) == move_utility:
            self.best_action = enemy.move()
        elif max(move_utility, attack_utility, heal_utility) == attack_utility:
            self.best_action = enemy.attack()
        elif max(move_utility, attack_utility, heal_utility) == heal_utility:
            self.best_action = enemy.heal()

        return utilities

    def move_utility(self, enemy, players):
        # Lasketaan liikkumisen hyödyllisyys etäisyyden ja terveyden perusteella
        smallest_dist = self.dist_and_dir(enemy, players)[0]
        health_ratio = enemy.hp / enemy.max_hp
        if smallest_dist != 1:
            utility = health_ratio * (1 / (smallest_dist + 1))
        else:
            utility = 0
        return utility

    def attack_utility(self, enemy, players):
        # Nyt tälleen koska ei vielä pidemmän rangen hyökkäyksiä, niille vaikka erikseen tehdään tämä
        smallest_dist = self.dist_and_dir(enemy, players)[0]
        health_ratio = enemy.hp / enemy.max_hp
        utility = health_ratio * smallest_dist

        if utility == 1:
            return utility
        else
            return 0

    def heal_utility(self, enemy):
        health_ratio = enemy.hp / enemy.max_hp
        utility = 1 - health_ratio
        return utility


    def execute_action(self, enemy, players):
        enemy.move_forward()