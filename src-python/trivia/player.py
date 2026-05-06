BOARD_SIZE = 12
WINNING_COINS = 6
#Yahir Hernandez

class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 1
        self.coins = 0
        self.in_penalty_box = False