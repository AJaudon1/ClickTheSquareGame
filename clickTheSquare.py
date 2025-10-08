# Alston Jaudon
# Click The Square Game

import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game settings
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Click the Square")
# 2 font sizes to choose from
font1 = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 56)
clock = pygame.time.Clock()

# Global settings
music_enabled = True
grid_size = 5

# class for making menu buttons
class Button:
    def __init__(self, x, y, width, height, text, text_color, font, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, text_color)
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def change_color(self, color):
        self.color = color

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)

    def is_on(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# class used for the squares in the game
class Square:
    def __init__(self, x, y, width, color):
        self.rect = pygame.Rect(x, y, width, width)
        self.color = color
        self.is_target = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def change_color(self, color):
        self.color = color

    def is_on(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# class used for the in-game timer
class Timer:
    def __init__(self, total_time, font, position):
        self.time_left = total_time  # In milliseconds
        self.font = font
        self.position = position
        self.last_update = pygame.time.get_ticks()
        self.running = False

    def start(self):
        self.running = True
        self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.running == False:
            return
        cur_time = pygame.time.get_ticks()
        time_change = cur_time - self.last_update
        self.time_left -= time_change
        self.time_left = max(0, self.time_left)
        self.last_update = cur_time

    def add_time(self, milliseconds):
        self.time_left += milliseconds

    def out_of_time(self):
        if (self.time_left <= 0):
            return True
        else:
            return False

    def draw(self, screen):
        seconds = self.time_left / 1000.0
        timer_text = self.font.render(f"Time: {seconds:.3f}", True, "White")
        screen.blit(timer_text, self.position)

# function to draw the main game grid
# grid will be approximately 640 x 640 pixels
def draw_grid(grid_size):
    grid = []
    set_width = (640 / grid_size) * 0.75
    xy_adjust = (640 / grid_size) * 0.25

    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            # convert float values to integers for the position
            x = int(350 + col * set_width + col * xy_adjust)
            y = int(70 + row * set_width + row * xy_adjust)

            # creates one square to add to the grid row
            square = Square(x, y, int(set_width), "White")
            grid_row.append(square)
        # adds single row to the grid
        grid.append(grid_row)
    return grid

def rand_index(grid_size):
    num = random.randint(0, grid_size - 1)
    return num

# Main gameplay function
def play_game(grid_size):
    global music_enabled
    
    if music_enabled:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Audio/Seeing_Squares.mp3")
        pygame.mixer.music.play(-1)
    
    # Game initialization
    game_grid = []
    game_grid = draw_grid(grid_size)
    points = 0
    level = 1
    squares_per_level = 20  # Increase level every 20 correct clicks

    # before starting the game, create a game timer with 5 seconds
    game_timer = Timer(5000, font2, (1000, 100))
    timer_on = False

    # Creates a timed countdown with text
    countdown_int = 1000
    countdown_last = pygame.time.get_ticks()
    countdown_cur = pygame.time.get_ticks()
    ready = Button(520, 340, 40, 40, "Ready...", "White", font2, "Black")
    set_btn = Button(645, 340, 40, 40, "Set...", "White", font2, "Black")
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
            # increment counter and reset timer
            num += 1
            countdown_last = countdown_cur

        # check for the text to display
        if num == 1:
            set_on = True
        elif num == 2:
            go_on = True
        elif num == 3:
            in_countdown = False

        # draw countdown text if able
        if ready_on:
            ready.draw(screen)
        if set_on:
            set_btn.draw(screen)
        if go_on:
            go.draw(screen)

        game_timer.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    target_on = False
    start_game = True

    while start_game:
        screen.fill("Black")

        # turn on a target if there isn't one
        if target_on == False:
            row = rand_index(grid_size)
            col = rand_index(grid_size)
            game_grid[row][col].is_target = True
            game_grid[row][col].change_color("Red")
            target_on = True

        # draw grid each frame
        for row in range(grid_size):
            for col in range(grid_size):
                game_grid[row][col].draw(screen)

        # start timer and draw remaining time each frame
        if timer_on == False:
            game_timer.start()
            timer_on = True

        game_timer.update()
        game_timer.draw(screen)

        # Display current level and score
        level_text = font1.render(f"Level: {level}", True, "White")
        score_text = font1.render(f"Score: {points}", True, "White")
        screen.blit(level_text, (1010, 150))
        screen.blit(score_text, (1010, 190))

        # check for click events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", points
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # iterate through the grid to find the clicked square
                for row in range(grid_size):
                    for col in range(grid_size):
                        if game_grid[row][col].is_on(pygame.mouse.get_pos()):
                            if game_grid[row][col].is_target == True:
                                points += 1
                                level = (points // squares_per_level) + 1

                                # Progressive time bonus - decreases as level increases
                                # Starts at 750ms, minimum 200ms
                                time_bonus = max(200, 750 - (level - 1) * 50)
                                game_timer.add_time(time_bonus)

                                game_grid[row][col].is_target = False
                                game_grid[row][col].change_color("Green")
                                game_grid[row][col].draw(screen)
                                pygame.display.flip()
                                pygame.time.wait(200)
                                game_grid[row][col].change_color("White")
                                target_on = False
                            else:
                                start_game = False
                                
        # check if time has run out
        if game_timer.out_of_time():
            start_game = False

        # grid updates at 30 fps
        pygame.display.flip()
        clock.tick(30)

    # Game over - return to end screen
    if music_enabled:
        pygame.mixer.music.stop()
    return "game_over", points, level

# End game screen
def show_end_game_screen(points, level):
    global music_enabled
    
    show_end_screen = True
    play_again_button = Button(440, 450, 180, 54, "Play Again", "Black", font1, "White")
    main_menu_button = Button(660, 450, 180, 54, "Main Menu", "Black", font1, "White")

    button_hover = False

    while show_end_screen:
        screen.fill("Black")

        # Display final score and level
        game_over_text = font2.render("Game Over!", True, "White")
        score_text = font2.render(f"Final Score: {points}", True, "White")
        level_text = font1.render(f"Level Reached: {level}", True, "White")

        screen.blit(game_over_text, (530, 200))
        screen.blit(score_text, (515, 280))
        screen.blit(level_text, (545, 340))

        if button_hover == False:
            play_again_button.change_color("White")
            main_menu_button.change_color("White")

        play_again_button.draw(screen)
        main_menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_on(pygame.mouse.get_pos()):
                    return "play_again"

                elif main_menu_button.is_on(pygame.mouse.get_pos()):
                    return "main_menu"

            elif event.type == pygame.MOUSEMOTION:
                if play_again_button.is_on(pygame.mouse.get_pos()):
                    play_again_button.change_color("Light Gray")
                    button_hover = True
                elif main_menu_button.is_on(pygame.mouse.get_pos()):
                    main_menu_button.change_color("Light Gray")
                    button_hover = True
                else:
                    button_hover = False

        pygame.display.flip()
        clock.tick(30)

# Settings menu
def show_settings_menu():
    global music_enabled, grid_size

    settings_menu = True

    # Create settings menu buttons
    settings_back = Button(50, 50, 150, 50, "Main Menu", "Black", font1, "White")
    music_toggle = Button(440, 200, 400, 54, f"Music: {'ON' if music_enabled else 'OFF'}", "Black", font1, "White")

    # Grid size buttons
    grid_3x3 = Button(360, 360, 120, 54, "3x3", "Black", font1, "Light Gray" if grid_size == 3 else "White")
    grid_4x4 = Button(500, 360, 120, 54, "4x4", "Black", font1, "Light Gray" if grid_size == 4 else "White")
    grid_5x5 = Button(640, 360, 120, 54, "5x5", "Black", font1, "Light Gray" if grid_size == 5 else "White")
    grid_6x6 = Button(780, 360, 120, 54, "6x6", "Black", font1, "Light Gray" if grid_size == 6 else "White")

    grid_label = Button(640, 320, 5, 5, "Grid Size:", "White", font2, "Black")

    button_hover = False

    while settings_menu:
        screen.fill("Black")

        if button_hover == False:
            settings_back.change_color("White")
            music_toggle.change_color("White")

        # Draw all buttons
        settings_back.draw(screen)
        music_toggle.draw(screen)
        grid_label.draw(screen)
        grid_3x3.draw(screen)
        grid_4x4.draw(screen)
        grid_5x5.draw(screen)
        grid_6x6.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if settings_back.is_on(pygame.mouse.get_pos()):
                    return "main_menu"

                elif music_toggle.is_on(pygame.mouse.get_pos()):
                    music_enabled = not music_enabled
                    if music_enabled:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                    music_toggle.update_text(f"Music: {'ON' if music_enabled else 'OFF'}")

                # Grid size selection
                elif grid_3x3.is_on(pygame.mouse.get_pos()):
                    grid_size = 3
                    grid_3x3.change_color("Light Gray")
                    grid_4x4.change_color("White")
                    grid_5x5.change_color("White")
                    grid_6x6.change_color("White")
                elif grid_4x4.is_on(pygame.mouse.get_pos()):
                    grid_size = 4
                    grid_3x3.change_color("White")
                    grid_4x4.change_color("Light Gray")
                    grid_5x5.change_color("White")
                    grid_6x6.change_color("White")
                elif grid_5x5.is_on(pygame.mouse.get_pos()):
                    grid_size = 5
                    grid_3x3.change_color("White")
                    grid_4x4.change_color("White")
                    grid_5x5.change_color("Light Gray")
                    grid_6x6.change_color("White")
                elif grid_6x6.is_on(pygame.mouse.get_pos()):
                    grid_size = 6
                    grid_3x3.change_color("White")
                    grid_4x4.change_color("White")
                    grid_5x5.change_color("White")
                    grid_6x6.change_color("Light Gray")

            elif event.type == pygame.MOUSEMOTION:
                if settings_back.is_on(pygame.mouse.get_pos()) or music_toggle.is_on(pygame.mouse.get_pos()):
                    button_hover = True
                    if settings_back.is_on(pygame.mouse.get_pos()):
                        settings_back.change_color("Light Gray")
                    if music_toggle.is_on(pygame.mouse.get_pos()):
                        music_toggle.change_color("Light Gray")
                else:
                    button_hover = False

        pygame.display.flip()
        clock.tick(30)

# Info menu
def show_info_menu():
    info_menu = True

    go_back = Button(50, 50, 150, 50, "Main Menu", "Black", font1, "White")

    correct_square = Square(300, 100, 200, "Red")
    wrong_square = Square(700, 100, 200, "White")

    correct_text = Button(300, 360, 5, 5, "Click these!", "White", font1, "Black")
    wrong_text = Button(900, 360, 5, 5, "Don't click these!", "White", font1, "Black")

    info_line1 = Button(600, 420, 5, 5, "When a square lights up red, click it!", "White", font1, "Black")
    info_line2 = Button(600, 480, 5, 5, "Clicking the correct square adds time to the clock", "White", font1, "Black")
    info_line3 = Button(600, 540, 5, 5, "Be wary of your time limit; higher levels add less time", "White", font1, "Black")
    info_line4 = Button(600, 600, 5, 5, "How far can you go?", "White", font1, "Black")
    info_timer = Timer(5000, font2, (1000, 100))

    button_hover_info = False

    # info menu loop, click go_back to return to the main menu
    while info_menu:
        screen.fill("Black")

        # button hover
        if button_hover_info == False:
            go_back.change_color("White")

        # draw buttons every frame
        correct_square.draw(screen)
        wrong_square.draw(screen)
        correct_text.draw(screen)
        wrong_text.draw(screen)
        go_back.draw(screen)
        arrow1 = pygame.draw.line(screen, "Light Gray", (300, 340), (380, 280), 2)
        arrow2 = pygame.draw.line(screen, "Light Gray", (870, 340), (790, 280), 2)
        info_line1.draw(screen)
        info_line2.draw(screen)
        info_line3.draw(screen)
        info_line4.draw(screen)
        info_timer.draw(screen)

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if go_back.is_on(pygame.mouse.get_pos()):
                    return "main_menu"

            elif event.type == pygame.MOUSEMOTION:
                if go_back.is_on(pygame.mouse.get_pos()):
                    go_back.change_color("Light Gray")
                    button_hover_info = True
                else:
                    button_hover_info = False

        pygame.display.flip()
        clock.tick(30)

# Main menu
def main_menu():
    global music_enabled
    
    # used for changing logo colors
    left_poly_color = "White"
    right_poly_color = "White"
    top_poly_color = "White"
    change_interval = 2650
    last_time = pygame.time.get_ticks()

    # initialize menu buttons
    start_button = Button(480, 360, 320, 54, "Start", "Black", font1, "White")
    info_button = Button(480, 450, 320, 54, "How to Play", "Black", font1, "White")
    settings_button = Button(480, 540, 320, 54, "Settings", "Black", font1, "White")
    quit_button = Button(480, 630, 320, 54, "Quit", "Black", font1, "White")

    button_hover = False

    # initialize game music
    pygame.mixer.init()
    if music_enabled:
        pygame.mixer.music.load("Audio/How_Far.mp3")
        pygame.mixer.music.play(-1)

    game_running = True

    while game_running:
        screen.fill("black")

        # turn on main menu music if off
        if music_enabled and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("Audio/How_Far.mp3")
            pygame.mixer.music.play(-1)

        # if mouse is not over buttons
        if button_hover == False:
            start_button.change_color("White")
            settings_button.change_color("White")
            info_button.change_color("White")
            quit_button.change_color("White")

        # draw buttons every frame
        start_button.draw(screen)
        settings_button.draw(screen)
        info_button.draw(screen)
        quit_button.draw(screen)

        # check for events
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                game_running = False

            # check clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_on(pygame.mouse.get_pos()):
                    result = play_game(grid_size)
                    if result[0] == "quit":
                        game_running = False
                    elif result[0] == "game_over":
                        points = result[1]
                        level = result[2]
         
                        # Show end game screen
                        while True:
                            end_result = show_end_game_screen(points, level,)
                            if end_result == "quit":
                                game_running = False
                                break
                            elif end_result == "play_again":
                                result = play_game(grid_size)
                                if result[0] == "quit":
                                    game_running = False
                                    break
                                elif result[0] == "game_over":
                                    points = result[1]
                                    level = result[2]
                                    continue
                            elif end_result == "main_menu":
                                # Restart main menu music
                                if music_enabled:
                                    pygame.mixer.music.load("Audio/How_Far.mp3")
                                    pygame.mixer.music.play(-1)
                                break

                elif info_button.is_on(pygame.mouse.get_pos()):
                    result = show_info_menu()
                    if result == "quit":
                        game_running = False

                elif settings_button.is_on(pygame.mouse.get_pos()):
                    result = show_settings_menu()
                    if result == "quit":
                        game_running = False

                elif quit_button.is_on(pygame.mouse.get_pos()):
                    game_running = False

            # check mouse location and highlight buttons
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
                elif quit_button.is_on(pygame.mouse.get_pos()):
                    quit_button.change_color("Light Gray")
                    button_hover = True
                else:
                    button_hover = False

        # draw a 3d square logo
        left_poly_frame = pygame.draw.polygon(screen, "Black", ((640, 300), (640, 200), (560, 163), (560, 263)), 5)
        left_poly_fill = pygame.draw.polygon(screen, left_poly_color, ((638, 298), (638, 198), (562, 165), (562, 263)))

        right_poly_frame = pygame.draw.polygon(screen, "Black", ((640, 300), (640, 200), (720, 163), (720, 263)), 5)
        right_poly_fill = pygame.draw.polygon(screen, right_poly_color, ((642, 298), (642, 198), (718, 161), (718, 261)))

        top_poly_frame = pygame.draw.polygon(screen, "Black", ((640, 200), (720, 163), (640, 124), (560, 163)), 5)
        top_poly_fill = pygame.draw.polygon(screen, top_poly_color, ((640, 198), (718, 163), (640, 126), (562, 163)))

        # logo polygons changing color
        current_time = pygame.time.get_ticks()
        if current_time - last_time >= change_interval:
            chosen_poly = random.randint(0, 2)
            # left case
            if (chosen_poly == 0):
                if (left_poly_color == "White"):
                    left_poly_color = "Red"
                    right_poly_color = "White"
                    top_poly_color = "White"
                else:
                    left_poly_color = "White"
                    right_poly_color = "Red"
            # right case
            elif (chosen_poly == 1):
                if (right_poly_color == "White"):
                    right_poly_color = "Red"
                    top_poly_color = "White"
                    left_poly_color = "White"
                else:
                    right_poly_color = "White"
                    top_poly_color = "Red"
            # top case
            else:
                if (top_poly_color == "White"):
                    top_poly_color = "Red"
                    left_poly_color = "White"
                    right_poly_color = "White"
                else:
                    top_poly_color = "White"
                    left_poly_color = "Red"
            # reset timer
            last_time = current_time

        # 30 fps
        pygame.display.flip()
        clock.tick(30)

# Run the game
if __name__ == "__main__":
    main_menu()
    pygame.quit()
