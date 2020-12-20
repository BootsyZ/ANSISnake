import sys
from snake.snake import Snake

if __name__ == "__main__":
    argv = sys.argv[1:]
    kwargs = {kw[0]: kw[1] for kw in [ar.split('=') for ar in argv if ar.find('=') > 0]}
    args = [arg for arg in argv if arg.find('=') < 0]
    game = Snake(*args, **kwargs)
    game.start()
