import pygame
import sys
import random

from src.minefield import Minefield
from src.sprites import CellSprite, load_sprite_sheet, load_flag_image, CELL_SIZE, AnimatedSprite, load_animation_sheet
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

        # Effect states
        self.shake_timer = 0
        self.flash_alpha = 0
        self.flash_color = (255, 146, 0) # Orange from original game (0xff9200)

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
            self.explosion_frames = load_animation_sheet("assets/textures/exploBig.png", (40, 40), (CELL_SIZE, CELL_SIZE))
            self.smoke_frames = load_animation_sheet("assets/textures/smoke.png", (20, 20), (CELL_SIZE, CELL_SIZE))
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
        self.animation_sprites = pygame.sprite.Group()

        # Create a map of cell data to cell sprite for easy lookup
        self.cell_sprite_map = {}

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
                self.cell_sprite_map[(x, y)] = sprite

    def trigger_game_over_effects(self):
        """Activates the screen shake and flash effects."""
        self.shake_timer = 20  # Shake for 20 frames
        self.flash_alpha = 200 # Start flash at this alpha

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
                                    # Check game_over state BEFORE opening the cell
                                    was_game_over = self.minefield.game_over
                                    
                                    x, y = sprite.cell_data.x, sprite.cell_data.y
                                    action = sprite.handle_click(event.button)

                                    if action == "open":
                                        opened_cells = self.minefield.open_cell(x, y)
                                        for cell_data in opened_cells:
                                            cell_sprite = self.cell_sprite_map[(cell_data.x, cell_data.y)]
                                            if cell_data.is_mine:
                                                explosion = AnimatedSprite(cell_sprite.rect.x, cell_sprite.rect.y, self.explosion_frames, 24)
                                                self.animation_sprites.add(explosion)
                                            else:
                                                smoke = AnimatedSprite(cell_sprite.rect.x, cell_sprite.rect.y, self.smoke_frames, random.randint(12, 30))
                                                self.animation_sprites.add(smoke)

                                    elif action == "flag":
                                        self.minefield.toggle_flag(x, y)

                                    # If the game just ended because of a mine hit
                                    if not was_game_over and self.minefield.game_over and not self.minefield.game_won:
                                        self.trigger_game_over_effects()

                                    self.all_sprites.update()
                                    break

            # --- Update ---
            self.starfield.update()
            self.animation_sprites.update()

            # --- Drawing ---
            render_offset = [0, 0]
            if self.shake_timer > 0:
                self.shake_timer -= 1
                render_offset[0] = random.randint(-4, 4)
                render_offset[1] = random.randint(-4, 4)

            # Draw all game elements to a temporary surface if shaking
            # This prevents shaking individual elements differently
            temp_surface = self.screen.copy()
            temp_surface.fill(BLACK_BG)
            self.starfield.draw(temp_surface)
            self.all_sprites.draw(temp_surface)
            self.animation_sprites.draw(temp_surface)
            self._draw_ui(mouse_pos, temp_surface)

            # Draw flash effect
            if self.flash_alpha > 0:
                flash_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                flash_surface.fill((*self.flash_color, self.flash_alpha))
                temp_surface.blit(flash_surface, (0, 0))
                self.flash_alpha -= 15 # Fade out faster

            # Draw the potentially shaken surface to the main screen
            self.screen.blit(temp_surface, render_offset)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def _draw_ui(self, mouse_pos, surface):
        """Draws all UI elements onto the given surface."""
        # Mine Counter
        counter_text = f"Mines: {self.minefield.mines_remaining}"
        counter_surf = self.font.render(counter_text, True, WHITE)
        surface.blit(counter_surf, (GRID_X_OFFSET, 10))

        # Game Over/Win Message
        if self.minefield.game_over:
            msg = "You Won!" if self.minefield.game_won else "Boom! Game Over"
            msg_surf = self.font.render(msg, True, WHITE)
            msg_rect = msg_surf.get_rect(center=(self.screen_width / 2, 15))
            surface.blit(msg_surf, msg_rect)

        # Difficulty Buttons
        for name, rect in self.buttons.items():
            color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(surface, color, rect, border_radius=5)
            btn_text = self.font.render(name.capitalize(), True, WHITE)
            text_rect = btn_text.get_rect(center=rect.center)
            surface.blit(btn_text, text_rect)

if __name__ == '__main__':
    game = Game(DEFAULT_DIFFICULTY)
    game.run()
