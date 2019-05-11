from standard import *


class Game():

    def __init__(self):

        self.frame = None

        self.attacker = None
        self.defender = None

        self.round = 0

        self.space_deck = SPACE_TACTIC_CARDS
        self.ground_deck = GROUND_TACTICS_CARDS

        self.two_damage_one_ship = False
        self.one_damage_two_ships = False
        self.one_damage_two_ships_first = None

        self.draw_card = None

        self.retreat = 0

    def update_round(self):
        self.round += 1

        if self.round <= 2:
            self.attacker.force = self.attacker.fleet
            # self.attacker.roll = self.attacker.space_roll
            self.attacker.hand = self.attacker.space_hand

            self.defender.force = self.defender.fleet
            # self.defender.roll = self.defender.space_roll
            self.defender.hand = self.defender.space_hand

        elif self.round > 2:
            self.attacker.force = self.attacker.army
            # self.attacker.roll = self.attacker.ground_roll
            self.attacker.hand = self.attacker.ground_hand

            self.defender.force = self.defender.army
            # self.defender.roll = self.defender.ground_roll
            self.defender.hand = self.defender.ground_hand

    def play_special_damage_card(self, card):
        if card == "Deal 2 damage to 1 ship - dice" or card == "Deal 2 damage to 1 ground unit - dice":
            self.two_damage_one_ship = True
        elif card == "Deal 1 damage to 2 ships - dice" or card == "Deal 1 damage to 2 ground units - dice":
            self.one_damage_two_ships = True

    def two_damage_one_ship_card(self):
        if self.two_damage_one_ship:
            self.two_damage_one_ship = False
            return True
        else:
            return self.two_damage_one_ship

    def one_damage_two_ships_check(self, ship):

        if self.one_damage_two_ships_first is None:
            self.one_damage_two_ships_first = ship
            return True
        elif self.one_damage_two_ships_first is ship:
            return False
        else:
            self.one_damage_two_ships_first = None
            self.one_damage_two_ships = False
            return True



class Imperial():

    def __init__(self):
        self.leaders = IMPERIAL_LEADERS
        self.ships = IMPERIAL_SHIPS
        self.army = IMPERIAL_ARMY


class Rebel():

    def __init__(self):
        self.leaders = REBEL_LEADERS
        self.ships = REBEL_SHIPS
        self.army = REBEL_ARMY


class Player():

    def __init__(self, side, leader, fleet, army):
        self.frame = None
        self.side = side
        self.is_attacker = False
        self.leader = leader
        self.space_value = 0
        self.ground_value = 0
        self.space_hand = []
        self.ground_hand = []
        self.red_roll = None
        self.black_roll = None
        self.fleet = fleet
        self.army = army
        self.can_retreat = None
        self.retreat_card = False
        self.roll = None
        self.used_roll = {'Red Hits': 0, 'Black Hits': 0, 'Direct Hits': [0, []], 'Cards': 0, 'Miss': 0}
        self.space_blocks = 0
        self.ground_blocks = 0
        self.can_block = False
        self.opponent = self.set_opponent()
        self.frame = None
        self.damage = 0

    def set_opponent(self, opponent=None):
        self.opponent = opponent
        return opponent

    def set_leader(self, leader):
        self.leader = leader
        self.set_space_value(LEADER_VALUE[self.leader][0])
        self.set_ground_value(LEADER_VALUE[self.leader][1])

    def set_space_value(self, value):
        self.space_value = value
        return value

    def set_ground_value(self, value):
        self.ground_value = value
        return value

    def reset_used_roll(self):
        self.used_roll = {'Red Hits': 0, 'Black Hits': 0, 'Direct Hits': [0, []], 'Cards': 0, 'Miss': 0}

    def set_roll(self, new_roll):
        self.roll = new_roll

    def __str__(self):
        if isinstance(self.side, Imperial):
            return "Imperial Player"
        else:
            return "Rebel Player"

