# write your code here
from random import randint
from collections import Counter

def make_grid(cells):
    grid = []
    for i in range(0, len(cells), 3):
        grid.append(list(cells[i:i+3]))
    return grid

def print_grid(grid):
    print('---------')
    for line in grid:
        print('| ', end='')
        for sim in line:
            if sim == '_':
                print('  ', end='')
            else:
                print(sim+' ', end='')
        print('|')
    print('---------')

def next_player(grid):
    cnt_x = 0
    cnt_o = 1
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 'X':
                cnt_x += 1
            if grid[i][j] == 'O':
                cnt_o += 1
    if cnt_x == cnt_o:
        return 'O'
    else:
        return 'X'

def next_move(grid, symbol):
    move = input('Enter the coordinates:')
    try:
        move = move.split( )
        move = [int(i) for i in move]
    except ValueError:
        print('You should enter numbers!')
        return next_move(grid, symbol)
    else:
        if not (0 < move[0] < 4 and  0 < move[1] < 4):
            print('Coordinates should be from 1 to 3!')
            return next_move(grid, symbol)
        if grid[3-move[1]][move[0]-1] != '_':
            print('This cell is occupied! Choose another one!')
            return next_move(grid, symbol)
        else:
            grid[3-move[1]][move[0]-1] = symbol
            return True

def ch_line(grid):
    for line in grid:
        if line[0] == line[1] == line[2]:
            if line[0] == 'X':
                return 'X'
            if line[0] == 'O':
                return 'O'
    return

def ch_col(grid):
    for i in range(3):
        if grid[0][i] == grid[1][i] == grid[2][i]:
            if grid[0][i] == 'X':
                return 'X'
            if grid[0][i] == 'O':
                return 'O'
    return

def ch_cross(grid):
    if (grid[0][0] == grid[1][1] == grid[2][2] or
            grid[0][2] == grid[1][1] == grid[2][0]):
        if grid[1][1] == 'X':
            return 'X'
        if grid[1][1] == 'O':
            return 'O'
    return

def ch_draw(grid):
    for i in grid:
        if '_' in i:
            return
    return 'Draw'

def check_win(grid):
    if ch_line(grid) is not None:
        return ch_line(grid)+' wins'
    if ch_col(grid) is not None:
        return     ch_col(grid)+' wins'
    if ch_cross(grid) is not None:
        return ch_cross(grid)+' wins'
    return

