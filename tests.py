import game_board

game = game_board.GameBoard()
for i in range(100):
    mover_info = game.check_snakes_ladders(i)
    print(f'Checking Square: {i}, Mover Info Returned: {mover_info}')