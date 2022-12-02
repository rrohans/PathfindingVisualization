import time, random
import matplotlib.pyplot as plt

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
        print("Running BFS...")
        start_time = time.time()
        self.bfs_distance = bfs(self.maze, self.start_node, self.end_node)
        self.bfs_time = (time.time() - start_time) 

    def run_dfs(self) -> None:
        print("Running DFS...")
        start_time = time.time()
        self.dfs_distance = dfs(self.maze, self.start_node, self.end_node)
        self.dfs_time = (time.time() - start_time)

    def run_dijkstra(self) -> None:
        print("Running Dijkstra...")
        start_time = time.time()
        self.dijkstra_distance = dijkstra(self.maze, self.start_node, self.end_node)
        self.dijkstra_time = (time.time() - start_time)

    def run_a_star(self) -> None:
        print("Running A*...")
        start_time = time.time()
        self.a_star_distance = a_star(self.maze, self.start_node, self.end_node)
        self.a_star_time = (time.time() - start_time)

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
        self.run_dfs()
        self.run_bfs()
        self.run_a_star()
        self.run_dijkstra()

        print(f"{self.filename} Results:")
        print(
            f"BFS: {len(self.bfs_distance) if self.bfs_distance else None} in {self.bfs_time}ms"
        )
        print(
            f"DFS: {len(self.dfs_distance) if self.dfs_distance else None} in {self.dfs_time}ms"
        )
        print(
            f"Dijkstra: {len(self.dijkstra_distance) if self.dijkstra_distance else None} in {self.dijkstra_time}ms"
        )
        print(
            f"A*: {len(self.a_star_distance) if self.a_star_distance else None} in {self.a_star_time}ms"
        )

        # plot the results in a bar graph and write the time on the middle of the bar
        plt.bar(
            ["BFS", "DFS", "Dijkstra", "A*"],
            [
                self.bfs_time,
                self.dfs_time,
                self.dijkstra_time,
                self.a_star_time,
            ],
        )
 
        for c in plt.gca().containers:
            plt.gca().bar_label(c, fmt="%.3f", color="black", fontweight="bold")

        plt.title(f"{self.filename} Results")
        plt.xlabel("Algorithm")
        plt.ylabel("Time (ms)")


        plt.show()


    def generate_random_maze(n: int):
        # generate a random n x n maze and save it to a file

        # create a 2d array of blocks
        maze = [[Block(x, y) for x in range(n)] for y in range(n)]

        # randomly select a start and end node
        start_node = (random.randint(0, n - 1), random.randint(0, n - 1))
        end_node = (random.randint(0, n - 1), random.randint(0, n - 1))

        # make sure the start and end nodes are not the same
        while start_node == end_node:
            end_node = (random.randint(0, n - 1), random.randint(0, n - 1))

        # set the start and end nodes
        maze[start_node[1]][start_node[0]].is_start = True
        maze[end_node[1]][end_node[0]].is_end = True

        # randomly select a number of walls
        num_walls = random.randint(0, n * n)

        # randomly select the walls
        for _ in range(num_walls):
            wall = (random.randint(0, n - 1), random.randint(0, n - 1))

            # make sure the wall is not the start or end node
            while wall == start_node or wall == end_node:
                wall = (random.randint(0, n - 1), random.randint(0, n - 1))

            maze[wall[1]][wall[0]].is_wall = True

        # save the maze to a file
        with open(f"{n}x{n}.maze", "w") as f:
            for row in maze:
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


