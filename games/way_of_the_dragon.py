import pygame
import sys

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def init_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Way of the Dragon")
    return screen

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.5
        self.jump_strength = -10
        self.platforms = platforms

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE]:
            self.velocity.y = self.jump_strength

        self.velocity.y += self.gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Prevent the player from falling through the bottom of the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0

        # Check for collision with platforms
        platform_collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        if platform_collisions:
            self.rect.bottom = platform_collisions[0].rect.top
            self.velocity.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Green color for platforms
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def create_sprites():
    platforms = pygame.sprite.Group()

    platform1 = Platform(100, 500, 200, 20)
    platform2 = Platform(400, 400, 200, 20)
    platforms.add(platform1, platform2)

    player = Player(platforms)
    all_sprites = pygame.sprite.Group(player, platform1, platform2)

    return all_sprites, platforms

def start_way_of_the_dragon():
    pygame.init()
    screen = init_screen()
    clock = pygame.time.Clock()
    all_sprites, platforms = create_sprites()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update all sprites
        all_sprites.update()

        # Fill the screen with a color (RGB)
        screen.fill((135, 206, 235))  # Sky blue background

        # Draw all sprites
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 frames per second
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_way_of_the_dragon()
