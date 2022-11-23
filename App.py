import pygame
import pygame_gui

from Block import Block


class App:
    def __init__(self) -> None:
        # initialize pygame
        pygame.init()

        # set window size and is_running and algorithm
        self.W_WIDTH = pygame.display.Info().current_w
        self.W_HEIGHT = pygame.display.Info().current_h

        print("Window Size: " + str(self.W_WIDTH) + "x" + str(self.W_HEIGHT))

        self.is_running = True
        self.algorithm = "Dijkstra"
        self.grid_sizes = ["50x50", "100x100", "150x150", "200x200"]
        self.selected_grid_size = self.grid_sizes[0]

        self.cells = [
            [Block(x, y) for x in range(int(self.selected_grid_size.split("x")[0]))]
            for y in range(int(self.selected_grid_size.split("x")[1]))
        ]

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

    def run(self) -> None:

        # define UI elements
        start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.W_WIDTH - 80, 0, 80, 50),
            text="Start",
            manager=self.gui_manager,
            object_id="#start_button",
        )
        algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Dijkstra", "A*", "BFS"],
            starting_option="Dijkstra",
            relative_rect=pygame.Rect(0, 0, 100, 50),
            manager=self.gui_manager,
        )
        grid_size_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.grid_sizes,
            starting_option="50x50",
            relative_rect=pygame.Rect(110, 0, 100, 50),
            manager=self.gui_manager,
        )

        # create clock and set fps
        clock = pygame.time.Clock()

        while self.is_running:

            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start:
                        print("Start Pathfinding with " + self.algorithm)

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == algorithm_dropdown:
                        print("Algorithm: " + event.text)
                        self.algorithm = event.text

                    if event.ui_element == grid_size_dropdown:
                        print("Grid Size: " + event.text)
                        self.selected_grid_size = event.text
                        self.update_cells(event.text)

                self.gui_manager.process_events(event)

            # update gui and draw window
            self.gui_manager.update(time_delta)
            self.window.fill((0, 0, 0))
            # draw cells
            for row in self.cells:
                for cell in row:
                    cell.draw(self.cells, self.window)

            self.gui_manager.draw_ui(self.window)
            pygame.display.update()

        pygame.quit()
