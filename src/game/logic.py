import pygame
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.world_width = 1600
        self.world_height = 1200
        self.player = None
        self.farm = None
        self.resources = {}
        self.is_running = True
        self.in_barn = False  # Track if the player is inside the barn
        self.show_inventory = False  # Toggle for showing inventory

        # Define world objects
        # Expanded farm field (grassy area) at position (50, 400), 10x current size.
        self.farm_field_rect = pygame.Rect(50, 400, 7000, 1500)
        # Barn exterior remains the same
        self.barn_rect = pygame.Rect(600, 350, 100, 100)
        # Define barn door on the exterior (for entering barn)
        self.barn_door_rect = pygame.Rect(640, 410, 20, 30)
        # Barn interior boundaries (local coordinates)
        self.barn_interior_rect = pygame.Rect(0, 0, 400, 300)

    def start(self):
        print("Game started!")
        # Place the player in the center of the world.
        self.player = Player(self.world_width // 2, self.world_height // 2)
        self.farm = Farm()
        self.farm.generate_seeds(10)  # Generate 10 seeds randomly within the farm field
        # Generate chickens to roam inside the barn
        self.farm.generate_chickens(3)
        print("Game started. Welcome to the sustainable farming game!")

    def handle_input(self, event):
        if not self.in_barn:
            # World mode controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.vx = -5
                elif event.key == pygame.K_RIGHT:
                    self.player.vx = 5
                elif event.key == pygame.K_UP:
                    self.player.vy = -5
                elif event.key == pygame.K_DOWN:
                    self.player.vy = 5
                elif event.key == pygame.K_e:
                    # Try to enter barn if near the door
                    player_rect = pygame.Rect(self.player.x - 20, self.player.y - 20, 40, 40)
                    if player_rect.colliderect(self.barn_door_rect):
                        self.enter_barn()
                elif event.key == pygame.K_i:
                    # Toggle the inventory display
                    self.show_inventory = not self.show_inventory
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.vx = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.player.vy = 0
        else:
            # Barn interior controls (simpler boundaries)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.vx = -3
                elif event.key == pygame.K_RIGHT:
                    self.player.vx = 3
                elif event.key == pygame.K_UP:
                    self.player.vy = -3
                elif event.key == pygame.K_DOWN:
                    self.player.vy = 3
                elif event.key == pygame.K_e:
                    self.exit_barn()
                elif event.key == pygame.K_i:
                    self.show_inventory = not self.show_inventory
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.vx = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.player.vy = 0

    def update(self):
        # Move the player
        self.player.x += self.player.vx
        self.player.y += self.player.vy

        if not self.in_barn:
            # World mode: constrain movement to world boundaries.
            self.player.x = max(0, min(self.world_width, self.player.x))
            self.player.y = max(0, min(self.world_height, self.player.y))
            # Check collision with seeds for pickup.
            for seed in self.farm.seeds[:]:
                seed_rect = pygame.Rect(seed.x - 5, seed.y - 5, 10, 10)
                player_rect = pygame.Rect(self.player.x - 20, self.player.y - 20, 40, 40)
                if player_rect.colliderect(seed_rect):
                    print("Picked up a seed!")
                    self.player.inventory.append(seed)
                    self.farm.seeds.remove(seed)
        else:
            # Barn mode: constrain movement to barn interior.
            self.player.x = max(0, min(self.barn_interior_rect.width, self.player.x))
            self.player.y = max(0, min(self.barn_interior_rect.height, self.player.y))
            # Update chicken movement with a simple random walk.
            for chicken in self.farm.chickens:
                if random.random() < 0.02:
                    chicken.vx = random.choice([-2, -1, 0, 1, 2])
                    chicken.vy = random.choice([-2, -1, 0, 1, 2])
                chicken.x += chicken.vx
                chicken.y += chicken.vy
                chicken.x = max(0, min(self.barn_interior_rect.width, chicken.x))
                chicken.y = max(0, min(self.barn_interior_rect.height, chicken.y))

    def render(self):
        if not self.in_barn:
            screen_width, screen_height = self.screen.get_size()
            # Calculate camera offset so the player is centered.
            camera_x = self.player.x - screen_width // 2
            camera_y = self.player.y - screen_height // 2
            camera_x = max(0, min(camera_x, self.world_width - screen_width))
            camera_y = max(0, min(camera_y, self.world_height - screen_height))
            self.screen.fill((135, 206, 235))
            farm_field = self.farm_field_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(self.screen, (34, 139, 34), farm_field)
            barn = self.barn_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(self.screen, (178, 34, 34), barn)
            door = self.barn_door_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(self.screen, (0, 0, 0), door)
            for seed in self.farm.seeds:
                pygame.draw.circle(self.screen, (139, 69, 19), (seed.x - camera_x, seed.y - camera_y), 5)
            # Draw the player as a stick figure.
            self.draw_stick_figure(self.screen, self.player.x - camera_x, self.player.y - camera_y, (255, 215, 0))
        else:
            # Barn interior rendering.
            self.screen.fill((200, 200, 200))
            door_rect = pygame.Rect(180, 270, 40, 30)
            pygame.draw.rect(self.screen, (0, 0, 0), door_rect)
            # Draw chickens (a simple circle for each chicken).
            for chicken in self.farm.chickens:
                pygame.draw.circle(self.screen, (255, 165, 0), (int(chicken.x), int(chicken.y)), 8)
            # Draw the player as a stick figure.
            self.draw_stick_figure(self.screen, self.player.x, self.player.y, (255, 215, 0))

        # Draw inventory overlay if enabled.
        if self.show_inventory:
            font = pygame.font.SysFont(None, 24)
            inventory_text = f"Seeds: {len(self.player.inventory)}"
            text_surf = font.render(inventory_text, True, (255, 255, 255))
            panel_rect = pygame.Rect(10, 10, 160, 40)
            pygame.draw.rect(self.screen, (0, 0, 0), panel_rect)
            self.screen.blit(text_surf, (15, 20))

    def draw_stick_figure(self, surface, x, y, color):
        """
        Draw a simple stick figure.
        'x, y' is the base (feet) position.
        """
        # Head (centered above the body)
        head_center = (x, y - 50)
        pygame.draw.circle(surface, color, head_center, 10, 2)
        # Body
        body_top = (x, y - 40)
        body_bottom = (x, y - 10)
        pygame.draw.line(surface, color, body_top, body_bottom, 2)
        # Arms
        left_arm_end = (x - 15, y - 25)
        right_arm_end = (x + 15, y - 25)
        pygame.draw.line(surface, color, (x, y - 35), left_arm_end, 2)
        pygame.draw.line(surface, color, (x, y - 35), right_arm_end, 2)
        # Legs
        left_leg_end = (x - 10, y)
        right_leg_end = (x + 10, y)
        pygame.draw.line(surface, color, body_bottom, left_leg_end, 2)
        pygame.draw.line(surface, color, body_bottom, right_leg_end, 2)

    def enter_barn(self):
        print("Entering barn...")
        self.in_barn = True
        # Set player to an interior starting position.
        self.player.x, self.player.y = 200, 150
        self.player.vx, self.player.vy = 0, 0

    def exit_barn(self):
        print("Exiting barn...")
        self.in_barn = False
        self.player.x, self.player.y = self.barn_door_rect.center
        self.player.vx, self.player.vy = 0, 0

class Player:
    def __init__(self, x, y):
        self.name = ""
        self.resources = {}
        self.inventory = []  # Holds seeds or future items.
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

    def set_name(self, name):
        self.name = name

class Farm:
    def __init__(self):
        self.crops = []
        self.animals = []
        self.seeds = []       # List of seeds on the ground.
        self.chickens = []    # List of chickens in the barn.

    def plant_crop(self, crop):
        self.crops.append(crop)

    def raise_animal(self, animal):
        self.animals.append(animal)

    def generate_seeds(self, count):
        for _ in range(count):
            x = 50 + int(random.random() * 7000)
            y = 400 + int(random.random() * 1500)
            self.seeds.append(Seed(x, y))

    def generate_chickens(self, count):
        for _ in range(count):
            # Place chickens inside the barn interior randomly.
            x = random.randint(0, 400)
            y = random.randint(0, 300)
            self.chickens.append(Chicken(x, y))

class Seed:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Chicken:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Set an initial random velocity.
        self.vx = random.choice([-2, -1, 0, 1, 2])
        self.vy = random.choice([-2, -1, 0, 1, 2])

import pygame
from game.logic import Game
import traceback

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sustainable Farming Game")
    game = Game(screen)
    game.start()

    running = True
    clock = pygame.time.Clock()

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                game.handle_input(event)

            game.update()
            game.render()
            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()