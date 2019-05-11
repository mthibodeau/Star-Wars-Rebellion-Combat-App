import tkinter as tk
from tkinter import ttk, messagebox
import standard as std
import setup_gui as gui
from models import *
import random
from collections import Counter

def start_game():

    std.game = Game()

    std.imperial_player = Player(Imperial(), "No Leader", ImperialFleet(), ImperialArmy())
    std.rebel_player = Player(Rebel(), "No Leader", RebelFleet(), RebelArmy())

    std.imperial_player.set_opponent(std.rebel_player)
    std.rebel_player.set_opponent(std.imperial_player)


def assign_roles(controller, attacker, defender):

    std.imperial_player.leader = std.imperial_player.leader.get()
    std.rebel_player.leader = std.rebel_player.leader.get()

    std.game.attacker, std.game.defender = attacker, defender

    # Changes tkinter variables of user-generated unit counts to standard python variables
    for player in [std.rebel_player, std.imperial_player]:

        for unit in player.fleet.fleet_count:
            player.fleet.fleet_count[unit] = player.fleet.fleet_count[unit].get()

        for unit in player.army.army_count:
            player.army.army_count[unit] = player.army.army_count[unit].get()

        # Builds dictionary of newly instantiated ship objects based on unit counts
        # Can change this to simply build ship without storing as fleet_count?
        player.fleet.set_fleet()
        player.army.set_army()

        draw_hand(player)

    setup_combat(controller)


def setup_combat(controller):

    std.game.update_round()

    for player in [std.game.attacker, std.game.defender]:

        if std.game.round <= 2:
            player.red_roll, player.black_roll = roll(player.fleet)
        else:
            player.red_roll, player.black_roll = roll(player.army)
            if isinstance(player.fleet, RebelFleet) and std.game.round == 3:
                player.ground_hand.extend(draw_ground_card() for unit in player.army.army["Shield Generator"])

        print("red", player.red_roll)
        print("black", player.black_roll)

        player.roll = Counter(player.red_roll)
        player.roll.update(player.black_roll)

        print(player.roll)


        player.damage = 0
        player.can_block = False
        player.block = tk.IntVar()
        player.block.set(0)

    controller.create_frame(gui.AssignDamage)
    controller.show_frame(gui.AssignDamage)


def check_blocks(controller, assign_damage_window):

    # if std.game.defender.damage == 0:
    #     evaluate_combat(controller, 0)


    if std.game.round <= 2:

        if "Discard 1 space tactic card to block up to 2 damage" in std.game.defender.space_hand or\
            "Draw two tactics cards (either type) - dice" in std.game.defender.space_hand or\
            "Block 1 damage" in std.game.defender.space_hand:

            window, parent = assign_damage_window.create_window()
            parent.show_block_cards(window)

        else:
            evaluate_combat(controller, 0)

    elif std.game.round > 2:

        if "Discard 1 ground tactic card to block up to 2 damage" in std.game.defender.ground_hand or\
            "Draw two tactics cards (either type) - dice" in std.game.defender.ground_hand or\
            "Block 1 damage" in std.game.defender.ground_hand:

            window, parent = assign_damage_window.create_window()
            parent.show_block_cards(window)

        else:
            evaluate_combat(controller, 0)


def evaluate_combat(controller, blocks):

    # defender can block is true means already run through this function for block
    if blocks > 0 and not std.game.defender.can_block:
        std.game.defender.can_block = True
        std.game.defender.block.set(blocks)
        gui.block_message()
        roll_frame = gui.print_roll(std.game.defender, std.game.defender.frame)
        gui.reveal_block(roll_frame, std.game.defender, controller)

    elif std.game.round < 4:
        std.game.attacker, std.game.defender = std.game.defender, std.game.attacker
        setup_combat(controller)

    else:
        std.game.update_round()
        std.game.attacker, std.game.defender = std.game.defender, std.game.attacker

        controller.create_frame(gui.Retreat)
        controller.show_frame(gui.Retreat)