def easy_ai(grid, symbol):
    move = randint(0, 8)
    if grid[move//3][move % 3] == '_':
        print('Making move level "easy"')
        grid[move // 3][move % 3] = symbol
        return True
    else:
        return easy_ai(grid, symbol)

def cross_can_win(grid, symbol):
    if (grid[0][0] + grid[1][1] + grid[2][2]).count(symbol) == 2:
        for i in range(3):
            if grid[i][i] == '_':
                return (i, i)
    if(grid[0][2] + grid[1][1] + grid[2][0]).count(symbol) == 2:
        for i in range(3):
            if grid[i][2-i] == '_':
                return (i, 2-i)
    return False



def rows_can_win(grid, symbol):
    for i, line in enumerate(grid):
        if line.count(symbol) == 2:
            for j, char in enumerate(line):
                if char == '_':
                    return (i, j)
    return False

def col_can_win(grid, symbol):
    for i in range(3):
        if (grid[0][i] + grid[1][i] + grid[2][i]).count(symbol) == 2:
            for j in range(3):
                if grid[j][i] == '_':
                    return (j, i)
    return False

def can_med_win(grid, symbol):
    move = cross_can_win(grid, symbol)
    if move != False:
        return move
    move = rows_can_win(grid, symbol)
    if move != False:
        return move
    move = col_can_win(grid, symbol)
    if move != False:
        return move
    return False





def med_ai(grid, symbol):
    can_win = can_med_win(grid, symbol)
    if can_win != False:
        grid[can_win[0]][can_win[1]] = symbol
        return True
    else:
        if symbol == 'X':
            adv_sym = 'O'
        elif symbol == 'O':
            adv_sym = 'X'
        can_win = can_med_win(grid, adv_sym)
        if can_win != False:
            grid[can_win[0]][can_win[1]] = symbol
            return True
    move = randint(0, 8)
    if grid[move//3][move % 3] == '_':
        print('Making move level "medium"')
        grid[move // 3][move % 3] = symbol
        return True
    else:
        return med_ai(grid, symbol)

def find_avil(grid):
    available_spots =[]
    for i in range(3):
        for j in range(3):
            if grid[i][j] == '_':
                available_spots.append((i, j))
    return available_spots


def minimax(grid, depth, maxim, sym):
    if sym == 'X':
        adv_sym = 'O'
    else:
        adv_sym = 'X'
    fake_grid = grid.copy()
    available_spots = find_avil(grid)
    if depth == 0 or len(available_spots) == 0:
        won = check_win(fake_grid)
        if won is not None:
            if sym in won:
                return 1
            else:
                return -1
        else:
            return 0

    if maxim:
        max_val = - 10000
        for spot in available_spots:
            fake_grid[spot[0]][spot[1]] = sym
            evalu = minimax(fake_grid, depth-1, False, sym)
            max_val = max(max_val, evalu)
        return max_val
    else:
        min_val = 10000
        for spot in available_spots:
            fake_grid[spot[0]][spot[1]] = adv_sym
            evalu = minimax(fake_grid, depth-1, True, sym)
            max_val = min(min_val, evalu)
        return min_val


    # fake_grid = grid.copy()
    # if symbol == 'X':
    #     adv_sym = 'O'
    # else:
    #     adv_sym = 'X'
    # available_spots = find_avil(fake_grid)
    # scores = [0]*len(available_spots)
    # won = check_win(fake_grid)
    # if won is not None:
    #     if symbol in won:
    #         if cnt % 2 == 0:
    #             return 1
    #         return -1
    #     else:
    #         if cnt % 2 == 0:
    #             return -1
    #         return 1
    #
    # if len(available_spots) != 0:
    #     next_turn = available_spots[0]
    #     fake_grid[next_turn[0]][next_turn[1]] = symbol
    #
    #     return minimax(fake_grid, adv_sym, cnt+1)
    # else:
    #     return 0






def get_commands():
    cmd = input('Input command: ')
    if cmd == 'exit':
        quit()
    if cmd.split(' ')[0] == 'start':
        cmd =cmd.split(' ')
        if len(cmd) != 3:
            print('Bad parameters!')
        else:
            players=[]
            for i in cmd:
                if i == 'easy':
                    players.append('easy')
                if i == 'user':
                    players.append('user')
                if i == "medium":
                    players.append('medium')
                if i == "hard":
                    players.append('hard')


            return players
    else:
        return get_commands()


def game(players):
    cells = '_________'
    grid = make_grid(cells)
    print_grid(grid)

    turn_cnt = 0

    while True:
        print(players)
        if ch_draw(grid) is not None:
            print('Draw')
            main()

        won = check_win(grid)
        if won is not None:
            print(won)
            main()

        if turn_cnt % 2 == 0:
            symbol = 'X'
        else:
            symbol = 'O'

        print(players[turn_cnt])
        if players[turn_cnt] == 'easy':
            moved = easy_ai(grid, symbol)
            if moved:
                print_grid(grid)
                turn_cnt = (turn_cnt + 1) % 2
                continue

        if players[turn_cnt] == 'medium':
            moved = med_ai(grid, symbol)
            if moved:
                print_grid(grid)
                turn_cnt = (turn_cnt + 1) % 2
                continue

        if players[turn_cnt] == 'hard':
            minimax(grid, 9, True, symbol)
            print_grid(grid)
            turn_cnt = (turn_cnt + 1) % 2
            continue


        if players[turn_cnt] == 'user':
            moved = next_move(grid, symbol)
            if moved:
                print_grid(grid)
                turn_cnt = (turn_cnt + 1) % 2
                continue


def main():
    players = get_commands()
    game(players)



if __name__ == '__main__':
    main()

