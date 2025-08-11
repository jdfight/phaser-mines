import pygame
import sys

from src.minefield import Minefield
from src.sprites import CellSprite, load_sprite_sheet, load_flag_image, CELL_SIZE
from src.starfield import Starfield

# --- Constants ---
DIFFICULTY = {
    "easy": {"size": (10, 10), "mines": 10},
    "medium": {"size": (16, 16), "mines": 40},
    "hard": {"size": (24, 24), "mines": 100},
}
DEFAULT_DIFFICULTY = "easy"

GAME_TITLE = "Asteroid Miner (Pygame)"
GRID_X_OFFSET = 40
GRID_Y_OFFSET = 40

# Colors
BLACK_BG = (0, 3, 12)
WHITE = (255, 255, 255)
BUTTON_COLOR = (50, 50, 70)
BUTTON_HOVER_COLOR = (80, 80, 100)

class Game:
    def __init__(self, difficulty_name):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.difficulty_name = difficulty_name
        self.setup_screen_and_assets()
        self.reset_game()

    def setup_screen_and_assets(self):
        """Sets up the screen size and loads assets."""
        grid_w, grid_h = DIFFICULTY[self.difficulty_name]["size"]
        self.screen_width = grid_w * CELL_SIZE + 200
        self.screen_height = grid_h * CELL_SIZE + 80

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(GAME_TITLE)

        try:
            self.cell_images = load_sprite_sheet()
            self.flag_image = load_flag_image()
        except pygame.error as e:
            print(f"Error loading assets: {e}")
            pygame.quit()
            sys.exit()

        self.starfield = Starfield(self.screen_width, self.screen_height)
        self._setup_buttons()

    def _setup_buttons(self):
        """Creates the rects for the difficulty buttons."""
        self.buttons = {}
        button_y = self.screen_height - 50
        for i, name in enumerate(DIFFICULTY.keys()):
            # Place buttons on the right side panel
            x_pos = self.screen_width - 160
            y_pos = 200 + i * 50
            self.buttons[name] = pygame.Rect(x_pos, y_pos, 120, 40)

    def reset_game(self):
        """Resets the game to the current difficulty."""
        difficulty = DIFFICULTY[self.difficulty_name]
        grid_w, grid_h = difficulty["size"]
        num_mines = difficulty["mines"]

        self.minefield = Minefield(grid_w, grid_h, num_mines)
        self.all_sprites = pygame.sprite.Group()

        for y in range(self.minefield.height):
            for x in range(self.minefield.width):
                cell_data = self.minefield.grid[y][x]
                sprite = CellSprite(
                    cell_data,
                    x * CELL_SIZE + GRID_X_OFFSET,
                    y * CELL_SIZE + GRID_Y_OFFSET,
                    self.cell_images,
                    self.flag_image,
                    self.font
                )
                self.all_sprites.add(sprite)

    def run(self):
        """Main game loop."""
        running = True
        clock = pygame.time.Clock()

        while running:
            mouse_pos = pygame.mouse.get_pos()

            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check difficulty buttons first
                    for name, rect in self.buttons.items():
                        if rect.collidepoint(event.pos):
                            self.difficulty_name = name
                            # Re-setup the screen and reset the game
                            self.setup_screen_and_assets()
                            self.reset_game()
                            break # Exit button loop
                    else: # If no button was clicked, check the grid
                        if not self.minefield.game_over:
                            for sprite in self.all_sprites:
                                if sprite.rect.collidepoint(event.pos):
                                    action = sprite.handle_click(event.button)
                                    if action == "open":
                                        self.minefield.open_cell(sprite.cell_data.x, sprite.cell_data.y)
                                    elif action == "flag":
                                        self.minefield.toggle_flag(sprite.cell_data.x, sprite.cell_data.y)

                                    self.all_sprites.update()
                                    break

            # --- Update ---
            self.starfield.update()

            # --- Drawing ---
            self.screen.fill(BLACK_BG)
            self.starfield.draw(self.screen)
            self.all_sprites.draw(self.screen)
            self._draw_ui(mouse_pos)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def _draw_ui(self, mouse_pos):
        """Draws all UI elements."""
        # Mine Counter
        counter_text = f"Mines: {self.minefield.mines_remaining}"
        counter_surf = self.font.render(counter_text, True, WHITE)
        self.screen.blit(counter_surf, (GRID_X_OFFSET, 10))

        # Game Over/Win Message
        if self.minefield.game_over:
            msg = "You Won!" if self.minefield.game_won else "Boom! Game Over"
            msg_surf = self.font.render(msg, True, WHITE)
            msg_rect = msg_surf.get_rect(center=(self.screen_width / 2, 15))
            self.screen.blit(msg_surf, msg_rect)

        # Difficulty Buttons
        for name, rect in self.buttons.items():
            color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            btn_text = self.font.render(name.capitalize(), True, WHITE)
            text_rect = btn_text.get_rect(center=rect.center)
            self.screen.blit(btn_text, text_rect)

if __name__ == '__main__':
    game = Game(DEFAULT_DIFFICULTY)
    game.run()
