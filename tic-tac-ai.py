# write your code here
from random import randint

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
            return players
    else:
        return get_commands()


def game(players):
    cells = '_________'
    grid = make_grid(cells)
    print_grid(grid)

    turn_cnt = 0

    while True:
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

        if players[turn_cnt] == 'easy':
            moved = easy_ai(grid, symbol)
            if moved:
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
