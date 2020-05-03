from utils_viv import dumb_ideas
import time
if __name__ == "__main__":
    obj = dumb_ideas()
    obj.init_selenium()
    obj.init_stockfish()
    obj.get_into_game()
    obj.bad_player()
