
LEADER_VALUE = {"No Leader": (0, 0), "Darth Vader": (2, 3), "Emperor Palpatine": (3, 2), "Grand Moff Tarkin": (2, 1),
                 "Gen. Tagge": (1, 2), "Col. Yularen": (2, 2), "Admiral Ozzel": (2, 1), "Admiral Piett": (3, 1),
                 "Gen. Veers": (1, 3), "Soontir Fel": (2, 1), "Moff Jerjerrod": (1, 1), "Boba Fett": (0, 0),
                 "Janus Greejatus": (0, 0), "Princess Leia": (1, 1), "Jan Dodonna": (2, 1), "Gen. Rieekan": (1, 2),
                 "Han Solo": (2, 2), "Admiral Ackbar": (3, 1), "Lando Calrissian": (2, 2), "Luke Skywalker": (2, 2),
                 "Luke Skywalker (Jedi)": (3, 3), "Obi-Wan Kenobi": (1, 3), "Wedge Antilles": (3, 1), "Gen. Madine": (1, 3),
                 "Chewbacca": (1, 2), "Mon Mothma": (0, 0)}

IMPERIAL_LEADERS = ["No Leader", "Darth Vader", "Emperor Palpatine", "Grand Moff Tarkin", "Gen. Tagge", "Col. Yularen",
                    "Admiral Ozzel", "Admiral Piett", "Gen. Veers", "Soontir Fel", "Moff Jerjerrod", "Boba Fett", "Janus Greejatus"]

REBEL_LEADERS = ["No Leader", "Princess Leia", "Jan Dodonna", "Gen. Rieekan", "Han Solo", "Admiral Ackbar", "Lando Calrissian",
                 "Luke Skywalker", "Luke Skywalker (Jedi)", "Obi-Wan Kenobi", "Wedge Antilles", "Gen. Madine", "Chewbacca",
                 "Mon Mothma"]

SHIPS = ["TIE", "Assault Carrier", "Star Destroyer", "Super Star Destroyer", "Death Star", "X-Wing", "Y-Wing",
         "Rebel Transport", "Corellian Corvette", "Mon Calamari Cruiser"]

ARMY = ["Stormtrooper", "AT-ST", "AT-AT", "Rebel Trooper", "Airspeeder", "Shield Generator", "Ion Cannon"]

IMPERIAL_SHIPS = ["TIE", "Assault Carrier", "Star Destroyer", "Super Star Destroyer", "Death Star"]

IMPERIAL_ARMY = ["Stormtrooper", "AT-ST", "AT-AT"]

REBEL_SHIPS = ["X-Wing", "Y-Wing", "Rebel Transport", "Corellian Corvette", "Mon Calamari Cruiser"]

REBEL_ARMY = ["Rebel Trooper", "Airspeeder", "Shield Generator", "Ion Cannon"]


DICE = ["Direct Hits", "Red Hits", "Black Hits", "Miss", "Cards"]

SPACE_TACTIC_CARDS = ["Deal 1 damage", "Deal 1 damage", "Reroll up to 2 dice", "Reroll up to 2 dice", "Block 1 damage",
                      "Block 1 damage", "Block 1 damage", "Discard 1 space tactic card to block up to 2 damage",
                      "Discard 1 space tactic card to block up to 2 damage", "Deal 2 damage to 1 ship - dice",
                      "Deal 2 damage to 1 ship - dice", "Deal 1 damage to 2 ships - dice", "Deal 1 damage to 2 ships - dice",
                      "Draw two tactics cards (either type) - dice", "Opponent cannot retreat this round"]

GROUND_TACTICS_CARDS = ["Deal 1 damage", "Deal 1 damage", "Reroll up to 2 dice", "Reroll up to 2 dice", "Block 1 damage",
                       "Block 1 damage", "Block 1 damage", "Discard 1 ground tactic card to block up to 2 damage",
                       "Discard 1 ground tactic card to block up to 2 damage", "Deal 2 damage to 1 ground unit - dice",
                       "Deal 1 damage to 2 ground units - dice", "Opponent cannot block damage during this ground battle round - dice",
                       "Draw two tactics cards (either type) - dice", "Deal damage equal to red attack value of one ship - dice",
                        "Ignore transport restrictions for retreat this round"]


CARD_DISCARDS = ["Discard 1 space tactic card to block up to 2 damage", "Discard 1 ground tactic card to block up to 2 damage"]

CARD_DICE = ["Deal 2 damage to 1 ship - dice", "Deal 1 damage to 2 ships - dice", "Draw two tactics cards (either type) - dice",
             "Deal 2 damage to 1 ground unit - dice", "Deal 1 damage to 2 ground units - dice",
             "Opponent cannot block damage during this ground battle round - dice", "Deal damage equal to red attack value of one ship - dice"]

CARD_BLOCK = ["Block 1 damage", "Discard 1 space tactic card to block up to 2 damage", "Discard 1 ground tactic card to block up to 2 damage"]

game = None
combat = None
round = None

imperial_player = None
rebel_player = None

