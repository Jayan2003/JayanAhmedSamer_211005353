
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from shape import FallingShape
from basket import draw_basket

# Initialize pygame
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display)
pygame.display.set_caption("Catch the Shapes - Entry")

# Font and color
font = pygame.font.SysFont('Arial', 50)
WHITE = (255, 255, 255)
BLUE = (0, 50, 220)


entry_background = pygame.image.load('images\EntryBackground.png')  

aqua_blue = entry_background.get_at((300, 10))[:3] 
# Function to draw the background image
def draw_entry_background():
    scaled_background = pygame.transform.scale(entry_background, display)
    screen.blit(scaled_background, (0, 0))


# Entry Screen Function
def entry_screen():
    instruction_font = pygame.font.SysFont('Arial', 24)
    
    while True: #Keep Showing the entry_background until the user clicks on play
        draw_entry_background()  
        
        # Title
        title = font.render("Catch the Shapes", True, WHITE)
        screen.blit(title, (220, 100))

        # Instructions
        instructions = [
            "Instructions:",
            "→ Use LEFT and RIGHT arrow keys to move the basket.",
            "→ Catch only the correct shape mentioned at the top.",
            "→ Each correct shape increases your score.",
            "→ Game ends when time runs out or target is met."
        ]
        
        # Takes each instruction and draws it on the screen,
        for i, line in enumerate(instructions):
            text_surface = instruction_font.render(line, True, WHITE)
            screen.blit(text_surface, (100, 180 + i * 30))

        # Play Button
        play_button = pygame.Rect(300, 400, 200, 60)
        pygame.draw.rect(screen, WHITE, play_button)
        play_text = font.render("PLAY", True, aqua_blue)
        screen.blit(play_text, (play_button.x + 40, play_button.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and play_button.collidepoint(event.pos):
                return

# Game Window Setup
def start_game():
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Catch the Shapes")

    # Sounds
    pygame.mixer.init()
    win_sound = pygame.mixer.Sound('sound\winSound.wav')
    lose_sound = pygame.mixer.Sound('sound\loseSound.wav')
    catch_sound = pygame.mixer.Sound('sound\catchSound.wav')

    # Load background music
    pygame.mixer.music.load('sound\BackgroundSound.mp3') 
    pygame.mixer.music.play(-1)  # Loop indefinitely

    # Background Image for the game
    background_image = pygame.image.load(r'images\UNDERWATERTREASURE.png')
    background_texture = glGenTextures(1)

    def load_background():
        texture_data = pygame.image.tostring(background_image, "RGBA", True)
        glBindTexture(GL_TEXTURE_2D, background_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, background_image.get_width(), background_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def draw_background():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, background_texture)
        glColor3f(1, 1, 1)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0);glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(800, 0)
        glTexCoord2f(1, 1); glVertex2f(800, 600)
        glTexCoord2f(0, 1); glVertex2f(0, 600)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

    def setup_2d():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setup_3d():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 10, # Eye/camera position (at z=10)
                  0, 0, 0,  # Look at the origin (center)
                  0, 1, 0) # Up direction is Y-axis

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    load_background()
    font = pygame.font.SysFont('Arial', 30)
    win_font = pygame.font.SysFont('Arial', 60)
    lose_font = pygame.font.SysFont('Arial', 60)

    # Game Variables
    basket_x = 0
    basket_speed = 0.15 #moves 0.15 units every frame
    score = 0
    correct_shape_type = random.choice(["circle", "square", "triangle", "star"])
    target_shapes = random.randint(15, 40)
    shapes = []
    spawn_timer = 0
    spawn_interval = 50
    collected_shapes = 0
    start_ticks = pygame.time.get_ticks() #Start time
    time_limit = 60

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and basket_x > -4.5:
            basket_x -= basket_speed
        if keys[K_RIGHT] and basket_x < 4.5:
            basket_x += basket_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background()

        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            shapes.append(FallingShape(correct_shape_type))
            spawn_timer = 0

        setup_2d()
        basket_screen_x = (basket_x * 100) + 400  # scales the basket's world X-coordinate to match the pixel scale of the screen


        for shape in shapes[:]:
            shape.update()
            basket_width=200
            basket_height=100
            basket_left = basket_screen_x - basket_width/2
            basket_right = basket_screen_x + basket_width/2
            basket_top = 100
            basket_bottom=basket_top-basket_height
            shape_left = shape.x - shape.size/2
            shape_right = shape.x + shape.size/2
            shape_top = shape.y + shape.size/2
            shape_bottom = shape.y - shape.size/2
            if shape_bottom < basket_top and basket_left < shape.x < basket_right:
                catch_sound.play()
                if shape.type == correct_shape_type:
                    collected_shapes += 1
                else:
                    collected_shapes = max(0, collected_shapes - 1)  # Prevent negative score
                shapes.remove(shape)
            elif shape.y < -shape.size:
                shapes.remove(shape)
            else:
                shape.draw()
      
   
        setup_3d()
        draw_basket(basket_x)
        setup_2d()

        seconds_left = max(0, time_limit - (pygame.time.get_ticks() - start_ticks) // 1000)
        timer_surface = font.render(f"Time: {seconds_left}s", True, (255, 255, 255))
        glWindowPos2d(650, 570) #sets the pixel position on the screen
        glDrawPixels(timer_surface.get_width(), timer_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(timer_surface, "RGBA", True))

        collected_surface = font.render(f"Collected: {collected_shapes} / {target_shapes}", True, (255, 255, 255))
        glWindowPos2d(20, 570)
        glDrawPixels(collected_surface.get_width(), collected_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(collected_surface, "RGBA", True))

        shape_surface = font.render(f"Collect: {correct_shape_type.capitalize()}", True, (255, 255, 255))
        glWindowPos2d(20, 530)
        glDrawPixels(shape_surface.get_width(), shape_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(shape_surface, "RGBA", True))

        if collected_shapes >= target_shapes:
            pygame.mixer.music.stop()
            win_surface = win_font.render("You Win!", True, (0, 255, 0))
            glWindowPos2d(300, 300)
            glDrawPixels(win_surface.get_width(), win_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(win_surface, "RGBA", True))
            win_sound.play()
            pygame.display.flip()
            pygame.time.wait(5000)
            break
        elif seconds_left == 0:
            pygame.mixer.music.stop()
            lose_surface = lose_font.render("You Lose!", True, (255, 0, 0))
            glWindowPos2d(300, 300)
            glDrawPixels(lose_surface.get_width(), lose_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(lose_surface, "RGBA", True))
            lose_sound.play()
            pygame.display.flip()
            pygame.time.wait(5000)
            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run
if __name__ == "__main__":
    entry_screen()
    start_game()
