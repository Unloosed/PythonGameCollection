import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Path to resource directory
RESOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "pollen_collector")

# Load images
images = {
    "bee": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "bee.png")), (50, 50)),
    "pollen": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "pollen.png")), (30, 30)),
    "raindrop": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "raindrop.png")), (20, 50)),
    "background": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "rainy_background.png")), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "gust_of_wind": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "gust_of_wind.png")), (30, 30)),
    "honey": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "honey.png")), (30, 30)),
    "focus": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "focus.png")), (30, 30)),
    "bounty": pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE_PATH, "bounty.png")), (30, 30))
}

# Timer settings
TIME_LIMIT = 30  # seconds

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bee Pollen Collector")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 35)
        self.running = True
        self.score = 0
        self.time_left = TIME_LIMIT
        self.start_ticks = pygame.time.get_ticks()
        self.additional_time = 0  # Track additional time from power-ups

        self.player = Player()
        self.collectible = Collectible()
        self.obstacles = [Obstacle() for _ in range(5)]
        self.power_ups = []

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

    def handle_events(self):
        """Handle user input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT + 1:
                self.player.speed = self.player.original_speed
            elif event.type == pygame.USEREVENT + 2:
                for obstacle in self.obstacles:
                    obstacle.speed = obstacle.original_speed

    def update(self):
        """Update game state."""
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.check_collision()
        self.update_timer()
        self.spawn_power_up()
        self.update_obstacles()
        self.update_power_ups()

    def check_collision(self):
        """Check for collisions between player and other objects."""
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.reposition()
            self.score += 1

        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                self.running = False
                self.game_over()

    def update_timer(self):
        """Update the game timer."""
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.time_left = TIME_LIMIT - int(seconds) + self.additional_time
        if self.time_left <= 0:
            self.running = False
            self.game_over()

    def spawn_power_up(self):
        """Spawn power-ups randomly."""
        if random.randint(1, 100) <= 1:  # 1% chance to spawn a power-up each frame
            power_up_type = random.choice(["gust_of_wind", "honey", "focus", "bounty"])
            self.power_ups.append(PowerUp(power_up_type))

    def update_obstacles(self):
        """Update the position of obstacles."""
        for obstacle in self.obstacles:
            obstacle.move()

    def update_power_ups(self):
        """Update the position of power-ups and apply effects."""
        for power_up in self.power_ups:
            power_up.move()
            if self.player.rect.colliderect(power_up.rect):
                power_up.apply_effect(self)
                self.power_ups.remove(power_up)

    def draw(self):
        """Draw all game elements on the screen."""
        self.screen.blit(images["background"], (0, 0))
        self.player.draw(self.screen)
        self.collectible.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        self.draw_score_and_timer()
        pygame.display.flip()

    def draw_score_and_timer(self):
        """Draw the score and timer on the screen."""
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))
        timer_text = self.font.render("Time: " + str(self.time_left), True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

    def game_over(self):
        """Display the game over screen."""
        self.screen.fill(WHITE)
        game_over_text = self.font.render("Game Over", True, BLACK)
        score_text = self.font.render("Score: " + str(self.score), True, BLACK)
        play_again_text = self.font.render("Press R to Restart or Q to Quit", True, BLACK)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        self.wait_for_restart_or_quit()

    def wait_for_restart_or_quit(self):
        """Wait for the player to restart or quit the game."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

class Player:
    def __init__(self):
        self.image = images["bee"]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.original_speed = self.speed

    def move(self, keys):
        """Move the player based on key presses."""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        """Draw the player on the screen."""
        screen.blit(self.image, self.rect.topleft)

class Collectible:
    def __init__(self):
        self.image = images["pollen"]
        self.rect = self.image.get_rect()  # Initialize rect here
        self.reposition()

    def reposition(self):
        """Reposition the collectible to a random location."""
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), random.randint(0, SCREEN_HEIGHT - self.rect.height))

    def draw(self, screen):
        """Draw the collectible on the screen."""
        screen.blit(self.image, self.rect.topleft)

class Obstacle:
    def __init__(self):
        self.image = images["raindrop"]
        self.rect = self.image.get_rect()  # Initialize rect here
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), random.randint(0, SCREEN_HEIGHT - self.rect.height))
        self.speed = random.randint(1, 3)
        self.original_speed = self.speed

    def move(self):
        """Move the obstacle down the screen."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), -self.rect.height)

    def draw(self, screen):
        """Draw the obstacle on the screen."""
        screen.blit(self.image, self.rect.topleft)

class PowerUp:
    def __init__(self, power_up_type):
        self.type = power_up_type
        self.image = images[self.type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (
        random.randint(0, SCREEN_WIDTH - self.rect.width), random.randint(0, SCREEN_HEIGHT - self.rect.height))
        self.duration = 5000  # Duration of power-up effect in milliseconds
        self.start_time = None

    def move(self):
        """Power-ups don't move."""
        pass

    def draw(self, screen):
        """Draw the power-up on the screen."""
        screen.blit(self.image, self.rect.topleft)

    def apply_effect(self, game):
        """Apply the effect of the power-up."""
        self.start_time = pygame.time.get_ticks()
        if self.type == "gust_of_wind":
            game.player.speed *= 1.5
            pygame.time.set_timer(pygame.USEREVENT + 1, self.duration)
        elif self.type == "honey":
            game.additional_time += 3  # Add 3 seconds to the additional time
        elif self.type == "focus":
            for obstacle in game.obstacles:
                obstacle.speed /= 1.5
            pygame.time.set_timer(pygame.USEREVENT + 2, self.duration)
        elif self.type == "bounty":
            game.score += 1  # Double the score for the next pollen collected
            pygame.time.set_timer(pygame.USEREVENT + 3, self.duration)

def start_pollen_collector():
    """Consolidated game start function for use in main.py"""
    game = Game()
    game.run()

if __name__ == "__main__":
    start_pollen_collector()
