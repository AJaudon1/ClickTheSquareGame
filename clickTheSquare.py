# Alston Jaudon
# Click The Square Game

import pygame
import random
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("How_Far.mp3")
pygame.mixer.music.play(-1)

#Game settings
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Click the Square")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
square_size = 100


#used for changing logo colors
left_poly_color = "White"
right_poly_color = "White"
top_poly_color = "White"
change_interval = 2650
last_time = pygame.time.get_ticks()

#class for easily making buttons
class Button:
    def __init__(self, x, y, width, height, text, font, color):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, "Black")
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surface.get_rect(center = self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def change_color(self, color):
        self.color = color

    def is_on(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

#Difficulty based on set grid_size
grid_size = 3

#function to draw the main game grid
#def draw_grid(grid_size):
    #

# game loop
game_running = True

#initialize menu buttons
start_button = Button(480, 360, 320, 54, "Start", font, "White")

settings_button = Button(480, 468, 320, 54, "Settings", font, "White")

info_button = Button(480, 576, 320, 54, "Info", font, "White")

button_hover = False

while game_running:
    screen.fill("black")

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
                game_running = False
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


    #draw menu buttons and text
    #start_button = pygame.draw.rect(screen, "White", (480, 360, 320, 54))
    #start_text = font.render("Start", True, "Black")
    #start_rect = start_text.get_rect(center=start_button.center)
    #screen.blit(start_text, start_rect)

    #settings_button = pygame.draw.rect(screen, "White", (480, 468, 320, 54))
    #settings_text = font.render("Settings", True, "Black")
    #settings_rect = settings_text.get_rect(center=settings_button.center)
    #screen.blit(settings_text, settings_rect)

    #info_button = pygame.draw.rect(screen, "White", (480, 576, 320, 54))
    #info_text = font.render("Info", True, "black")
    #info_rect = info_text.get_rect(center=info_button.center)
    #screen.blit(info_text, info_rect)

    #check for menu clicks


    #30 fps
    pygame.display.flip()
    clock.tick(30)

#close the game
pygame.quit()


