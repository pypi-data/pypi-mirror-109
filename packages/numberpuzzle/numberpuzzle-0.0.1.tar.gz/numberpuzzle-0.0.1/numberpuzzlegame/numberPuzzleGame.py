import pygame
import random

grid_size = int(input('choose a difficulty 4-16: '))
square_size = 50
scnsize = grid_size * square_size
numbers = []
scramblednumbers = []
squares = []

pygame.init()
screen = pygame.display.set_mode((scnsize, scnsize))

class Square():
    def __init__(self, x, y, size, number, is_zero = False, color = (255,0,255)):
        self.x = x
        self.y = y
        self.size = size
        self.number = number
        self.is_zero = is_zero
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size), 1)
        def draw_text(surf, text, size, x, y, is_zero):
            font_name = pygame.font.match_font('arial')
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, (255, 255, 255))
            if is_zero:
                text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            surf.blit(text_surface, text_rect)
        draw_text(screen, str(self.number), 30, self.x + 25, self.y + 7, self.is_zero)

    def move(self, squares, index):    
        temp = self.number        
        self.number = squares[index].number 
        self.is_zero = True
        squares[index].number = temp
        squares[index].is_zero = False


def setup_grid():    
    
    # Create scrambled numbers
    numbers = list(range(1, grid_size ** 2))
    for num in range(grid_size**2 - 1):
        chosen_num = random.choice(numbers)
        scramblednumbers.append(chosen_num)
        numbers.remove(chosen_num)
    
    #Create squares
    for i in range(grid_size ** 2 - 1): 
        x = (i % grid_size) * square_size
        y = (i // grid_size) * square_size  
        number = scramblednumbers[i]            
        square = Square(x, y, square_size, number) 
        squares.append(square)
    square = Square ((grid_size-1) * square_size, (grid_size-1) * square_size, square_size, 0, is_zero=True)
    squares.append(square)
    return squares
            
squares = setup_grid()

run = True
while run:
    screen.fill((0,0,0))
    for square in squares:
        square.draw()
    pygame.display.update()
    for index,square in enumerate(squares):
        if square.number == 0:
            empty_square_index = index
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for index, square in enumerate(squares):
                    if square.x - square_size == squares[empty_square_index].x and square.y == squares[empty_square_index].y:
                        square.move(squares, empty_square_index)
            if event.key == pygame.K_RIGHT:
                for index, square in enumerate(squares):
                    if square.x + square_size == squares[empty_square_index].x and square.y == squares[empty_square_index].y:
                        square.move(squares, empty_square_index)
            if event.key == pygame.K_UP:
                for index, square in enumerate(squares):
                    if square.x  == squares[empty_square_index].x and square.y - square_size == squares[empty_square_index].y:
                        square.move(squares, empty_square_index)
            if event.key == pygame.K_DOWN:
                for index, square in enumerate(squares):
                    if square.x  == squares[empty_square_index].x and square.y + square_size == squares[empty_square_index].y:
                        square.move(squares, empty_square_index)


    
