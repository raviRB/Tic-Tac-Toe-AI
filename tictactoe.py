import pygame
import  time
import copy

def init_game():

    pygame.init()
    global display_height ,display_width ,game_screen ,white, black , font_name , red , blue
    display_height = 300
    display_width = 300
    font_name = "comicsansms"
    game_screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("TIC TAC TOE - AI")

    white = (255, 255, 255)
    black = (0, 0, 0)
    red  = (250 , 0 ,0)
    blue = (0 ,0 , 250 )
    game_screen.fill(white)
    pygame.display.update()

def display_win_draw(player , draw = False):

    player  = player + 1
    game_screen.fill(white)
    if not draw:
        display_text("player " + str(player) + " won", display_width // 2, display_height // 2)
        print("player " + str(player) + " won")

    else:
        display_text("Draw", display_width // 2, display_height // 2)
        print("DRAW")

    pygame.display.update()
    time.sleep(3)

def display_text(message ,  x_cord , y_cord ,font_size = 40 ):

    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(message, True, black)
    textRect = text.get_rect()
    textRect.center = (x_cord , y_cord)
    game_screen.blit(text, textRect)

def cal_depth(board_state):  # number of board positions used

    depth = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board_state[i][j] != 0:
                depth+=1
    return depth

def minimax(board , depth , isComp , player):

    if not isComp :
        if depth == 9:
            if check_if_won(player + 1, board):
                return -1
            return 0
        bestval = +999999
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == 0:
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = player + 1
                    if check_if_won(player + 1, new_board):
                        return -1
                    temp = minimax(new_board, depth +1, True , 1 - player)
                    if temp < bestval:
                        bestval = temp
    else:
        if depth == 9:
            if check_if_won(player + 1, board):
                return 1
            return 0
        bestval = -999999
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == 0:
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = player + 1
                    if check_if_won(player + 1, new_board):
                        return 1
                    temp = minimax(new_board, depth +1, False , 1 - player)
                    if temp > bestval:
                        bestval = temp


    return bestval

def AI_makemove(board_state  , depth , player):
    start = time.time()
    bestval = -9999
    a = 0
    b = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board_state[i][j] == 0:
                new_board = copy.deepcopy(board_state)
                new_board[i][j] = player + 1
                if check_if_won(player + 1, new_board):
                    bestval = 1
                    a = i
                    b = j
                temp =  minimax(new_board , depth+1, False, 1 - player)
                if temp > bestval:
                    bestval =  temp
                    a = i
                    b = j

    end = time.time()
    print("Time taken for this move : ",(end-start)," seconds")
    return [bestval , a ,b]


def get_box(mouseclick_x , mouseclick_y):  # x and y co-ordianate of box on the grid
    if mouseclick_x <= 100:
        x = 0
    elif mouseclick_x <= 200:
        x = 1
    else:
        x = 2
    if mouseclick_y <= 100:
        y = 0
    elif mouseclick_y <= 200:
        y = 1
    else:
        y = 2
    return x,y

def check_if_won(player,board):
    # row
    for i in range(0,3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] == player:
            return True
    # col
    for i in range(0,3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] == player:
            return True
    # diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] == player:
        return True
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] == player:
        return True

def com_make_move(board, player):
    new_board = copy.deepcopy(board)
    val, i, j = AI_makemove(new_board, cal_depth(board),player)
    if board[i][j] == 0:
        board[i][j] = player + 1
        return True

def user_make_move(board,player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            co_ordinates = pygame.mouse.get_pos()
            box_col, box_row = get_box(*co_ordinates)
            if not board[box_row][box_col]:
                board[box_row][box_col] = player + 1
                return True

def draw_populate_board_caller(board):
    draw_board()
    populate_board(board)
    pygame.display.update()

def is_board_empty(board):
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] != 0:
                return False
    return True

def draw_circle(x_cord,y_cord):
    x_cord = x_cord*100 + 50
    y_cord = y_cord*100 + 50
    pygame.draw.circle(game_screen,blue,(x_cord,y_cord),30, 5)


def populate_board(board):
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == 1:
                draw_cross(j, i)
            elif board[i][j] == 2:
                draw_circle(j, i)

def draw_cross(x_cord,y_cord):
    x_cord = x_cord*100 + 50
    y_cord = y_cord*100 + 50
    pygame.draw.line(game_screen, red, (x_cord - 30 , y_cord - 30), (x_cord + 30 , y_cord + 30), 5)
    pygame.draw.line(game_screen, red, (x_cord + 30 , y_cord - 30), (x_cord - 30 , y_cord + 30), 5)

def draw_board():
    pygame.draw.line(game_screen, black, (100, 0), (100, 300), 3)
    pygame.draw.line(game_screen, black, (200, 0), (200, 300), 3)
    pygame.draw.line(game_screen, black, (0, 100), (300, 100), 3)
    pygame.draw.line(game_screen, black, (0, 200), (300, 200), 3)

def game_loop():

    global first_player , second_player
    key_pressed = False  # true if user has pressed a key
    init_game()
    display_text("press 1 for single player",display_width//2 ,(display_height-10)//2 , 20)
    display_text("press 2 for multi player", display_width // 2, (display_height+40) // 2, 20)
    pygame.display.update()
    game_close = False
    game_start = False

    while not game_start:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_2:
                    first_player = "user1"
                    second_player = "user2"
                    game_start = True

                elif event.key == pygame.K_1:
                    game_screen.fill(white)
                    display_text("press 1 to play first", display_width // 2, (display_height - 10) // 2, 20)
                    display_text("otherwise press 2", display_width // 2, (display_height + 40) // 2, 20)
                    pygame.display.update()

                    while not key_pressed:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1:
                                    first_player = "user1"
                                    second_player = "com"
                                    key_pressed = True
                                elif event.key == pygame.K_2:
                                    first_player = "com"
                                    second_player = "user1"
                                    key_pressed = True
                    game_start = True

    while not game_close:  # close game screen

        player = 0  # 0 first player 1 second player
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        game_over = False
        game_screen.fill(white)
        draw_populate_board_caller(board)

        while not game_over:
            game_screen.fill(white)
            if cal_depth(board) == 9:
                display_win_draw(player, True)
                game_over = True
                continue

            if player == 0:   # first player
                if first_player is "com":
                    if is_board_empty(board):
                        board[0][0] = player + 1
                        player = 1 - player
                    elif com_make_move(board,player):
                        if check_if_won(player + 1, board):
                            display_win_draw(player)
                            game_over = True
                        player = 1 - player

                else:
                    if user_make_move(board,player):
                        if check_if_won(player + 1, board):
                            display_win_draw(player)
                            game_over = True
                        player = 1 - player

                draw_populate_board_caller(board)

            if player == 1:  # second player
                if second_player is "com":
                    if com_make_move(board,player):
                        if check_if_won(player + 1, board):
                            display_win_draw(player)
                            game_over = True
                        player = 1 - player
                else:
                    if user_make_move(board,player):
                        if check_if_won(player + 1, board):
                            display_win_draw(player)
                            game_over = True
                        player = 1 - player

                draw_populate_board_caller(board)

        draw_populate_board_caller(board)


game_loop()
