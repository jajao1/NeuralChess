import chess.pgn
from lib2to3.pgen2 import driver
from stockfishpy.stockfishpy import Engine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def init_page():
    driver = webdriver.Firefox()
    driver.get('https://www.chess.com')
    return driver


def game_init(driver, chessEngine):
    while 1:
        try:
         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='move']/div[@class='white node selected'][1]")))
         break
        except TimeoutException:
         print("Arguadando o jogo começar")
        pass

    play(driver, chessEngine)
    return


def play(driver, chessEngine):
    

    pgn = ""
    open('plays.pgn', 'w').close()

    print("Qual sua cor")

    user_color = input()


    for move_number in range(1, 500):

        if move_number == 1:
            print("e2e4")

        while 1:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='move']/div[@class='white node selected'][1]")))
                playWhite = driver.find_element(By.XPATH, "//*[@class='move']/div[@class='white node selected'][1]").text

                print(move_number,". ",playWhite," ")
                logpgnw = str(+move_number)+". "+playWhite

                pgn = new_move_png(pgn, logpgnw)

                with open("plays.pgn", "w") as text_file:
                    text_file.write("%s" % pgn)

                break
            except TimeoutException:
                pass

        best_move = get_best_move(chessEngine)
        print(best_move)
            
        while 1:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='move']/div[@class='black node selected'][1]")))
                playBlack = driver.find_element(By.XPATH, "//*[@class='move']/div[@class='black node selected'][1]").text

                logpgnb = str(" "+playBlack+" ")

                print(logpgnb)


                pgn = new_move_png(pgn, logpgnb)


                with open("plays.pgn", "w") as text_file:
                    text_file.write("%s" % pgn)
                break
            except TimeoutException:
                pass
    return

def new_move_png(pgn, logpgn):

    pgn += logpgn 

    return pgn
    

def get_best_move(chessEngine):

    pgnfilename = str('plays.pgn')

    with open(pgnfilename, encoding="utf-8-sig") as fi:
        game = chess.pgn.read_game(fi)

    game = game.end()
    board = game.board()

    chessEngine.ucinewgame()
    chessEngine.setposition(board.fen())

    move = chessEngine.bestmove()
    bestmove = move['bestmove']
    
    return bestmove


def main():
    chessEngine = Engine('./stockfish_13_linux_x64', param={'Threads': 2, 'Ponder': True})

    driver = init_page()
    game_init(driver, chessEngine)
    


main()
    