class Fleet():

    def __init__(self):

        self.fleet_count = {ship: 0 for ship in SHIPS}
        self.fleet = {ship: [ship() for i in range(self.fleet_count[ship])] for ship in SHIPS}
        self.black_dice = self.get_black_dice()
        self.red_dice = self.get_red_dice()

    def get_black_dice(self):

        total_dice = sum([sum([s.black_attack_value for s in self.fleet[k] if s.get_status()]) for k in self.fleet.keys()])
        if total_dice <= 5:
            return total_dice
        else:
            return 5

    def get_red_dice(self):

        total_dice = sum([sum([s.red_attack_value for s in self.fleet[k] if s.get_status()]) for k in self.fleet.keys()])
        if total_dice <= 5:
            return total_dice
        else:
            return 5

    def can_transport(self):
        return sum([sum([s.transport for s in self.fleet[k] if s.get_status()]) for k in self.fleet.keys()])

class ImperialFleet(Fleet):

    def __init__(self):
        super().__init__()
        self.fleet_count = {ship: 0 for ship in IMPERIAL_SHIPS}
        self.fleet = self.set_fleet()

    def set_fleet(self):

        self.fleet = {"TIE": [TIE() for i in range(self.fleet_count["TIE"])],
                      "Assault Carrier": [AssaultCarrier() for i in range(self.fleet_count["Assault Carrier"])],
                      "Star Destroyer": [StarDestroyer() for i in range(self.fleet_count["Star Destroyer"])],
                      "Super Star Destroyer": [SuperStarDestroyer() for i in range(self.fleet_count["Super Star Destroyer"])],
                      "Death Star": [DeathStar() for i in range(self.fleet_count["Death Star"])]}


class RebelFleet(Fleet):

    def __init__(self):
        super().__init__()
        self.fleet_count = {ship: 0 for ship in REBEL_SHIPS}
        self.fleet = self.set_fleet()

    def set_fleet(self):

        self.fleet = {"X-Wing": [XWing()for i in range(self.fleet_count["X-Wing"])],
                      "Y-Wing": [YWing() for i in range(self.fleet_count["Y-Wing"])],
                      "Rebel Transport": [RebelTransport()for i in range(self.fleet_count["Rebel Transport"])],
                      "Corellian Corvette": [CorellianCorvette() for i in range(self.fleet_count["Corellian Corvette"])],
                      "Mon Calamari Cruiser": [MonCalamariCruiser() for i in range(self.fleet_count["Mon Calamari Cruiser"])]}


class Army():
    def __init__(self):

        self.army_count = {unit: 0 for unit in ARMY}
        self.army = {unit: [unit() for i in range(self.army_count[unit])] for unit in ARMY}
        self.black_dice = self.get_black_dice()
        self.red_dice = self.get_red_dice()
        self.transport_restrictions = True
        self.can_retreat = True

    def get_black_dice(self):

        total_dice = sum(
            [sum([s.black_attack_value for s in self.army[k] if s.get_status()]) for k in self.army.keys()])
        if total_dice <= 5:
            return total_dice
        else:
            return 5

    def get_red_dice(self):

        total_dice = sum(
            [sum([s.red_attack_value for s in self.army[k] if s.get_status()]) for k in self.army.keys()])
        if total_dice <= 5:
            return total_dice
        else:
            return 5

    def transport(self):
        return sum([sum([s.transport for s in self.army[k] if s.get_status()]) for k in self.army.keys()])


class ImperialArmy(Army):
    def __init__(self):
        super().__init__()
        self.army_count = {unit: 0 for unit in IMPERIAL_ARMY}
        self.army = self.set_army()

    def set_army(self):
        self.army = {"Stormtrooper": [Stormtrooper() for i in range(self.army_count["Stormtrooper"])],
                     "AT-ST": [ATST() for i in range(self.army_count["AT-ST"])],
                     "AT-AT": [ATAT() for i in range(self.army_count["AT-AT"])]}


