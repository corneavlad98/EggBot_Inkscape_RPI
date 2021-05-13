import pygame

pygame.init()

# Define some colors
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Eggbot Main Menu")

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Main menu
# This screen will be seen by the player when entering the game
# It includes a PLAY button, QUIT button and a fancy name animation above them
def game_intro():
    intro = True
    y = 245
    color = RED
    while intro:
       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            
        
        screen.fill(DARKBLUE)

        font = pygame.font.SysFont("Georgia", 120, True)
        buttonFont = pygame.font.SysFont("Georgia", 36, True)

        title_text = font.render("Eggbot", True, color)
        title_text_shade = font.render("Eggbot", True, BLACK)

        template1Text = buttonFont.render("Template 1", True, BLACK)
        template2Text = buttonFont.render("Template 2", True, BLACK)
        template3Text = buttonFont.render("Template 3", True, BLACK)

        screen.blit(title_text_shade, (176, 58))
        screen.blit(title_text_shade, (176, 62))
        screen.blit(title_text, (180, 60))
      

        # selectRect = pygame.Rect(245, y, 310, 90)
        # pygame.draw.rect(screen, WHITE, selectRect)

        template1 = pygame.draw.rect(screen, GREEN, (50, 250, 220, 80))
        template2 = pygame.draw.rect(screen, GREEN, (300, 250, 220, 80))
        template3 = pygame.draw.rect(screen, GREEN, (550, 250, 220, 80))

        screen.blit(template1Text, (58, 265))      
        screen.blit(template2Text, (308, 265))
        screen.blit(template3Text, (558, 265))

        settingsButton = pygame.draw.rect(screen, YELLOW, (300, 350, 220, 80))
        quitButton = pygame.draw.rect(screen, RED, (300, 450, 220, 80))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y = 245
        if keys[pygame.K_DOWN]:
            y = 335
        if keys[pygame.K_RETURN]:
            if y == 245:
                intro = False
            elif y == 335:
                quit()

        pygame.display.update()
        clock.tick(60)



while True:
    game_intro()

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
