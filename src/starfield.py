import pygame
import random

class Starfield:
    """
    Manages a 3D starfield effect.
    """
    def __init__(self, screen_width, screen_height, num_stars=200):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_stars = num_stars
        self.stars = []

        # Star properties
        self.speed = 0.5  # Slower than original for a more subtle effect
        self.star_color = (200, 200, 200) # White-ish stars

        for _ in range(self.num_stars):
            self.stars.append(self._generate_star())

    def _generate_star(self):
        """Generates a single star with a random position."""
        # Start stars in a "box" in front of the camera
        x = random.uniform(-self.screen_width, self.screen_width)
        y = random.uniform(-self.screen_height, self.screen_height)
        # z determines depth; start them at various distances
        z = random.uniform(1, self.screen_width)
        return [x, y, z]

    def update(self):
        """
        Updates the position of each star.
        """
        for star in self.stars:
            # Move star closer to the viewer
            star[2] -= self.speed

            # If star is behind the viewer, reset it to a new position
            if star[2] <= 0:
                star[0] = random.uniform(-self.screen_width, self.screen_width)
                star[1] = random.uniform(-self.screen_height, self.screen_height)
                star[2] = self.screen_width # Reset to the back

    def draw(self, surface):
        """
        Draws the stars onto the given surface.
        """
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        for star in self.stars:
            # Basic 3D projection
            if star[2] > 0:
                sx = (star[0] / star[2]) * self.screen_width + center_x
                sy = (star[1] / star[2]) * self.screen_height + center_y

                # Check if the star is on screen
                if 0 < sx < self.screen_width and 0 < sy < self.screen_height:
                    # Star size diminishes with distance
                    size = (1 - star[2] / self.screen_width) * 2
                    size = max(0, min(3, size)) # Clamp size

                    # Draw a small circle for the star
                    pygame.draw.circle(surface, self.star_color, (int(sx), int(sy)), size)
