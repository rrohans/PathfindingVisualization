import pygame

class Block:

    # define colors for the blocks
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.color = Block.WHITE
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_checked = False
        self.is_path = False

        # a* algorithm variables
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")

        # dijkstra algorithm variables
        self.distance = float("inf")

    def __lt__(self, other) -> bool:
        return self.distance < other.distance

    # draw the block (block responsible for drawing itself)
    def draw(self, cells, window: pygame.Surface) -> None:
        def calculate_dimensions() -> tuple:
            # calculate the dimensions of the block
            # based on how many cells there are
            # so that they tile the screen below the UI
            width = window.get_width() / len(cells[0])
            height = (window.get_height() - 50) / len(cells)
            return width, height

        def select_color() -> tuple:
            # select the color of the block
            if self.is_wall:
                return Block.BLACK
            elif self.is_start:
                return Block.GREEN
            elif self.is_end:
                return Block.ORANGE
            elif self.is_checked:
                return Block.YELLOW
            elif self.is_path:
                return Block.PURPLE
            else:
                return Block.WHITE

        # calculate the dimensions of the block
        width, height = calculate_dimensions()

        # draw the block such that there is a 1px gap between them
        pygame.draw.rect(
            window,
            select_color(),
            (
                self.x * width + 1,
                self.y * height + 1 + 50,  # +50 to account for UI
                width - 1,
                height - 1,
            ),
        )
