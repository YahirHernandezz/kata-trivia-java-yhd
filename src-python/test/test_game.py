import io
import random
import sys
import pytest
# Yahir Hernández
from trivia.game_old import GameOld
from trivia.game import Game


def extract_output(rand: random.Random, game) -> str:
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        game.add("Chet")
        game.add("Pat")
        game.add("Sue") 

        not_a_winner = False
        while True:
            game.roll(rand.randint(1, 5))

            if rand.randint(0, 8) == 7:
                not_a_winner = game.wrong_answer()
            else:
                not_a_winner = game.handle_correct_answer()

            if not not_a_winner:
                break
    finally:
        sys.stdout = old_stdout

    return buffer.getvalue()


def run_seed(seed: int, print_expected: bool = False):
    expected_output = extract_output(random.Random(seed), GameOld())
    if print_expected:
        print(expected_output)
    actual_output = extract_output(random.Random(seed), Game())
    assert actual_output == expected_output, (
        f"Change detected for seed {seed}. "
        "To debug it, run test_one_seed with that seed."
    )


def test_caracterization():
    """Runs 10,000 random games to verify old and new code output match."""
    for seed in range(1, 10_000):
        run_seed(seed)


@pytest.mark.skip(reason="Enable and set a particular seed to see the output")
def test_one_seed():
    run_seed(1, print_expected=True)