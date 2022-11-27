import pygame
import pygame_gui

from Block import Block
from Algorithms import bfs, dfs, dijkstra, a_star


class App:

    ALGO_DESC = {
        "BFS": "Shortest path guaranteed on unweighted graphs",
        "DFS": "Shortest path not guaranteed on unweighted graphs",
        "Dijkstra": "Shortest path guaranteed on weighted graphs",
        "A*": "Shortest path guaranteed on weighted graphs",
    }

    ALGOS = {
        "BFS": bfs,
        "DFS": dfs,
        "Dijkstra": dijkstra,
        "A*": a_star,
    }

    def __init__(
        self,
        w: int = 800,
        h: int = 800,
    ) -> None:
        # initialize pygame
        pygame.init()

        # set window size and is_running and algorithm
        self.W_WIDTH = w
        self.W_HEIGHT = h

        self.is_running = True
        self.algorithm = "Dijkstra"
        self.grid_sizes = ["10x10", "20x20", "30x30", "40x40", "50x50"]
        self.selected_grid_size = self.grid_sizes[2]

        self.cells = [
            [Block(x, y) for x in range(int(self.selected_grid_size.split("x")[0]))]
            for y in range(int(self.selected_grid_size.split("x")[1]))
        ]

        # start and end blocks
        self.start_block: tuple = None
        self.end_block: tuple = None

        # create window and gui manager and set window title
        pygame.display.set_caption("Pathfinding Visualizer")
        self.window = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))
        self.gui_manager = pygame_gui.UIManager(
            (self.W_WIDTH, self.W_HEIGHT), "theme.json"
        )

    def update_cells(self, new_size: str) -> None:
        self.cells = [
            [Block(x, y) for x in range(int(new_size.split("x")[0]))]
            for y in range(int(new_size.split("x")[1]))
        ]

    def clear_board(self) -> None:
        for row in self.cells:
            for block in row:
                block.is_wall = False
                block.is_start = False
                block.is_end = False
                block.is_checked = False
                block.is_path = False

        self.start_block = None
        self.end_block = None

    def restart(self) -> None:
        # clear all paths and checked blocks and dijkstra variables and a* variables
        for row in self.cells:
            for block in row:
                block.is_checked = False
                block.is_path = False
                block.g = float("inf")
                block.h = 0
                block.f = float("inf")
                block.distance = float("inf")

    def start(self) -> None:
        print("Start Pathfinding with " + self.algorithm)
        self.ALGOS[self.algorithm](
            self.cells, self.start_block, self.end_block, self.draw
        )

    def save(self) -> None:
        with open(f"{self.selected_grid_size}.maze", "w") as f:
            for row in self.cells:
                for block in row:
                    if block.is_wall:
                        f.write("w")
                    elif block.is_start:
                        f.write("s")
                    elif block.is_end:
                        f.write("e")
                    else:
                        f.write(".")
                f.write("\n")

    def draw(self) -> None:
        self.window.fill((0, 0, 0))
        # draw cells
        for row in self.cells:
            for block in row:
                block.draw(self.cells, self.window)

        # draw gui elements
        self.gui_manager.draw_ui(self.window)
        pygame.display.update()

    def run(self) -> None:

        # define UI elements
        start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.W_WIDTH - 80, 0, 80, 50),
            text="Start",
            manager=self.gui_manager,
            object_id="#start_button",
        )
        algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Dijkstra", "A*", "BFS", "DFS"],
            starting_option="Dijkstra",
            relative_rect=pygame.Rect(0, 0, 100, 50),
            manager=self.gui_manager,
        )
        grid_size_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.grid_sizes,
            starting_option=self.selected_grid_size,
            relative_rect=pygame.Rect(110, 0, 100, 50),
            manager=self.gui_manager,
        )
        clear_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.W_WIDTH - 160, 0, 80, 50),
            text="Clear",
            manager=self.gui_manager,
        )
        save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.W_WIDTH - 240, 0, 80, 50),
            text="Save",
            manager=self.gui_manager,
        )
        load_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.W_WIDTH - 320, 0, 80, 50),
            text="Load",
            manager=self.gui_manager,
        )
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.W_WIDTH - 400, 0, 80, 50),
            text="Restart",
            manager=self.gui_manager,
        )

        # create clock and set fps
        clock = pygame.time.Clock()

        while self.is_running:

            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                self.gui_manager.process_events(event)

                if event.type == pygame.QUIT:
                    self.is_running = False

                # handle UI events
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if (
                        event.ui_element == start
                        and self.start_block
                        and self.end_block
                    ):
                        self.start()

                    if event.ui_element == clear_button:
                        self.clear_board()

                    if event.ui_element == save_button:
                        self.save()

                    if event.ui_element == load_button:
                        self.update_cells(
                            self.selected_grid_size
                        )  # TODO: Make it so that the size will be determined by the maze file
                        with open(f"{self.selected_grid_size}.maze", "r") as f:
                            for y, line in enumerate(f):
                                for x, char in enumerate(line):
                                    if char == "w":
                                        self.cells[y][x].is_wall = True
                                    elif char == "s":
                                        self.cells[y][x].is_start = True
                                        self.start_block = (x, y)
                                    elif char == "e":
                                        self.cells[y][x].is_end = True
                                        self.end_block = (x, y)

                    if event.ui_element == restart_button:
                        self.restart()

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == algorithm_dropdown:
                        print("Algorithm: " + event.text)
                        self.algorithm = event.text
                        self.update_cells(self.selected_grid_size)
                        self.start_block = None
                        self.end_block = None

                    if event.ui_element == grid_size_dropdown:
                        print("Grid Size: " + event.text)
                        self.selected_grid_size = event.text
                        self.update_cells(event.text)
                        self.start_block = None
                        self.end_block = None

                # handle clicking cells
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if y < 50:
                            continue
                        width = self.window.get_width() / len(self.cells[0])
                        height = (self.window.get_height() - 50) / len(self.cells)
                        x = int(x / width)
                        y = int((y - 50) / height)
                        if self.start_block is None:
                            self.start_block = (x, y)
                            self.cells[y][x].is_start = True
                        elif self.end_block is None and (x, y) != self.start_block:
                            self.end_block = (x, y)
                            self.cells[y][x].is_end = True
                        elif (x, y) != self.start_block and (x, y) != self.end_block:
                            self.cells[y][x].is_wall = not self.cells[y][x].is_wall
                        else:
                            pass  # do nothing

                # handle dragging cells for walls
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = event.pos
                        if y < 50:
                            continue
                        width = self.window.get_width() / len(self.cells[0])
                        height = (self.window.get_height() - 50) / len(self.cells)
                        x = int(x / width)
                        y = int((y - 50) / height)
                        if (x, y) != self.start_block and (x, y) != self.end_block:
                            self.cells[y][x].is_wall = True

                # handle keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.clear_board()

                    if event.key == pygame.K_r:
                        self.restart()

                    if event.key == pygame.K_s:
                        self.save()

                    if event.key == pygame.K_RETURN:
                        self.start()

            # update gui and draw window
            self.gui_manager.update(time_delta)

            self.draw()

        pygame.quit()
