import tkinter as tk
from tkinter import ttk, messagebox
import standard as std
import play as swr


class GUI(tk.Tk):
    """
    Base set-up for windows/frames in SW_rebellion_combat
    """

    def __init__(self):
        tk.Tk.__init__(self)

        tk.Tk.wm_title(self, "Star Wars Rebellion Combat")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.create_frame(Setup)
        self.show_frame(Setup)

    def create_frame(self, f):

        frame = f(self.container, self)
        self.frames[f] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    # controller is the GUI class object containing the frames and show_frame function
    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class Setup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.initialize()

    def initialize(self):
        heading = ttk.Label(self, text="Setup")
        heading.grid(row=0, columnspan=2)

        std.game.frame = self.parent

        self.setup_unit_entry()

    def setup_unit_entry(self):

        imp_frame = ttk.LabelFrame(self, text="Imperial Forces", labelanchor="nw")
        imp_frame.grid(row=1, column=0)

        reb_frame = ttk.LabelFrame(self, text="Rebel Forces", labelanchor="nw")
        reb_frame.grid(row=1, column=1)

        for i, player in enumerate([std.imperial_player, std.rebel_player]):
            if i == 0:
                frame = imp_frame
            else:
                frame = reb_frame

            player.leader = tk.StringVar()
            leader_options = ttk.OptionMenu(frame, player.leader, *player.side.leaders)
            leader_options.grid(row=0, column=0)

            space_forces_label = tk.Label(frame, text="Space Forces")
            space_forces_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            self.print_unit_entry(frame, player.fleet.fleet_count, player.side.ships, 2)

            ground_forces_label = tk.Label(frame, text="Ground Forces")
            ground_forces_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

            self.print_unit_entry(frame, player.army.army_count, player.side.army, 8)

        # Blank line to parallel Rebel Force lines
        blank = ttk.Label(imp_frame, text="")
        blank.grid(row=11, column=1, columnspan=2)

        # # Basic Commands for Program
        imp_attack = ttk.Button(self, text="Imperials Attack!", command=lambda: swr.assign_roles(self.controller, std.imperial_player, std.rebel_player))
        imp_attack.grid(row=10, column=0)

        rebel_attack = ttk.Button(self, text="Rebels Attack!", command=lambda: swr.assign_roles(self.controller, std.rebel_player, std.imperial_player))
        rebel_attack.grid(row=10, column=1)

    def print_unit_entry(self, frame, force_count, force, row):
        for i, unit in enumerate(force):
            force_count[unit] = tk.IntVar()
            force_count[unit].set(0)
            unit_label = tk.Label(frame, text=unit)
            unit_label.grid(row=i + row, column=0)

            entry = ttk.Entry(frame, width=3, textvariable=force_count[unit])
            inc = ttk.Button(frame, text=" + ", width=3, command=lambda entry=entry: self.increase_count(entry))
            dec = ttk.Button(frame, text=" - ", width=3, command=lambda entry=entry: self.decrease_count(entry))

            inc.grid(row=i + row, column=1)
            entry.grid(row=i + row, column=2)
            dec.grid(row=i + row, column=3)

    def increase_count(self, e):
        count = int(e.get())
        e.delete(0, tk.END)
        e.insert(0, str(count+1))

    def decrease_count(self, e):
        count = int(e.get())
        e.delete(0, tk.END)
        e.insert(0, str(count-1))


