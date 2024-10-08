import pygame
import sys

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def init_screen():
    """
    Initializes the game screen.

    Returns:
        screen (pygame.Surface): The initialized game screen.
    """
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Way of the Dragon")
    return screen


class Player(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Attributes:
        image (pygame.Surface): The visual representation of the player.
        rect (pygame.Rect): The rectangular area of the player.
        velocity (pygame.math.Vector2): The player's velocity.
        gravity (float): The gravity affecting the player.
        jump_strength (float): The strength of the player's jump.
        platforms (pygame.sprite.Group): The platforms in the game.
    """

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
        """
        Updates the player's state.
        """
        self.handle_keys()
        self.apply_gravity()
        self.move()
        self.check_collisions()

    def handle_keys(self):
        """
        Handles the player's input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE]:
            self.velocity.y = self.jump_strength

    def apply_gravity(self):
        """
        Applies gravity to the player.
        """
        self.velocity.y += self.gravity

    def move(self):
        """
        Moves the player based on velocity.
        """
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Prevent the player from falling through the bottom of the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0

    def check_collisions(self):
        """
        Checks for collisions with platforms.
        """
        platform_collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        if platform_collisions:
            self.rect.bottom = platform_collisions[0].rect.top
            self.velocity.y = 0


class Platform(pygame.sprite.Sprite):
    """
    Represents a platform in the game.

    Attributes:
        image (pygame.Surface): The visual representation of the platform.
        rect (pygame.Rect): The rectangular area of the platform.
    """

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Green color for platforms
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def create_sprites():
    """
    Creates and returns the game sprites.

    Returns:
        all_sprites (pygame.sprite.Group): All the sprites in the game.
        platforms (pygame.sprite.Group): The platform sprites in the game.
    """
    platforms = pygame.sprite.Group()

    platform1 = Platform(100, 500, 200, 20)
    platform2 = Platform(400, 400, 200, 20)
    platforms.add(platform1, platform2)

    player = Player(platforms)
    all_sprites = pygame.sprite.Group(player, platform1, platform2)

    return all_sprites, platforms


def game_loop(screen, clock, all_sprites):
    """
    The main game loop.

    Args:
        screen (pygame.Surface): The game screen.
        clock (pygame.time.Clock): The game clock.
        all_sprites (pygame.sprite.Group): All the sprites in the game.
    """
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


def start_way_of_the_dragon():
    """Starts the game."""
    pygame.init()
    screen = init_screen()
    clock = pygame.time.Clock()
    all_sprites, platforms = create_sprites()

    game_loop(screen, clock, all_sprites)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    start_way_of_the_dragon()
