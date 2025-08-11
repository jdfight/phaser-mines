import pygame
import random

CELL_SIZE = 40  # The original game resizes sprites to 40x40

def load_sprite_sheet():
    """
    Loads the spritesheet and slices it into a dictionary of images.
    """
    sheet = pygame.image.load("assets/textures/mine-tiles2.png").convert_alpha()

    # The spritesheet has 64x64 tiles
    tile_size = 64

    # We only need frames 0, 1, and 2 for the cells
    images = {
        "empty": sheet.subsurface(pygame.Rect(0 * tile_size, 0, tile_size, tile_size)),
        "hidden": sheet.subsurface(pygame.Rect(1 * tile_size, 0, tile_size, tile_size)),
        "mine": sheet.subsurface(pygame.Rect(2 * tile_size, 0, tile_size, tile_size)),
    }

    # Scale the images to the desired display size
    for key, img in images.items():
        images[key] = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))

    return images

def load_flag_image():
    """Loads and scales the flag image."""
    flag_img = pygame.image.load("assets/textures/flag.png").convert_alpha()
    return pygame.transform.scale(flag_img, (CELL_SIZE, CELL_SIZE))

def load_animation_sheet(path, frame_size, scale_size):
    """Loads a spritesheet for animation."""
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(sheet.get_width() // frame_size[0]):
        frame = sheet.subsurface(pygame.Rect(i * frame_size[0], 0, frame_size[0], frame_size[1]))
        frames.append(pygame.transform.scale(frame, scale_size))
    return frames

class AnimatedSprite(pygame.sprite.Sprite):
    """A sprite that plays an animation and then disappears."""
    def __init__(self, x, y, frames, frame_rate):
        super().__init__()
        self.frames = frames
        self.frame_rate = frame_rate
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 / self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill() # Animation finished
            else:
                self.image = self.frames[self.frame]


class CellSprite(pygame.sprite.Sprite):
    """
    Visual representation of a single cell in the minefield.
    """
    def __init__(self, cell_data, x, y, images, flag_image, font):
        super().__init__()
        self.cell_data = cell_data
        self.images = images
        self.flag_image = flag_image
        self.font = font

        self.image = self.images["hidden"]
        self.rect = self.image.get_rect(topleft=(x, y))

        self._update_image() # Set initial image

    def update(self):
        """
        Update the sprite's appearance based on the cell's data.
        This should be called whenever the cell's state might have changed.
        """
        self._update_image()

    def _update_image(self):
        """Internal helper to set the correct image and text."""
        if self.cell_data.is_open:
            # When a mine is opened, it will be handled by an explosion animation
            if self.cell_data.is_mine:
                self.image = self.images["empty"] # Show empty tile underneath
            else:
                self.image = self.images["empty"]
                if self.cell_data.adjacent_mines > 0:
                    # Render the number on top of the empty tile
                    text_surf = self.font.render(str(self.cell_data.adjacent_mines), True, (0, 255, 68)) # Green text from original
                    text_rect = text_surf.get_rect(center=self.image.get_rect().center)
                    # We blit onto a copy to not modify the base 'empty' image
                    self.image = self.images["empty"].copy()
                    self.image.blit(text_surf, text_rect)
        else: # Cell is not open
            if self.cell_data.is_flagged:
                # Draw the hidden tile first, then the flag on top
                self.image = self.images["hidden"].copy()
                self.image.blit(self.flag_image, (0, 0))
            else:
                self.image = self.images["hidden"]

    def handle_click(self, mouse_button):
        """
        Determines the action to take based on the mouse button.
        Returns 'open' or 'flag' if an action should be taken.
        """
        # 1 for left click, 3 for right click
        if mouse_button == 1 and not self.cell_data.is_flagged and not self.cell_data.is_open:
            return "open"
        elif mouse_button == 3 and not self.cell_data.is_open:
            return "flag"
        return None
