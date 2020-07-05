# write your code here
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

def next_move(grid):
    move = input('Enter the coordinates:')
    try:
        move = move.split( )
        move = [int(i) for i in move]
    except:
        print('You should enter numbers!')
        return next_move(grid)
    else:
        if not (0 < move[0] < 4 and  0 < move[1] < 4):
            print('Coordinates should be from 1 to 3!')
            return next_move(grid)
        if grid[3-move[1]][move[0]-1] != '_':
            print('This cell is occupied! Choose another one!')
            return next_move(grid)
        else:
            chr = next_player(grid)
            grid[3-move[1]][move[0]-1] = chr
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


def main():
    cells = input('Enter cells: ')
    grid = make_grid(cells)
    print_grid(grid)
    while True:
        moved = next_move(grid)
        if moved:
            print_grid(grid)
        won =check_win(grid)
        if won is not None:
            print(won)
            break
        if ch_draw(grid) is not None:
            print('Draw')
            break
        print('Game not finished')
        break


if __name__ == '__main__':
    main()



