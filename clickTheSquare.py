# Alston Jaudon
# Click The Square Game

import pygame
import random
import time

# Initialize pygame
pygame.init()

#Game settings
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Click the Square")
#2 font sizes to choose from
font1 = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 56)
clock = pygame.time.Clock()

#class for easily making menu buttons
class Button:
    def __init__(self, x, y, width, height, text, text_color, font, color):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, text_color)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surface.get_rect(center = self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def change_color(self, color):
        self.color = color

    def is_on(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

#class used for the squares in the game
class Square:
    def __init__(self, x, y, width, color):
        self.rect = pygame.Rect(x,y,width, width)
        self.color = color
        self.is_target = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def change_color(self, color):
        self.color = color

    def is_on(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

#function to draw the main game grid
#grid will be approximately 640 x 640 pixels
def draw_grid(grid_size):
    grid = []
    set_width = (640/grid_size) * 0.75
    xy_adjust = (640/grid_size) * 0.25
    
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            #convert float values to integers for the position
            x = int(350 + col*set_width + col*xy_adjust)
            y = int(70 + row*set_width + row*xy_adjust)

            #creates one square to add to the grid row
            square = Square(x, y, int(set_width), "White")
            grid_row.append(square)
        #adds single row to the grid
        grid.append(grid_row)
    return grid

def rand_index(grid_size):
    num = random.randint(0, grid_size-1)
    return num

#used for testing
def draw_square():
    set_width = (640/grid_size) * 0.75
    xy_adjust = (640/grid_size) * 0.25
    x = int(320)
    y = int(40)
    square = Square(x, y, int(set_width), "White")
    return square


#Difficulty based on set grid_size
grid_size = 5

#used for changing logo colors
left_poly_color = "White"
right_poly_color = "White"
top_poly_color = "White"
change_interval = 2650
last_time = pygame.time.get_ticks()

# game loops
game_running = True
start_game = False

#initialize menu buttons
start_button = Button(480, 360, 320, 54, "Start", "Black", font1, "White")

settings_button = Button(480, 468, 320, 54, "Settings", "Black", font1, "White")

info_button = Button(480, 576, 320, 54, "Info", "Black", font1, "White")

button_hover = False


#initialize game music
pygame.mixer.init()
pygame.mixer.music.load("Audio/How_Far.mp3")
pygame.mixer.music.play(-1)

while game_running:
    screen.fill("black")

    #turn on main menu music if off
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Audio/How_Far.mp3")
        pygame.mixer.music.play(-1)

    #if mouse is not over buttons
    if button_hover == False:
        start_button.change_color("White")
        settings_button.change_color("White")
        info_button.change_color("White")

    #draw buttons every frame
    start_button.draw(screen)
    settings_button.draw(screen)
    info_button.draw(screen)

    #check for events
    for event in pygame.event.get():

        #quit the game
        if event.type == pygame.QUIT:
            game_running = False

        #check clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_on(pygame.mouse.get_pos()):
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Audio/Seeing_Squares.mp3")
                pygame.mixer.music.play(-1)

                #Gameplay starts here
    #----------------------------------------------------------
                game_grid = []
                game_grid = draw_grid(grid_size)
                points = 0

                #Creates a timed countdown with text
                countdown_int = 1000
                countdown_last = pygame.time.get_ticks()
                countdown_cur = pygame.time.get_ticks()
                ready = Button(520, 340, 40, 40, "Ready...", "White", font2, "Black")
                set = Button(645, 340, 40, 40, "Set...", "White", font2, "Black")
                go = Button(740, 340, 40, 40, "Go!!!", "White", font2, "Black")
                ready_on = True
                set_on = False
                go_on = False
                num = 0

                in_countdown = True
                while in_countdown:
                    screen.fill("Black")
                    countdown_cur = pygame.time.get_ticks()
                    if countdown_cur - countdown_last >= countdown_int:
                        #increment counter and reset timer
                        num += 1
                        countdown_last = countdown_cur
                    
                    #check for the text to display
                    if num == 1:
                        set_on = True
                    elif num == 2:
                        go_on = True
                    elif num == 3:
                        in_countdown = False

                    #draw countdown text if able
                    if ready_on:
                        ready.draw(screen)
                    if set_on:
                        set.draw(screen)
                    if go_on:
                        go.draw(screen)

                    pygame.display.flip()
                    clock.tick(30)

                target_on = False
                start_game = True
                while start_game:
                    screen.fill("Black")
                    
                    #turn on a target if there isn't one
                    #Green flash on correct pick freezes game for 5 frames, will affect in-game timer
                    if target_on == False:
                        row = rand_index(grid_size)
                        col = rand_index(grid_size)
                        game_grid[row][col].is_target = True
                        game_grid[row][col].change_color("Red")
                        target_on = True

                    #draw grid each frame
                    for row in range(grid_size):
                        for col in range(grid_size):
                            game_grid[row][col].draw(screen)
                    
                    #check for click events
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #iterate through the grid to find the clicked square
                            for row in range(grid_size):
                                for col in range(grid_size):
                                    if game_grid[row][col].is_on(pygame.mouse.get_pos()):
                                        if game_grid[row][col].is_target == True:
                                            points += 1
                                            game_grid[row][col].is_target = False
                                            game_grid[row][col].change_color("Green")
                                            game_grid[row][col].draw(screen)
                                            pygame.display.flip()
                                            pygame.time.wait(200)
                                            game_grid[row][col].change_color("White")
                                            target_on = False
                                        else:
                                            start_game = False
                                            print("You scored" + str(points) + "points")

                    #grid updates at 30 fps
                    pygame.display.flip()
                    clock.tick(30)
                pygame.mixer.music.stop()
    #----------------------------------------------------------
            elif settings_button.is_on(pygame.mouse.get_pos()):
                game_running = False
            elif info_button.is_on(pygame.mouse.get_pos()):
                game_running = False

        #check mouse location and highlight buttons
        elif event.type == pygame.MOUSEMOTION:
            if start_button.is_on(pygame.mouse.get_pos()):
                start_button.change_color("Light Gray")
                button_hover = True
            elif settings_button.is_on(pygame.mouse.get_pos()):
                settings_button.change_color("Light Gray")
                button_hover = True
            elif info_button.is_on(pygame.mouse.get_pos()):
                info_button.change_color("Light Gray")
                button_hover = True
            else:
                button_hover = False

    #render game here

    #draw a 3d square logo
    left_poly_frame = pygame.draw.polygon(screen, "Black", ((640,300),(640,200),(560,163),(560,263)),5)
    left_poly_fill = pygame.draw.polygon(screen, left_poly_color, ((638,298),(638,198),(562,165),(562,263)))

    right_poly_frame = pygame.draw.polygon(screen, "Black", ((640,300),(640,200),(720,163),(720,263)),5)
    right_poly_fill = pygame.draw.polygon(screen,right_poly_color, ((642,298),(642,198),(718,161),(718,261)))

    top_poly_frame = pygame.draw.polygon(screen, "Black", ((640,200),(720,163),(640,124),(560,163)),5)
    top_poly_fill = pygame.draw.polygon(screen, top_poly_color, ((640,198),(718,163),(640,126),(562,163)))

    #logo polygons changing color
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= change_interval:
        chosen_poly = random.randint(0,2)
        #left case
        if(chosen_poly == 0):
            if(left_poly_color == "White"):
                left_poly_color = "Red"
                right_poly_color = "White"
                top_poly_color = "White"
            else:
                left_poly_color = "White"
                right_poly_color = "Red"
        #right case
        elif(chosen_poly == 1):
            if(right_poly_color == "White"):
                right_poly_color = "Red"
                top_poly_color = "White"
                left_poly_color = "White"
            else:
                right_poly_color = "White"
                top_poly_color = "Red"
        #top case
        else:
            if(top_poly_color == "White"):
                top_poly_color = "Red"
                left_poly_color = "White"
                right_poly_color = "White"
            else:
                top_poly_color = "White"
                left_poly_color = "Red"
        #reset timer
        last_time = current_time

    #30 fps
    pygame.display.flip()
    clock.tick(30)

#close the game
pygame.quit()