class RebelArmy(Army):
    def __init__(self):
        super().__init__()
        self.army_count = {unit: 0 for unit in REBEL_ARMY}
        self.army = self.set_army()

    def set_army(self):
        self.army = {"Rebel Trooper": [RebelTrooper() for i in range(self.army_count["Rebel Trooper"])],
                     "Airspeeder": [Airspeeder() for i in range(self.army_count["Airspeeder"])],
                     "Shield Generator": [ShieldGenerator() for i in range(self.army_count["Shield Generator"])],
                     "Ion Cannon": [IonCannon() for i in range(self.army_count["Ion Cannon"])]}


class Unit():
    health_color = None
    black_attack_value = 0
    red_attack_value = 0
    max_health = 0


    def __init__(self):
        self.current_health = self.max_health
        self.status = self.get_status()

    def get_max_health(self):
        return self.max_health

    def get_current_health(self):
        return self.current_health

    def get_health_color(self):
        return self.health_color

    def add_damage(self, damage):
        self.current_health += damage
        self.status = self.get_status()

    def get_status(self):
        if self.current_health > 0:
            return True
        else:
            return False


class TIE(Unit):

    health_color = "black"
    black_attack_value = 1
    red_attack_value = 0
    max_health = 1
    transport = -1

    def __init__(self):
        super().__init__()


class AssaultCarrier(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 1
    max_health = 2
    transport = 4

    def __init__(self):
        super().__init__()


class StarDestroyer(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 2
    max_health = 4
    transport = 6

    def __init__(self):
        super().__init__()


class SuperStarDestroyer(Unit):
    health_color = "red"
    black_attack_value = 2
    red_attack_value = 3
    max_health = 6
    transport = 8

    def __init__(self):
        super().__init__()


class DeathStar(Unit):
    health_color = "red"
    black_attack_value = 0
    red_attack_value = 4
    max_health = 0
    transport = 8

    def __init__(self):
        self.status = True
        super().__init__()

    def get_status(self):
        return self.status

    def destroy_ship(self):
        self.status = False

    def add_damage(self):
        pass


class XWing(Unit):
    health_color = "black"
    black_attack_value = 1
    red_attack_value = 0
    max_health = 1
    transport = 1


    def __init__(self):
        super().__init__()


class YWing(Unit):
    health_color = "black"
    black_attack_value = 0
    red_attack_value = 1
    max_health = 1
    transport = 1

    def __init__(self):
        super().__init__()


class RebelTransport(Unit):
    health_color = "red"
    black_attack_value = 0
    red_attack_value = 0
    max_health = 2
    transport = 4

    def __init__(self):
        super().__init__()


class CorellianCorvette(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 1
    max_health = 2
    transport = 2

    def __init__(self):
        super().__init__()


class MonCalamariCruiser(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 2
    max_health = 4
    transport = 6

    def __init__(self):
        super().__init__()


class Stormtrooper(Unit):
    health_color = "black"
    black_attack_value = 1
    red_attack_value = 0
    max_health = 1
    transport = -1

    def __init__(self):
        super().__init__()


class ATST(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 1
    max_health = 2
    transport = -1


    def __init__(self):
        super().__init__()


class ATAT(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 2
    max_health = 3
    transport = -1

    def __init__(self):
        super().__init__()


class RebelTrooper(Unit):
    health_color = "black"
    black_attack_value = 1
    red_attack_value = 0
    max_health = 1
    transport = -1

    def __init__(self):
        super().__init__()


class Airspeeder(Unit):
    health_color = "red"
    black_attack_value = 1
    red_attack_value = 1
    max_health = 2
    transport = -1

    def __init__(self):
        super().__init__()


class ShieldGenerator(Unit):
    health_color = "red"
    black_attack_value = 0
    red_attack_value = 0
    max_health = 3
    transport = 0

    def __init__(self):
        super().__init__()


class IonCannon(Unit):
    health_color = "red"
    black_attack_value = 0
    red_attack_value = 0
    max_health = 3
    transport = 0

    def __init__(self):
        super().__init__()

