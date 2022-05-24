import chess.pgn
from requests import delete
from stockfishpy.stockfishpy import Engine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

username = ''
password = ''

def init_page():
    driver = webdriver.Firefox()
    driver.get('https://www.chess.com/login')
    return driver


def login(driver):
    global username, password
    elem = driver.find_element_by_id('username')
    elem.clear()
    elem.send_keys(username)
    elem = driver.find_element_by_id('password')
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    return


def game_init(driver, chessEngine):
    while 1:
        try:
         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'draw-button-component')))
         break
        except TimeoutException:
         print("Arguadando o jogo começar")
        pass

    play(driver, chessEngine)
    return


def play(driver, chessEngine):
    

    pgn = ""
    user_color = ""
    open('plays.pgn', 'w').close()

    elem_user = driver.find_element(By.XPATH, "//*[@class='live-game-start-component']/span/a[@class='user-username username'][1]").text
    print(elem_user)

    if elem_user == username:
        print("Sua cor é branco")
        user_color = "white"
    else:
        print("Sua cor é preto")
        user_color = "black"



    for move_number in range(1, 500):

        if user_color == 'white':
            if move_number != 1:
                best_move = get_best_move(chessEngine)
                highlight_move(driver, user_color, best_move)
            
        while 1:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='move']/div[@class='white node selected'][1]")))
                playWhite = driver.find_element(By.XPATH, "//*[@class='move']/div[@class='white node selected'][1]").text

                logpgnw = str(+move_number)+". "+playWhite + " "

                pgn = new_move_png(pgn, logpgnw)

                if user_color == 'white':
                    if move_number != 1:
                        delete_highlight(driver, user_color, best_move)
                    

                with open("plays.pgn", "w") as text_file:
                    text_file.write("%s" % pgn)

                break
            except TimeoutException:
                pass

        if user_color == 'black':    
            best_move = get_best_move(chessEngine)
            highlight_move(driver, user_color, best_move)
            
        while 1:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='move']/div[@class='black node selected'][1]")))
                playBlack = driver.find_element(By.XPATH, "//*[@class='move']/div[@class='black node selected'][1]").text

                logpgnb = str(playBlack+" ")


                pgn = new_move_png(pgn, logpgnb)

                if user_color == "black":
                    delete_highlight(driver, user_color, best_move)
                    

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

def highlight_move(driver, user_color, best_move):
    driver.execute_script("""


        chessboard = document.getElementById('board-single');


        highlight1_pos = arguments[0].charCodeAt(0) - 'a'.charCodeAt() + 1 
        highlight1_class = + highlight1_pos + arguments[1];
        element = document.createElement('div');      
        element.setAttribute("class", "highlight square-" + highlight1_class);   
        element.setAttribute("id", "highlight 11");   
        element.setAttribute("style", "background-color: rgb(235, 97, 80); opacity: 0.8");    
        chessboard.appendChild(element);



        highlight1_pos = arguments[2].charCodeAt(0) - 'a'.charCodeAt() + 1 
        highlight1_class = + highlight1_pos + arguments[3];
        element = document.createElement('div');      
        element.setAttribute("class", "highlight square-" + highlight1_class);   
        element.setAttribute("id", "highlight 12");   
        element.setAttribute("style", "background-color: rgb(235, 97, 80); opacity: 0.8");    
        chessboard.appendChild(element);


       """, best_move[0], best_move[1], best_move[2], best_move[3], user_color)
    return

def delete_highlight(driver, user_color, best_move):
    driver.execute_script("""



        highlight1_pos = arguments[0].charCodeAt(0) - 'a'.charCodeAt() + 1 
        highlight1_class = + highlight1_pos + arguments[1];
        element = document.getElementById("highlight 11");
        element.parentNode.removeChild(element);

        highlight1_pos = arguments[2].charCodeAt(0) - 'a'.charCodeAt() + 1 
        highlight1_class = + highlight1_pos + arguments[3];
        element = document.getElementById("highlight 12");
        element.parentNode.removeChild(element);


       """, best_move[0], best_move[1], best_move[2], best_move[3], user_color)
    return


def main():
    chessEngine = Engine('./stockfish_13_linux_x64', param={'Threads': 2, 'Ponder': True})
    

    driver = init_page()

    login(driver)
    game_init(driver, chessEngine)
    


main()
    
