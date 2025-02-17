import sys

sys.dont_write_bytecode = (
    True  # Prevents __pycache__ folder from being generated in vsc
)


from game import Game


if __name__ == "__main__":
    Game().play()
