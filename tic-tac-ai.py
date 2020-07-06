from random import randint, choice
from copy import deepcopy


def make_grid():
    """
    :return: 2d array for the game
    """
    cells = '_________'
    grid = []
    for i in range(0, len(cells), 3):
        grid.append(list(cells[i:i+3]))
    return grid


def print_grid(grid):
    """
    :param grid: 2d array
    prints current state of the game
    """
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


def user_move(grid, symbol):
    """
    :param grid: game bord
    :param symbol: X or O
    accepts input from user and let him play
    """
    move = input('Enter the coordinates:    ')
    try:
        move = move.split( )
        move = [int(i) for i in move]
    except ValueError:
        print('You should enter numbers!')
        return user_move(grid, symbol)
    else:
        if not (0 <= move[0] <= 2 and 0 <= move[1] <= 2):
            print('Coordinates should be from 0 to 2!')
            return user_move(grid, symbol)
        if grid[move[0]][move[1]] != '_':
            print('This cell is occupied! Choose another one!')
            return user_move(grid, symbol)
        else:
            grid[move[0]][move[1]] = symbol
            return


def win_chk(grid):
    """
    :param grid: bord state
    :return: string of who won or None if nobdy won
    """
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

    def check_win(grid):
        if ch_line(grid) is not None:
            return ch_line(grid)+' wins'
        if ch_col(grid) is not None:
            return ch_col(grid)+' wins'
        if ch_cross(grid) is not None:
            return ch_cross(grid)+' wins'
        return

    return check_win(grid)


def easy_ai(grid, symbol):
    """
    :param grid: game bord
    :param symbol: X or O
    """
    move = choice(find_avil(grid))
    print('Making move level "easy"')
    grid[move[0]][move[1]] = symbol


def medium_ai(grid, symbol):
    """
    :param grid: game bord
    :param symbol: X or O
    """
    def cross_can_win(grid, symbol):
        if (grid[0][0] + grid[1][1] + grid[2][2]).count(symbol) == 2:
            for i in range(3):
                if grid[i][i] == '_':
                    return (i, i)
        if (grid[0][2] + grid[1][1] + grid[2][0]).count(symbol) == 2:
            for i in range(3):
                if grid[i][2 - i] == '_':
                    return (i, 2 - i)
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
        """
        chacks if symbol can win next turn
        """
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
            return
        else:
            switch_sym = {'X': 'O', 'O': 'X'}
            adv_sym = switch_sym[symbol]
            can_win = can_med_win(grid, adv_sym)
            if can_win != False:
                grid[can_win[0]][can_win[1]] = symbol
                return
        move = choice(find_avil(grid))
        print('Making move level "medium"')
        grid[move[0]][move[1]] = symbol
        return

    med_ai(grid, symbol)


def find_avil(grid):
    """
    :param grid:  game bord
    :return: list of empty spots
    """
    available_spots =[]
    for i in range(3):
        for j in range(3):
            if grid[i][j] == '_':
                available_spots.append((i, j))
    return available_spots


def hard_ai(grid, depth, sym):
    """
    :param grid:
    :param depth:
    :param sym:
    hard AI implementation using minimax
    """
    def minimax_init(grid, depth, sym):
        """
        initialising conditions for minimax
        """
        if len(find_avil(grid)) == 9:
            best_spot = choice([(0, 0), (2, 2), (2, 0), (0, 2)])
            grid[best_spot[0]][best_spot[1]] = sym
            return
        best_score = -100
        fake_grid = deepcopy(grid)
        for i in range(3):
            for j in range(3):
                if grid[i][j] == '_':
                    fake_grid[i][j] = sym
                    score = minimax(fake_grid, depth, False, sym)
                    fake_grid[i][j] = '_'
                    #print(score , (i, j))
                    if score > best_score:
                        best_score = score
                        best_spot = (i, j)

        grid[best_spot[0]][best_spot[1]] = sym


    def minimax(grid, depth, maxim, sym):
        """
        :param grid: game bord state after initialiser move
        :param depth: depth of search - not used
        :param maxim: Is maximising player
        :param sym: symbol of maximising player
        :return: return max score possible given minimax
        """
        switch_sym = {'X': 'O', 'O': 'X'}
        adv_sym = switch_sym[sym]
        available_spots = find_avil(grid)
        won = win_chk(grid)
        if won is not None:
            if sym in won:
                return 10
            elif adv_sym in won:
                return -10
            else:
                return 0
        elif len(available_spots) == 0:
            return 0
        else:
            scores = []
            if maxim:
                available_spots = find_avil(grid)
                for spot in available_spots:
                    grid[spot[0]][spot[1]] = sym
                    evalu = minimax(grid, depth-1, False, sym)
                    grid[spot[0]][spot[1]] = '_'
                    scores.append(evalu)
                return max(scores)
            else:
                available_spots = find_avil(grid)
                for spot in available_spots:
                    grid[spot[0]][spot[1]] = adv_sym
                    evalu = minimax(grid, depth-1, True, sym)
                    grid[spot[0]][spot[1]] = '_'
                    scores.append(evalu)
                return min(scores)

    minimax_init(grid, depth, sym)


def get_commands():
    """
    starts a new game or quit
    :return list of players
    """
    print('Format: start p1 p2  or exit \ngame modes: user / easy / medium / hard')
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
                if i == 'easy' or i == 'user' or i == "medium" or i == "hard":
                    players.append(i)
            if len(players) != 2:
                print('Bad parameters!\n')
                return get_commands()
            return players
    else:
        return get_commands()


def pick_player(player, grid, symbol):
    """
    :param player: players turn
    :param grid: game bord
    :param symbol: X or O
    """
    if player == 'easy':
        easy_ai(grid, symbol)
        print_grid(grid)
        return

    if player == 'medium':
        medium_ai(grid, symbol)
        print_grid(grid)
        return

    if player == 'hard':
        hard_ai(grid, 9, symbol)
        print_grid(grid)
        return

    if player == 'user':
        user_move(grid, symbol)
        print_grid(grid)
        return


def game(players):
    """
    manages the game
    :param players: a list of players
    """
    grid = make_grid()
    print_grid(grid)
    turn_cnt = 0
    while True:
        won = win_chk(grid)
        if won is not None:
            print(won)
            main()

        if len(find_avil(grid)) == 0:
            print('Draw')
            main()

        if turn_cnt % 2 == 0:
            symbol = 'X'
        else:
            symbol = 'O'

        pick_player(players[turn_cnt], grid, symbol)
        turn_cnt = (turn_cnt + 1) % 2


def main():
    players = get_commands()
    game(players)



if __name__ == '__main__':
    main()