class AssignDamage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller
        self.click = 0

        self.imp_frame = None
        self.reb_frame = None

        self.initialize()


    def initialize(self):
        heading = ttk.Label(self, text="Assign Damage")
        heading.grid(row=0, columnspan=4)

        self.imp_frame, self.reb_frame = build_frames(self)
        self.imp_frame.grid(row=1, column=0, columnspan=2, sticky="n")
        self.reb_frame.grid(row=1, column=2, columnspan=2, sticky="n")

        for i, player in enumerate([std.imperial_player, std.rebel_player]):
            if i == 0:
                frame = self.imp_frame
            else:
                frame = self.reb_frame

            print_roll(player, frame)

            if player == std.game.attacker:
                show_cards(player, frame, self.controller, self)

            else:
                show_defender_forces(player, frame)

    def create_window(self):
        window = tk.Toplevel(width=300, height=300)
        return (window, self)

    def show_block_cards(self, window):

        if std.game.round <= 2:
            hand = std.game.defender.space_hand
        else:
            hand = std.game.defender.ground_hand

        message = "{} may play cards to block damage".format(std.game.defender)
        label = ttk.Label(window, text=message, pad=10)
        label.grid(row=0, column=0, columnspan=2)


        frame = ttk.LabelFrame(window, text="Cards")
        frame.grid(row=1, column=0)

        count = 1

        for i, card in enumerate(sorted(hand)):
            b = ttk.Button(frame, text=card, pad=5)
            b.config(command=lambda c=(card, b): __play_block(self, window, c[0], c[1]))
            b.grid(row=i, column=0, sticky="w")

            if card not in ["Block 1 damage", "Discard 1 space tactic card to block up to 2 damage",
                            "Discard 1 ground tactic card to block up to 2 damage"]:
                disable_card_button(b)

            count = i

        done = ttk.Button(frame, text="Done", pad=5, command=lambda: __done_blocks())
        done.grid(row=count + 1)

        def __play_block(self, w, card, button):
            if card != "Block 1 damage":
                w.destroy()
            swr.play_card(self, card, button)

        def __done_blocks():
            window.destroy()
            if std.game.round <= 2:
                blocks = std.game.defender.space_blocks
            else:
                blocks = std.game.defender.ground_blocks

            swr.evaluate_combat(self.controller, blocks)

    def ask_card_type(self, window):

        heading = ttk.Label(window, text="Draw a space tactic card or a ground tactic card.", pad=10)
        heading.grid(row=0, column=0, columnspan=2)

        ttk.Button(window, text="Space Deck", pad=10, command=lambda: __click_card_draw(swr.draw_space_card,  std.game.attacker.space_hand, window)).grid(row=1, column=0)
        ttk.Button(window, text="Ground Deck", pad=10, command=lambda: __click_card_draw(swr.draw_ground_card,  std.game.attacker.ground_hand, window)).grid(row=1, column=1)

        def __click_card_draw(deck, hand, window):
            draw = deck()
            if draw is not None:
                hand.append(draw)
                self.click += 1
                if self.click == 2:
                    window.destroy()

                    show_cards(std.game.attacker, std.game.attacker.frame, self.controller, self)

    def reroll_dice(self, window):

        self.click = 0

        heading = ttk.Label(window, text="Reroll up to 2 dice", pad=10)
        heading.grid(row=0, column=0, columnspan=2)

        roll = std.game.attacker.used_roll

        for category, dice in std.game.attacker.red_roll.items():
            if category == "Direct Hits":
                if dice != 0:
                    for i in range(roll[category][0].get()):
                        ttk.Button(window, text=category, pad=10, command=lambda: __click_card_draw(category, window)).grid(row=1, column=i)

            elif dice != 0 :
                for i in range(roll[category].get()):
                    ttk.Button(window, text=category, pad=10, command=lambda: __click_card_draw(category, window)).grid(row=2, column=i)



        def __click_card_draw(category, window):
            self.click += 1
            if self.click == 2:
                window.destroy()

    def cards_to_discard(self, window, button):

        if std.game.round <= 2:
            hand = std.game.defender.space_hand
        else:
            hand = std.game.defender.ground_hand

        heading = ttk.Label(window, text="Choose a card to discard:", pad=10)
        heading.grid(row=0, column=0, columnspan=2)

        frame = ttk.LabelFrame(window, text="Cards")
        frame.grid(row=1, column=0)

        count = 1
        discard_count = True

        for i, card in enumerate(sorted(hand)):
            b = ttk.Button(frame, text=card, pad=5)
            b.config(command=lambda c=(card, hand): __confirm_discard(c[0], c[1]))
            b.grid(row=i, column=0, sticky="w")
            count = i

            if discard_count and card in ["Discard 1 space tactic card to block up to 2 damage", "Discard 1 ground tactic card to block up to 2 damage"]:
                disable_card_button(b)
                discard_count = False

        b = ttk.Button(frame, text="Go Back", pad=5, command=lambda: window.destroy())
        b.grid(row=count+1)

        def __confirm_discard(discard, hand):
            if __confirm_discard_message(discard):
                swr.increase_blocks(2)
                swr.discard(hand, discard)

                if std.game.round <= 2:
                    swr.discard(hand, "Discard 1 space tactic card to block up to 2 damage")
                else:
                    swr.discard(hand, "Discard 1 ground tactic card to block up to 2 damage")

                window.destroy()

                # recreate block window without played card

                new_window, parent = self.create_window()
                parent.show_block_cards(new_window)


        def __confirm_discard_message(discard):
            message = "Discard: " + discard + "?"
            return messagebox.askyesno("Discard?", message=message)


