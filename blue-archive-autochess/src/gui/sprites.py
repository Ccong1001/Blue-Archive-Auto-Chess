import pygame

class SpriteManager:
    def __init__(self):
        self.sprites = {}

    def load_sprite(self, name, path):
        """Load a sprite from a given path and store it with the specified name."""
        sprite = pygame.image.load(path).convert_alpha()
        self.sprites[name] = sprite

    def get_sprite(self, name):
        """Retrieve a sprite by its name."""
        return self.sprites.get(name)

    def unload_sprite(self, name):
        """Remove a sprite from the manager."""
        if name in self.sprites:
            del self.sprites[name]

    def clear_sprites(self):
        """Clear all loaded sprites."""
        self.sprites.clear()