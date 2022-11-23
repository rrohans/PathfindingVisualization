import pygame


class Block:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREEN = (0, 255, 0)

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.color = Block.ORANGE
        self.is_wall = False
        self.is_start = False
        self.is_end = False

    def draw(self, cells, window: pygame.Surface) -> None:
        pass