def play_card(controller, card, card_button):
    # CARD_EFFECTS = {"Deal 1 damage": increase_direct_hits(), "Block 1 damage": increase_blocks(),
    #                 "Reroll up to 2 dice": reroll(2)}

    player = std.game.attacker

    if std.game.round <= 2:
        hand = player.space_hand
    else:
        hand = player.ground_hand

    if card in std.CARD_DISCARDS:
        if len(player.hand) == 1:
            gui.no_discard_message()
            return

        window, parent = controller.create_window()
        parent.cards_to_discard(window, card_button)

        # recreate block window without played card
        window, parent = controller.create_window()
        parent.show_block_cards(window)


    elif card in CARD_DICE:
        if player.used_roll["Cards"].get() <= 0:
            gui.no_card_die_message()
            return

        assign_die("Cards", player)

        if card == "Draw two tactics cards (either type) - dice":
            window, parent = controller.create_window()
            parent.ask_card_type(window)
            gui.disable_card_button(card_button)
            discard(hand, card)

        if card in ["Deal 1 damage to 2 ships - dice", "Deal 1 damage to 2 ground units - dice"]:
            std.game.play_special_damage_card(card)
            gui.disable_card_button(card_button)
            discard(hand, card)

        if card in ["Deal 2 damage to 1 ship - dice", "Deal 2 damage to 1 ground unit - dice"]:
            std.game.play_special_damage_card(card)
            gui.disable_card_button(card_button)
            discard(hand, card)

        if card == "Deal damage equal to red attack value of one ship - dice":
            play_card_bombardment()
            gui.disable_card_button(card_button)
            discard(hand, card)

    elif card == "Block 1 damage":
        increase_blocks(1)
        gui.disable_card_button(card_button)
        if std.game.round <= 2:
            hand = std.game.defender.space_hand
        else:
            hand = std.game.defender.ground_hand
        discard(hand, card)

    elif card == "Deal 1 damage":
        increase_direct_hits()
        discard(hand, card)
        gui.disable_card_button(card_button)

    elif card == "Reroll up to 2 dice":
        reroll(controller)
        discard(hand, card)
        gui.disable_card_button(card_button)

    elif card == "Opponent cannot retreat this round":
        std.game.defender.army.can_retreat = False
        gui.disable_card_button(card_button)

    elif card == "Ignore transport restrictions for retreat this round":
        std.game.attacker.army.transport_restrictions = False
        gui.disable_card_button(card_button)


    # if card in player.space_hand: player.space_hand.remove(card)
    # if card in player.ground_hand: player.ground_hand.remove(card)


def discard(hand, card):
    hand.remove(card)


def play_card_bombardment():
    player = std.game.attacker
    ships = [category for category in player.fleet.fleet.keys() if len(player.fleet.fleet[category]) > 0]

    if "Death Star" in ships:
        red = 4
    elif "Super Star Destroyer in Ships":
        red = 3
    elif "Star Destroyer" in ships or "Mon Calamari Cruiser" in ships:
        red = 2
    elif "Assault Carrier" in ships or "Corellian Corvette" in ships or "Y-Wing" in ships:
        red = 1
    else:
        return

    for i in range(red):
        increase_direct_hits()


def increase_direct_hits():
    player = std.game.attacker
    if std.game.round <= 2:
        player.roll["Direct Hits"] += 1
        temp = player.used_roll["Direct Hits"][0].get()
        player.used_roll["Direct Hits"][0].set(temp + 1)

    else:
        player.roll["Direct Hits"] += 1
        temp = player.used_roll["Direct Hits"][0].get()
        player.used_roll["Direct Hits"][0].set(temp + 1)


def reroll(controller):
    player = std.game.attacker
    print("reroll - not working")


    window, parent = controller.create_window()
    parent.reroll_dice(window)


def increase_blocks(blocks=1):
    if std.game.round <= 2:
        std.game.defender.space_blocks += blocks
    else:
        std.game.defender.ground_blocks += blocks


def retreat(controller):

    if std.game.round == 5:
        player = std.game.attacker
    else:
        player = std.game.defender

    if player.army.can_retreat:

        if not player.army.transport_restrictions:
            gui.retreat_success_message()

        elif player.fleet.can_transport() + player.army.transport() >=0:
            gui.retreat_success_message()

        else:
            gui.retreat_fail_message(player.fleet.can_transport() + player.army.transport())
    else:
        gui.retreat_fail_message("{} cannot retreat this round.".format(player))

    controller.create_frame(gui.Final)
    controller.show_frame(gui.Final)


def continue_battle(controller, player):

    if std.game.round == 5:
        std.game.update_round()
        controller.create_frame(gui.Retreat)
        controller.show_frame(gui.Retreat)

    else:
        new_combat(controller)


