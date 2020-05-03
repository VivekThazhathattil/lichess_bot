from selenium import webdriver
from selenium.webdriver import ActionChains
from stockfish import Stockfish
import re
import random
import time
import requests

#TODO: Fix for wait till opponent play
class dumb_ideas(object):
    def get_into_game(self):
        time.sleep(2)
        quick_pair_button = self.driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/span[1]")
        quick_pair_button.click()
        time.sleep(2)
        one_min_button = self.driver.find_element_by_xpath("/html/body/div/main/div[2]/div[2]/div[1]")
        one_min_button.click()
#        play_comp_button = self.driver.find_element_by_xpath("/html/body/div/main/div[1]/div[1]/a[3]")
#        play_comp_button.click()
#        play_button = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div[5]/button[2]")
#        play_button.click()
#        five_min_button = self.driver.find_element_by_xpath("/html/body/div/main/div[2]/div[2]/div[5]")
#        five_min_button.click()
    
    def _get_move_list(self):
        self.ingame_url = self.driver.current_url
        response = requests.get(self.driver.current_url)
        self.html_source = response.content.decode('utf-8')
        temp_move_list = re.findall("\"uci\":\"\w+\"",self.html_source)
        self.move_list = []
        for move in temp_move_list: # #TODO:use translation while making moves as well
            mv = str(move)[7:-1:1]
            if mv == "e1h1":
                mv = "e1g1"
            elif mv == "e8h8":
                mv = "e8g8"
            elif mv == "e1a1":
                mv = "e1c1"
            elif mv == "e8a8":
                mv = "e8c8"
            self.move_list.append(mv)
        self.num_moves = len(self.move_list)
#        print(str(self.ingame_url))
        print("Move list:")
        i = 0
        for move in self.move_list:
            i = i + 1
            print(str(i) + ") " + move)
        print("\n")
#        print("is last move valid? : ")
#        print(self.stockfish.is_move_correct(self.move_list[-1]))
    
    def _move_decider(self):
        self.stockfish.set_position(self.move_list)
        if (self.is_white and self.num_moves % 2 ==0) or (not self.is_white  and self.num_moves % 2 !=0):
                best_move = self.stockfish.get_best_move()
                print("best move: " + str(best_move))
                self.click_square(best_move[:2])
                self.click_square(best_move[2:])
            
        
    def _am_i_white(self):
        print("hello")
        self.html_source = self.driver.page_source
        rel_text = re.findall("\"player\":{\"color\":\"\w+\"",self.html_source)
        print("The player's color is " + str(rel_text[0])[19:-1:1])
        if(str(rel_text[0])[19:-1:1] != "white"):
            self.is_white = False
        else:
            self.is_white = True 
        
    def init_stockfish(self):
        self.stockfish = Stockfish("/home/tvivek/experimental/lichess_bot/stockfish-11-linux/Linux/stockfish_20011801_x64_modern")
        self.stockfish.set_skill_level(1) # set this for player strength MAX:=20

    def init_selenium(self):
        self.driver = webdriver.Chrome() # pakal-maanyan
#        self.kili = webdriver.Chrome() # udaayippu
        self.driver.get("https://lichess.org")

    def click_square(self,square):
        column_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        x = column_map[square[0]]
        y = int(square[1]) - 1
        # determine orientation of board
        board = self.driver.find_element_by_xpath("/html/body/div/main/div[1]/div[1]/div/cg-helper/cg-container/cg-board")
        ori = self.driver.find_element_by_xpath("/html/body/div/main/div[1]/div[1]/div")
        orientation = ori.get_attribute("class")
        if 'orientation-black' in orientation:
            x = 7 - x
        else:
            y = 7 - y
        print((x,y))
        x = x * 64 + 32
        y = y * 64 + 32
        
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(board, x, y)
        action.click()
        action.perform()
    
    def bad_player(self):
        #TODO: Check if the game is over or not
        for i in range(10):
            try:
                self._am_i_white()
            except:
                time.sleep(1)
                continue
        while True:
            try:
                self._get_move_list()
                my_time = self.driver.find_element_by_xpath("/html/body/div/main/div[1]/div[9]/div[2]")
                my_time = self.driver.find_element_by_class("time")
                time.sleep(random.uniform(0,0.8))
                self._move_decider()
                self.check_if_game_over()
                if self.is_game_over:
                    print("getting new opponent")
                    self.get_new_opponent()
                self._am_i_white()
            except:
                pass

    def check_if_game_over(self):
        my_check = self.driver.find_element_by_text("NEW OPPONENT")
        if my_check != Null:
            print("my check isn't empty")
            self.is_game_over = True
        else:
            print("my check is empty")
            self.is_game_over = False


    def get_new_opponent(self):
        new_opponent_button = self.driver.find_element_by_xpath("/html/body/div/main/div[1]/div[6]/div/a[1]")
        new_opponet_button.click()
        self.bad_player()


