import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Path to resource directory
RESOURCE_PATH = "resources/pollen_collector/"

# Load images
bee_image = pygame.image.load(RESOURCE_PATH+"bee.png")
pollen_image = pygame.image.load(RESOURCE_PATH+"pollen.png")
raindrop_image = pygame.image.load(RESOURCE_PATH+"raindrop.png")
background_image = pygame.image.load(RESOURCE_PATH+"rainy_background.png")

# Scale images
bee_image = pygame.transform.scale(bee_image, (50, 50))
pollen_image = pygame.transform.scale(pollen_image, (30, 30))
raindrop_image = pygame.transform.scale(raindrop_image, (20, 50))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

        self.player = Player()
        self.collectible = Collectible()
        self.obstacles = [Obstacle() for _ in range(5)]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.check_collision()
        self.update_timer()
        for obstacle in self.obstacles:
            obstacle.move()

    def check_collision(self):
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.reposition()
            self.score += 1

        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                self.running = False
                self.game_over()

    def update_timer(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.time_left = TIME_LIMIT - int(seconds)
        if self.time_left <= 0:
            self.running = False
            self.game_over()

    def draw(self):
        self.screen.blit(background_image, (0, 0))
        self.player.draw(self.screen)
        self.collectible.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))
        timer_text = self.font.render("Time: " + str(self.time_left), True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))
        pygame.display.flip()

    def game_over(self):
        self.screen.fill(WHITE)
        game_over_text = self.font.render("Game Over", True, (0, 0, 0))
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        play_again_text = self.font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

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
        self.image = bee_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Collectible:
    def __init__(self):
        self.image = pollen_image
        self.rect = self.image.get_rect()  # Initialize rect here
        self.reposition()

    def reposition(self):
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), random.randint(0, SCREEN_HEIGHT - self.rect.height))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Obstacle:
    def __init__(self):
        self.image = raindrop_image
        self.rect = self.image.get_rect()  # Initialize rect here
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), random.randint(0, SCREEN_HEIGHT - self.rect.height))
        self.speed = random.randint(1, 3)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (random.randint(0, SCREEN_WIDTH - self.rect.width), -self.rect.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def local_run_redefine_resources_paths():
    global bee_image, pollen_image, raindrop_image, background_image
    # Path to resource directory
    resource_path = "resources/pollen_collector/"

    # Load images
    bee_image = pygame.image.load(resource_path + "bee.png")
    pollen_image = pygame.image.load(resource_path + "pollen.png")
    raindrop_image = pygame.image.load(resource_path + "raindrop.png")
    background_image = pygame.image.load(resource_path + "rainy_background.png")

    # Scale images
    bee_image = pygame.transform.scale(bee_image, (50, 50))
    pollen_image = pygame.transform.scale(pollen_image, (30, 30))
    raindrop_image = pygame.transform.scale(raindrop_image, (20, 50))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def start_pollen_collector():
    game = Game()
    game.run()

if __name__ == "__main__":
    local_run_redefine_resources_paths()
    start_pollen_collector()
