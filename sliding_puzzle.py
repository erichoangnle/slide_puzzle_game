from datetime import datetime
from itertools import product
import pygame, sys, os, random
from shutil import rmtree
from PIL import Image


WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
window_size = width, height = 770, 600
pic_size = pic_width, pic_height = 320, 480
tile_size = 80

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 18)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sliding Puzzle")


win = [
    ['0-0.jpg', '0-1.jpg', '0-2.jpg', '0-3.jpg'],
    ['1-0.jpg', '1-1.jpg', '1-2.jpg', '1-3.jpg'],
    ['2-0.jpg', '2-1.jpg', '2-2.jpg', '2-3.jpg'],
    ['3-0.jpg', '3-1.jpg', '3-2.jpg', '3-3.jpg'],
    ['4-0.jpg', '4-1.jpg', '4-2.jpg', '4-3.jpg'],
    ['5-0.jpg', '5-1.jpg', '5-2.jpg', '']
]

rank = {
    '0-0.jpg': 1, '0-1.jpg': 2, '0-2.jpg': 3, '0-3.jpg': 4,
    '1-0.jpg': 5, '1-1.jpg': 6, '1-2.jpg': 7, '1-3.jpg': 8,
    '2-0.jpg': 9, '2-1.jpg': 10, '2-2.jpg': 11, '2-3.jpg': 12,
    '3-0.jpg': 13, '3-1.jpg': 14, '3-2.jpg': 15, '3-3.jpg': 16,
    '4-0.jpg': 17, '4-1.jpg': 18, '4-2.jpg': 19, '4-3.jpg': 20,
    '5-0.jpg': 21, '5-1.jpg': 22, '5-2.jpg': 23
}

board = []
for i in range(50, pic_height, tile_size + 1):
    row = []
    for j in range(40, pic_width, tile_size + 1):
        row.append((j, i))
    board.append(row)


def draw_grid():
    """
    Draw a grid on game window.
    """
    for row in board:
        for item in row:
            rect = pygame.Rect(item[0], item[1], tile_size, tile_size)
            pygame.draw.rect(screen, BLACK, rect, 1)


def solvable(tile_list):
    """
    Count number of inversions of randomly generated puzzle. Count
    the number of row from bottom to the row where black space is at.
    if the number of inversions is odd and the blank is on even row
    counting from the bottm up, or vice versa, the puzzle is solvable.
    """
    inversion_count = 0
    for i in range(len(tile_list)):
        for j in range(i + 1, len(tile_list)):
            if tile_list[i] != '' and tile_list[j] != '' and tile_list[i] > tile_list[j]:
                inversion_count += 1

    for i in range(len(tile_list)):
        if tile_list[i] == '':
            zero_inversion =  6 - (i // 4)

    if (inversion_count % 2) != (zero_inversion % 2): return True
    else: return False


def cut_image(img_name):
    """
    Create a temporary folder. Choose a random image in img
    folder. Cut image to tile size and save output (except last tile)
    to temp folder.
    """
    try:
        os.mkdir('data/temp')
    except FileExistsError:
        pass

    img = Image.open(img_name)
    width, height = img.size

    grid = product(*(range(0, height, tile_size), range(0, width, tile_size)))
    for i, j in grid:
        tile = (j, i, j + tile_size, i + tile_size)
        output = f"data/temp/{int(i / tile_size)}-{int(j / tile_size)}.jpg"
        if output != 'data/temp/5-3.jpg':
            img.crop(tile).save(output)


def generate_puzzle(state):
    """
    Generate random puzzle from cut images.
    """
    tile_list = os.listdir('data/temp')
    tile_list.append("")
    random.shuffle(tile_list)

    if solvable(tile_list):
        for i in range(6):
            for j in range(4):
                state[i][j] = tile_list[0]
                tile_list.pop(0)
        return
    else:
        generate_puzzle(state)


def render_game(img_name, state):
    """
    Place cut image tile on grid randomly and place original image.
    """
    for i in range(6):
        for j in range(4):
            try:
                tile = pygame.image.load(f'data/temp/{state[i][j]}')
                screen.blit(tile, (board[i][j][0], board[i][j][1]))
            except FileNotFoundError:
                pass

    img = pygame.image.load(img_name)
    screen.blit(img, (410, 53))
        

def move_tile(state, x, y):
    """
    If there is an empty cell vertically or horizontally
    adjacent to clicked tile, move the tile to that cell.
    """
    for i in range(6):
        for j in range(4):
            rect = pygame.Rect(board[i][j][0], board[i][j][1], tile_size, tile_size)
            if rect.collidepoint(x, y):
                adjacent = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                for cell in adjacent:
                    if cell[0] >= 0 and cell[0] <= 5 and cell[1] >= 0 and cell[1] <= 3:
                        if state[cell[0]][cell[1]] == '':
                            state[cell[0]][cell[1]] = state[i][j]
                            state[i][j] = ''
                            return True
        

def main():

    game = 0

    while True:

        state = [['' for _ in range(4)] for _ in range(6)]
        img_name = f"data/img/{random.choice(os.listdir('data/img'))}"

        draw_grid()
        cut_image(img_name)
        generate_puzzle(state)

        turn = 0
        start_time = datetime.now().replace(microsecond=0)

        while True:
            
            # Re-fill screen with white to remove old text
            screen.fill(WHITE)
            # Draw grid and place tile on screen       
            render_game(img_name, state)
            # Display game number
            game_text = my_font.render(f"Game: {game}", False, (0, 0, 0))
            screen.blit (game_text, (360, 10))
            # Calculate and display elapsed time
            now_time = datetime.now().replace(microsecond=0)
            time_elapsed = now_time - start_time
            time_text = my_font.render(f"{time_elapsed}", False, (0, 0, 0))
            screen.blit(time_text, (668, 550))
            # Print number of turn
            turn_text = my_font.render(f"Moves: {turn}", False, (0, 0, 0))
            screen.blit(turn_text, (40, 550))

            # Listen for game window event
            for event in pygame.event.get():
                # Quit game and close window
                if event.type == pygame.QUIT:
                    try:
                       rmtree('data/temp')
                    except FileNotFoundError:
                        pass
                    pygame.quit()
                    sys.exit()

                # If there is a mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if move_tile(state, x, y): 
                        turn += 1  

            # Check if game is won
            if state == win:
                win_text = my_font.render(f"You won! Wanna play again?", False, (0, 0, 0))
                yes = my_font.render("(YES)", False, (0, 0, 0))
                no = my_font.render("(NO)", False, (0, 0, 0))   
                screen.blit(win_text, (200, 550))
                screen.blit(yes, (460, 550))
                screen.blit(no, (530, 550))

                if yes.get_rect(topleft = (460, 550)).collidepoint(x, y):
                    game += 1
                    break

                if no.get_rect(topleft = (530, 550)).collidepoint(x, y):
                    try:
                       rmtree('data/temp')
                    except FileNotFoundError:
                        pass
                    pygame.quit()
                    sys.exit()        
                
            pygame.display.update()

if __name__ == '__main__':
    main()