from collections import deque
from trivia.player import Player
# Yahir Hernandez
BOARD_SIZE = 12
WINNING_COINS = 6
QUESTIONS_PER_CATEGORY = 50
MAX_PLAYERS = 6

# REFACTOR ME
class Game:
    def __init__(self):
        self.players = []

        self.pop_questions = deque()
        self.science_questions = deque()
        self.sports_questions = deque()
        self.rock_questions = deque()

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(QUESTIONS_PER_CATEGORY):
            self.pop_questions.append(f"Pop Question {i}")
            self.science_questions.append(f"Science Question {i}")
            self.sports_questions.append(f"Sports Question {i}")
            self.rock_questions.append(self.create_rock_question(i))

    def create_rock_question(self, index):
        return f"Rock Question {index}"

    def has_enough_players(self):
        return self.how_many_players() >= 2

    def add(self, player_name):
        player = Player(player_name)
        self.players.append(player)
        print(f"{player_name} was added")
        print(f"They are player number {len(self.players)}")
        return True

    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        print(f"{self.players[self.current_player].name} is the current player")
        print(f"They have rolled a {roll}")

        if self.players[self.current_player].in_penalty_box:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print(f"{self.players[self.current_player].name} is getting out of the penalty box")
                player = self.players[self.current_player]
                player.advance(roll)

                print(f"{self.players[self.current_player].name}'s new location is {self.players[self.current_player].position}")
                print(f"The category is {self._current_category()}")
                self._ask_question()
            else:
                print(f"{self.players[self.current_player].name} is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            player = self.players[self.current_player]
            player.advance(roll)        

            print(f"{self.players[self.current_player].name}'s new location is {self.players[self.current_player].position}")
            print(f"The category is {self._current_category()}")
            self._ask_question()

    def _ask_question(self):
        category = self._current_category()
        if category == "Pop":
            print(self.pop_questions.popleft())
        if category == "Science":
            print(self.science_questions.popleft())
        if category == "Sports":
            print(self.sports_questions.popleft())
        if category == "Rock":
            print(self.rock_questions.popleft())

    def _current_category(self):
        pos = self.players[self.current_player].position - 1
        if pos in (0, 4, 8):
            return "Pop"
        if pos in (1, 5, 9):
            return "Science"
        if pos in (2, 6, 10):
            return "Sports"
        return "Rock"
    
    def _advance_turn(self):
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def handle_correct_answer(self):
        player = self.players[self.current_player]
        if self.players[self.current_player].in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                player.add_coin()
                print(f"{self.players[self.current_player].name} now has {self.players[self.current_player].coins} Gold Coins.")

                winner = self._did_player_win()
                self._advance_turn()

                return winner
            else:
                self._advance_turn()
                return True
        else:
            print("Answer was corrent!!!!")
            player.add_coin()
            print(f"{self.players[self.current_player].name} now has {self.players[self.current_player].coins} Gold Coins.")

            winner = self._did_player_win()
            self._advance_turn()

            return winner

    def wrong_answer(self):
        player = self.players[self.current_player]
        print("Question was incorrectly answered")
        print(f"{self.players[self.current_player].name} was sent to the penalty box")
        player.send_to_penalty_box()

        self._advance_turn()
        return True

    def _did_player_win(self):
        player = self.players[self.current_player]
        return not (player.has_won())