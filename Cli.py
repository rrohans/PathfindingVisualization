import time

from Block import Block
from Algorithms import bfs, dfs, a_star, dijkstra


class Cli:
    def __init__(self, fn: str) -> None:
        self.filename = fn
        self.maze = None

        self.start_node = None
        self.end_node = None

        # timing variables
        self.bfs_time = 0
        self.dfs_time = 0
        self.dijkstra_time = 0
        self.a_star_time = 0

        # distance variables
        self.bfs_distance = 0
        self.dfs_distance = 0
        self.dijkstra_distance = 0
        self.a_star_distance = 0

    def run_bfs(self) -> None:
        start_time = time.time()
        self.bfs_distance = bfs(self.maze, self.start_node, self.end_node)
        self.bfs_time = (time.time() - start_time) * 1000

    def run_dfs(self) -> None:
        start_time = time.time()
        self.dfs_distance = dfs(self.maze, self.start_node, self.end_node)
        self.dfs_time = (time.time() - start_time) * 1000

    def run_dijkstra(self) -> None:
        start_time = time.time()
        self.dijkstra_distance = dijkstra(self.maze, self.start_node, self.end_node)
        self.dijkstra_time = (time.time() - start_time) * 1000

    def run_a_star(self) -> None:
        start_time = time.time()
        self.a_star_distance = a_star(self.maze, self.start_node, self.end_node)
        self.a_star_time = (time.time() - start_time) * 1000

    def read_maze(self) -> list[list[Block]]:
        maze = []
        tmp_block = None
        try:
            with open(self.filename, "r") as f:
                for y, line in enumerate(f):
                    tmp_row = []
                    for x, char in enumerate(line):
                        if char == "w":
                            tmp_block = Block(x, y)
                            tmp_block.is_wall = True
                        elif char == "s":
                            tmp_block = Block(x, y)
                            tmp_block.is_start = True
                            self.start_node = (x, y)
                        elif char == "e":
                            tmp_block = Block(x, y)
                            tmp_block.is_end = True
                            self.end_node = (x, y)
                        else:
                            tmp_block = Block(x, y)

                        tmp_row.append(tmp_block)

                    maze.append(tmp_row)

        except FileNotFoundError:
            print(f"Maze file {self.filename} not found.")
            exit(1)

        return maze

    def run(self) -> None:
        self.maze = self.read_maze()
        self.run_bfs()
        self.run_dfs()
        self.run_dijkstra()
        self.run_a_star()

        print(f"{self.filename} Results:")
        print(f"BFS: {len(self.bfs_distance) if self.bfs_distance else None} in {self.bfs_time}ms")
        print(f"DFS: {len(self.dfs_distance) if self.bfs_distance else None} in {self.dfs_time}ms")
        print(f"Dijkstra: {len(self.dijkstra_distance) if self.bfs_distance else None} in {self.dijkstra_time}ms")
        print(f"A*: {len(self.a_star_distance) if self.bfs_distance else None} in {self.a_star_time}ms")
