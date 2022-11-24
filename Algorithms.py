from Block import Block

# bfs algorithm that finds shortest path from start to end
# and paints the path purple if it exists and yellow if checked
# return the cells as a list that are in the path
def bfs(cells: list[list[Block]], start: tuple, end: tuple) -> int:
    def get_neighbors() -> list[Block]:
        # get the neighbors of the block
        neighbors = []

        # get the coordinates of the block
        x = block.x
        y = block.y

        # get the left neighbor
        if x > 0:
            left = cells[y][x - 1]
            neighbors.append(left)

        # get the right neighbor
        if x < len(cells[0]) - 1:
            right = cells[y][x + 1]
            neighbors.append(right)

        # get the top neighbor
        if y > 0:
            top = cells[y - 1][x]
            neighbors.append(top)

        # get the bottom neighbor
        if y < len(cells) - 1:
            bottom = cells[y + 1][x]
            neighbors.append(bottom)

        return neighbors

    # check if start and end are valid
    if start is None or end is None:
        return None

    # set start and end blocks
    start_block = cells[start[1]][start[0]]
    end_block = cells[end[1]][end[0]]

    # set start block as checked and add it to the queue
    start_block.is_checked = True
    queue = [start_block]

    # set the parent of the start block to itself
    start_block.parent = start_block

    # while the queue is not empty
    while len(queue) > 0:
        # get the first block in the queue
        block = queue.pop(0)

        # if the block is the end block
        if block == end_block:
            # get the path
            path = []
            current_block = block

            # while the current block is not the start block
            while current_block != start_block:
                # add the current block to the path
                current_block.is_checked = False
                current_block.is_path = True
                path.append(current_block)

                # set the current block to its parent
                current_block = current_block.parent

            # reverse the path and return it
            path.reverse()
            return path

        # get the neighbors of the block
        neighbors = get_neighbors()

        # for each neighbor
        for neighbor in neighbors:
            # if the neighbor is not a wall and not checked
            if not neighbor.is_wall and not neighbor.is_checked:
                # set the neighbor as checked
                neighbor.is_checked = True

                # set the parent of the neighbor to the block
                neighbor.parent = block

                # add the neighbor to the queue
                queue.append(neighbor)

    # return None if no path exists
    return None