class Retreat(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.initialize()

    def initialize(self):
        heading = ttk.Label(self, text="Surviving Forces")
        heading.grid(row=0, columnspan=4)

        imp_frame, reb_frame = build_frames(self)
        imp_frame.grid(row=1, column=0, columnspan=2)
        reb_frame.grid(row=1, column=2, columnspan=2)

        for i, player in enumerate([std.imperial_player, std.rebel_player]):
            if i == 0:
                frame = imp_frame
                op_frame = reb_frame
            else:
                frame = reb_frame
                op_frame = imp_frame

            if (player == std.game.attacker and std.game.round == 5) or (player == std.game.defender and std.game.round == 6):
                ttk.Button(frame, text="Retreat?", pad=20, command=lambda: swr.retreat(self.controller)).grid(row=1, column=0)
                ttk.Button(frame, text="Continue Battle?", pad=20, command=lambda: swr.continue_battle(self.controller, player)).grid(row=1, column=1)

            else:
                ttk.Label(frame, text="", pad=20).grid(row=1, column=1)

            canvas = tk.Canvas(frame, width=500, height=600)
            canvas.grid(row=2, column=0, columnspan=2)

            draw_forces(canvas, player, player.fleet.fleet)
            draw_forces(canvas, player, player.army.army)


class Final(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.initialize()

    def initialize(self):
        heading = ttk.Label(self, text="Final Outcome")
        heading.grid(row=0, columnspan=4)

        imp_frame, reb_frame = build_frames(self)
        imp_frame.grid(row=1, column=0, columnspan=2)
        reb_frame.grid(row=1, column=2, columnspan=2)

        for i, player in enumerate([std.imperial_player, std.rebel_player]):
            if i == 0:
                frame = imp_frame
                op_frame = reb_frame
            else:
                frame = reb_frame
                op_frame = imp_frame

            canvas = tk.Canvas(frame, width=500, height=600)
            canvas.grid(row=2, column=0, columnspan=2)

            draw_forces(canvas, player, player.fleet.fleet)
            draw_forces(canvas, player, player.army.army)


def show_defender_forces(player, frame):

    canvas = tk.Canvas(frame, width=425, height=450)
    canvas.grid(row=4, column=0, columnspan=6)

    if std.game.round <= 2:
        force = player.fleet.fleet
    else:
        force = player.army.army

    draw_forces(canvas, player, force)

    std.game.defender.frame = frame


def show_cards(player, frame, controller, assign_damage_window):

    if std.game.round <= 2:
        hand = player.space_hand
    else:
        hand = player.ground_hand

    cards = ttk.LabelFrame(frame, text="Cards", labelanchor="nw")
    cards.grid(row=3, column=0, columnspan=6, sticky="w")
    cards.columnconfigure(0, minsize=450)
    cards.rowconfigure(0, minsize=15)

    for i, card in enumerate(sorted(hand)):

        b = ttk.Button(cards, text=card, pad=5)
        b.config(command= lambda c=(card, b): swr.play_card(assign_damage_window, c[0], c[1]))
        b.grid(row=i, column=0, sticky="w")

        if card in std.CARD_BLOCK:
            disable_card_button(b)

    if not std.game.defender.can_block:
        attack = ttk.Button(frame, text="Assign Damage", pad=20, command=lambda: swr.check_blocks(controller, assign_damage_window))
        attack.grid(row=5, column=0, rowspan=5)

        if std.game.round <=2:
            std.game.draw_card = ttk.Button(frame, text="Draw Space Tactic Card", pad=20, command=lambda: __draw_card_dice(swr.draw_space_card, player.space_hand))
        else:
            std.game.draw_card = ttk.Button(frame, text="Draw Ground Tactic Card", pad=20, command=lambda: __draw_card_dice(swr.draw_ground_card, player.ground_hand))

        std.game.draw_card.grid(row=5, column=1, rowspan=5)

        def check_draw_card():
            if player.used_roll["Cards"].get() <= 0:
                disable_card_button(std.game.draw_card)

        def __draw_card_dice(deck, h):
            draw = deck()
            if draw is not None:
                h.append(draw)
            temp = player.used_roll["Cards"].get()
            player.used_roll["Cards"].set(temp-1)

            check_draw_card()

            for widget in cards.winfo_children():
                widget.destroy()

            show_cards(std.game.attacker, std.game.attacker.frame, controller, assign_damage_window)

        check_draw_card()

def disable_card_button(b):
    b.config(state=tk.DISABLED)


def build_frames(controller):
    """
    :param controller: Frame for where to build sub-LabelFrames to hold each sides widgets
    :returns: A tuple containing the LabelFrame in the form (imperial_frame, rebel_frame)
    """
    imp_frame = ttk.LabelFrame(controller, text="Imperial Forces", labelanchor="nw")

    reb_frame = ttk.LabelFrame(controller, text="Rebel Forces", labelanchor="nw")

    std.imperial_player.frame = imp_frame
    std.rebel_player.frame = reb_frame

    return imp_frame, reb_frame


def print_roll(player, f):

    # Auto Updating Roll Results

    frame = ttk.LabelFrame(f, text="Roll", labelanchor="nw")
    frame.grid(row=1, column=0, columnspan=2)

    for i, r in enumerate(std.DICE):
        ttk.Label(frame, text=r).grid(row=0, column=i)
        ttk.Label(frame, text="--").grid(row=1, column=i)
        frame.columnconfigure(i, minsize=75)

    ttk.Label(frame, text="Block").grid(row=0, column=5, sticky="n")
    ttk.Label(frame, text="--").grid(row=1, column=5)
    frame.columnconfigure(5, minsize=75)

    if player is std.game.attacker:
        reveal_roll(player, frame)

    else:
        return frame


def reveal_roll(attacker, frame):

    for i, r in enumerate(std.DICE):
        if r == "Direct Hits":
            attacker.used_roll[r][0] = tk.IntVar()
            attacker.used_roll[r][0].set(attacker.roll[r])
            ttk.Label(frame, textvariable=attacker.used_roll[r][0]).grid(row=1, column=i)
        else:
            attacker.used_roll[r] = tk.IntVar()
            attacker.used_roll[r].set(attacker.roll[r])
            ttk.Label(frame, textvariable=attacker.used_roll[r]).grid(row=1, column=i)


def draw_death_star(canvas, num, y):
    x = 20

    for deathstar in range(num):
        canvas.create_oval(x, y, x + 60, y + 60, fill="black")
        x += 70
        # deathstar = tk.PhotoImage(file="deathstar_50px.gif")
        # canvas.create_image(x, y, image=deathstar, anchor="nw")
        # canvas.tag_bind(deathstar, "<Button-1>", ship_tagger)

    y += 70

    return y


def draw_unit_health(canvas, unit, x, y):
    if std.game.round <= 4:
        box_size = 30
    else:
        box_size = 20

    for i in range(unit.max_health):

        health_box = canvas.create_rectangle(x, y, x + box_size, y + box_size, width=2,
                                             tags=[unit.health_color, unit])

        if i >= unit.get_current_health():
            canvas.addtag("hit", "withtag", health_box)
            canvas.addtag("grey", "withtag", health_box)
        else:
            canvas.itemconfigure(health_box, fill=unit.health_color)

        x += box_size

    return x + 5


def draw_unit_container(canvas, unit, x, y):
    if std.game.round <= 4:
        box_size = 30
    else:
        box_size = 20

    canvas.create_rectangle(x - 4, y - 4, x + 3 + (box_size * unit.max_health),
                            y + box_size + 3)


def draw_forces(canvas, player, force):
    x = 10
    y = 10

    # Increase to show both space and ground forces at end of combat
    if force == player.fleet.fleet:
        inventory = std.SHIPS

    else:
        inventory = std.ARMY
        if std.game.round > 4:
            y = 300
            canvas.create_text(x, y, anchor="nw", text="Ground Forces")
            y = 320

    for category in inventory:
        if category in force and len(force[category]) > 0:
            canvas.create_text(x, y, anchor="nw", text=category)
            x += 10
            y += 25

            if category == "Death Star":
                y = draw_death_star(canvas, len(force[category]), y)

            else:
                for unit in force[category]:
                    # start next ship visual on new line if too long
                    if (x > 400 and unit.max_health > 1) or (unit.max_health == 1 and x > 460):
                        y += 50
                        x = 20

                    draw_unit_container(canvas, unit, x, y)
                    x = draw_unit_health(canvas, unit, x, y)

                    x += 15

                    def ship_tagger(event, unit=unit, canvas=canvas, player=player):
                        return view_damage(event, unit, canvas, player)

                    # click event to assign damage to specific ship
                    canvas.tag_bind(unit, "<Button-1>", ship_tagger)

                x = 10
                if std.game.round <= 4:
                    y += 50
                else:
                    y += 25


def view_damage(event, ship, canvas, defender):

    if defender == std.game.attacker:
        return

    attacker = std.game.attacker

    h = event.widget.find_closest(event.x, event.y)

    def __remove_damage_fill():

        canvas.dtag(h, "damage")

        if ship.max_health > 1:
            canvas.itemconfigure(h, fill="red")
        else:
            canvas.itemconfigure(h, fill="black")

    def __add_damage_fill(h=h):

        canvas.addtag("damage", "withtag", h)

        if ship.max_health > 1:
            canvas.itemconfigure(h, fill="red4")
        else:
            canvas.itemconfigure(h, fill="grey40")

    if std.game.two_damage_one_ship:

        __add_damage_fill()

        second_hit = event.widget.find_closest(event.x+30, event.y)

        __add_damage_fill(second_hit)

        canvas.addtag("card", "withtag", h)
        canvas.addtag("card", "withtag", second_hit)

        std.game.two_damage_one_ship = False

        return

    if "damage" in canvas.gettags(h):
        if "red" in canvas.gettags(h):
            if not defender.can_block and "card" not in canvas.gettags(h):
                swr.unassign_die("Red Hits", attacker, ship)
                __remove_damage_fill()
            elif defender.block.get() > 0:
                swr.block_damage(defender, ship)
                canvas.addtag("blocked", "withtag", h)
                __remove_damage_fill()

        else:
            if not defender.can_block:
                swr.unassign_die("Black Hits", attacker, ship)
                __remove_damage_fill()
            elif defender.block.get() > 0:
                swr.block_damage(defender, ship)
                canvas.addtag("blocked", "withtag", h)
                __remove_damage_fill()

    elif std.game.one_damage_two_ships:
        if std.game.one_damage_two_ships_check(ship):
            __add_damage_fill()
            canvas.addtag("card", "withtag", h)

    elif "blocked" in canvas.gettags(h):
        __add_damage_fill()
        swr.unblock_damage(defender, ship)
        canvas.dtag(h, "blocked")

    elif "red" in canvas.gettags(h) and swr.check_roll("Red Hits", attacker) and not defender.can_block:
        __add_damage_fill()
        swr.assign_die("Red Hits", attacker, ship)

    elif "black" in canvas.gettags(h) and swr.check_roll("Black Hits", attacker) and not defender.can_block:
        __add_damage_fill()
        swr.assign_die("Black Hits", attacker, ship)


def reveal_block(frame, defender, controller):

    block = ttk.Button(frame, text="Block Damage", pad=20, command=lambda: swr.end_block_damage(controller))
    block.grid(row=5, column=0, columnspan=6, rowspan=5)

    # defender.block.set(blocks)
    b = ttk.Label(frame, textvariable=defender.block)
    b.grid(row=2, column=5)


def block_message():
    message = "{} can block {} damage.".format(std.game.defender, std.game.defender.block.get())
    return messagebox.showinfo("Block", message=message)


def retreat_success_message():
    message = "You successfully retreat with all units!"
    return messagebox.showinfo("Retreat Success!", message=message)


def retreat_fail_message(units):
    try:
        message = "You cannot retreat with all units. You must leave {} behind.".format(abs(units))
        return messagebox.showerror("Not enough transportation space", message=message)
    except:
        message = units
        return messagebox.showerror("Tactic Card", message=message)


def end_of_deck_message():
    message = "All cards have been drawn from this deck."
    return messagebox.showinfo("No more cards", message=message)


def no_card_die_message():
    return messagebox.showerror("Need Cards die", message="You need a Card die roll to play this.")


def no_discard_message():
    return messagebox.showerror("Discard Error", message="You need a card to discard to play this.")
