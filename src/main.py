import pygame
from game.logic import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sustainable Farming Game")
    game = Game(screen)  # Pass the screen to the Game instance
    game.start()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        game.update()
        game.render()  
        pygame.display.flip()  # Update the full display surface to the screen
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()