def new_combat(controller):
    std.game.round = 0

    for player in [std.imperial_player, std.rebel_player]:

        player.army.can_retreat = True
        player.army.transport_restrictions = True

        for k, v in player.fleet.fleet.items():
            player.fleet.fleet[k] = [ship for ship in v if ship.get_status()]

        for k, v in player.army.army.items():
            player.army.army[k] = [unit for unit in v if unit.get_status()]

    setup_combat(controller)


def end_block_damage(controller):

    std.game.attacker, std.game.defender = std.game.defender, std.game.attacker

    if std.game.round < 4:
        setup_combat(controller)
    else:
        std.game.update_round()
        controller.create_frame(gui.Retreat)
        controller.show_frame(gui.Retreat)


def draw_hand(player):

    if LEADER_VALUE[player.leader][0] > 0:
        count = 1
        card = draw_space_card()
        while card is not None and LEADER_VALUE[player.leader][0] >= count:
            player.space_hand.append(card)
            card = draw_space_card()
            count += 1

    if LEADER_VALUE[player.leader][1] > 0:
        count = 1
        card = draw_ground_card()
        while card is not None and LEADER_VALUE[player.leader][1] >= count:
            player.ground_hand.append(card)
            card = draw_ground_card()
            count += 1


def draw_space_card():

    try:
        drawn = random.choice(std.game.space_deck)
        std.game.space_deck.remove(drawn)
        return drawn
    except IndexError:
        gui.end_of_deck_message()
        return None


def draw_ground_card():
    try:
        drawn = random.choice(std.game.ground_deck)
        std.game.ground_deck.remove(drawn)
        return drawn
    except IndexError:
        gui.end_of_deck_message()
        return None


def roll(force):
    """
    2/6 - blank
    2/6 - regular hit
    1/6 - direct hit
    1/6 - draw/play card
    """

    black = force.get_black_dice()
    red = force.get_red_dice()

    if std.game.round <= 2 and isinstance(force, ImperialFleet):
        red -= (len(std.rebel_player.army.army["Ion Cannon"]) * 2)

    black_results = {'Black Hits': 0, 'Direct Hits': 0, 'Cards': 0, 'Miss': 0}

    red_results = {'Red Hits': 0, 'Direct Hits': 0, 'Cards': 0, 'Miss': 0}

    for i in range(black):
        black_results[roll_black_dice()] += 1

    for i in range(red):
        red_results[roll_red_dice()] += 1

    return (red_results, black_results)


def roll_red_dice():
    return random.choice(["Miss", "Miss", "Red Hits", "Red Hits", "Direct Hits", "Cards"])


def roll_black_dice():
    return random.choice(["Miss", "Miss", "Black Hits", "Black Hits", "Direct Hits", "Cards"])


def check_roll(result, player):
    if player.used_roll[result].get() > 0 or player.used_roll["Direct Hits"][0].get() > 0:
        return True
    else:
        return False


def assign_die(result, player, ship=None):

    if player.used_roll[result].get() > 0:
        temp = player.used_roll[result].get()
        player.used_roll[result].set(temp - 1)

        if result == "Cards" and player.used_roll[result].get() <= 0:
            gui.disable_card_button(std.game.draw_card)

    else:
        temp = player.used_roll["Direct Hits"][0].get()
        player.used_roll["Direct Hits"][0].set(temp - 1)
        player.used_roll["Direct Hits"][1].append(result)

    if ship != None:
        increase_damage(ship)
        std.game.defender.damage += 1


def unassign_die(result, player, ship):
    if result in player.used_roll["Direct Hits"][1]:
        temp = player.used_roll["Direct Hits"][0].get()
        player.used_roll["Direct Hits"][0].set(temp + 1)
        player.used_roll["Direct Hits"][1].remove(result)
    else:
        temp = player.used_roll[result].get()
        player.used_roll[result].set(temp + 1)
    decrease_damage(ship)
    std.game.defender.damage -= 1


def block_damage(defender, ship):
    temp = defender.block.get()
    defender.block.set(temp-1)
    decrease_damage(ship)


def unblock_damage(defender, ship):
    temp = defender.block.get()
    defender.block.set(temp+1)
    increase_damage(ship)
    if std.game.round <= 2:
        defender.space_hand.append("Block 1 damage")
    else:
        defender.ground_hand.append("Block 1 damage")


def increase_damage(ship):
    ship.add_damage(-1)


def decrease_damage(ship):
    ship.add_damage(1)


def main():
    start_game()

    app = gui.GUI()
    app.mainloop()

if __name__ == '__main__':
    main()

