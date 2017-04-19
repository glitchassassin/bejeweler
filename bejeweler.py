import lackey

def main():
    lackey.Settings.InfoLogs = False
    lackey.Settings.ActionLogs = False
    
    r = start_game()
    board = r.offset(lackey.Location(336, 80))
    board.setW(660)
    board.setH(660)
    cell_size = board.getW()/8
    while True:
        grid = find_gems(board)
        #print("\n".join([str(r) for r in grid]))
        moves = calculate_move(grid)
        if moves is None:
            print("No matches found, waiting...")
            continue
        square1, square2 = moves
        print (square1, square2)
        square1_click = lackey.Location(
            board.getX() + (square1[1] * cell_size + (cell_size/2)),
            board.getY() + (square1[0] * cell_size + (cell_size/2))
        )
        square2_click = lackey.Location(
            board.getX() + (square2[1] * cell_size + (cell_size/2)),
            board.getY() + (square2[0] * cell_size + (cell_size/2))
        )
        board.click(square1_click)
        lackey.sleep(0.3)
        board.click(square2_click)
        #break

def find_gems(board):
    #board.debugPreview()
    gem_types = [
        ("green_gem.png", 0.85),
        ("yellow_gem.png", 0.85),
        ("red_gem.png", 0.85),
        ("purple_gem.png", 0.75),
        ("orange_gem.png", 0.85),
        ("white_gem.png", 0.85),
        ("blue_gem.png", 0.85)
    ]
    board_state = [[None for j in range(8)] for i in range(8)]
    cell_size = board.getW()/8
    for gem, similarity in gem_types:
        matches = board.findAll(lackey.Pattern(gem).similar(similarity))
        offset = board.getTopLeft()
        for m in matches:
            board_x = int((m.getTarget().x - offset.x)/cell_size)
            board_y = int((m.getTarget().y - offset.y)/cell_size)
            board_state[board_y][board_x] = gem[:1]
        #print ("\n".join([str(m.getTarget()) for m in matches]))
        #break
    return board_state

def calculate_move(grid):
    moves = calculate_move_horizontal(grid)
    if moves is not None:
        return moves
    # No horizontal moves; transpose and check for vertical moves
    moves = calculate_move_horizontal(zip(*grid))
    if moves is not None:
        return (reversed(move) for move in moves)

def calculate_move_horizontal(grid):
    # Potential horizontal matches can be one of three sets:
    # oxo | oox | xoo
    print("\n".join([str(r) for r in grid]))
    match_patterns = [
        ([[1,1,0],
          [0,0,1]], ((1,2), (0,2))),

        ([[0,0,1],
          [1,1,0]], ((0,2), (1,2))),

        ([[0,1,1],
          [1,0,0]], ((1,0), (0,0))),

        ([[1,0,0],
          [0,1,1]], ((0,0), (1,0))),

        ([[0,1,0],
          [1,0,1]], ((0,1), (1,1))),

        ([[1,0,1],
          [0,1,0]], ((1,1), (0,1))),

        ([[1,1,0,1]], ((0,3), (0,2))),
        ([[1,0,1,1]], ((0,0), (0,1))),
    ]
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell is None:
                continue # Didn't recognize this gem
            elif col_index < len(row)-1 and cell == row[col_index+1]:
                # Gem is adjacent to a same-colored gem
                # Check if there is a catty-corner gem to move
                try:
                    upper_left = grid[row_index-1][col_index-1] if row_index > 0 and col_index > 0 else None
                except:
                    upper_left = None
                try:
                    lower_left = grid[row_index+1][col_index-1] if col_index > 0 else None
                except:
                    lower_left = None
                try:
                    upper_right = grid[row_index-1][col_index+2] if row_index > 0 else None
                except:
                    upper_right = None
                try:
                    lower_right = grid[row_index+1][col_index+2]
                except:
                    lower_right = None
                
                if cell == upper_left:
                    # Swap upper left with left
                    return ((row_index-1, col_index-1), (row_index, col_index-1))
                elif cell == lower_left:
                    # Swap lower left with left
                    return ((row_index+1, col_index-1), (row_index, col_index-1))
                if cell == upper_right:
                    # Swap upper left with left
                    return ((row_index-1, col_index+2), (row_index, col_index+2))
                elif cell == lower_right:
                    # Swap lower left with left
                    return ((row_index+1, col_index+2), (row_index, col_index+2))
            elif col_index < len(row)-2 and cell == row[col_index+2]:
                # Gem is separated from a same-colored gem by one
                try:
                    upper_middle = grid[row_index-1][col_index+1] if row_index > 0 else None
                except:
                    upper_middle = None
                try:
                    lower_middle = grid[row_index+1][col_index+1]
                except:
                    lower_middle = None
                
                if cell == upper_middle:
                    # Swap upper middle with middle
                    return ((row_index-1, col_index+1), (row_index, col_index+1))
                elif cell == lower_middle:
                    # Swap lower middle with middle
                    return ((row_index+1, col_index+1), (row_index, col_index+1))


def start_game():
    app = lackey.App("Bejeweled").focus()
    r = app.window()
    if not r.exists(lackey.Pattern("hint_button.png"), 0.5):
        if not r.exists(lackey.Pattern("zen_mode.png"), 0.5):
            r.wait(lackey.Pattern("play_button.png"))
            r.click()
        r.wait(lackey.Pattern("zen_mode.png"))
        r.click()
    r.wait(lackey.Pattern("hint_button.png"))
    return r

if __name__ == "__main__":
    main()