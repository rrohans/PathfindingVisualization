import time

from Block import Block

# get the neighbors of a block
def get_neighbors(block: Block, cells: list[list[Block]]) -> list[Block]:
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


# bfs algorithm that finds shortest path from start to end
# and paints the path purple if it exists and yellow if checked
# return the cells as a list that are in the path
def bfs(cells: list[list[Block]], start: tuple, end: tuple, draw=None) -> list[tuple]:

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
        if draw:
            draw()
        # get the first block in the queue
        block = queue.pop(0)

        # if the block is the end block
        if block == end_block:
            # get the path
            path = []
            current_block = block

            # while the current block is not the start block
            while current_block != start_block:
                if draw:
                    draw()
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
        neighbors = get_neighbors(block, cells)

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


# a* algorithm that finds shortest path from start to end
# and paints the path purple if it exists and yellow if checked
# return the cells as a list that are in the path
def a_star(
    cells: list[list[Block]], start: tuple, end: tuple, draw=None
) -> list[tuple]:
    # check if start and end are valid
    if start is None or end is None:
        return None

    # set start and end blocks
    start_block = cells[start[1]][start[0]]
    end_block = cells[end[1]][end[0]]

    def heuristic(a: Block, b: Block) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

    # begin a* algorithm
    open_set = set()
    closed_set = set()
    open_set.add(start_block)

    # set the parent of the start block to itself
    start_block.parent = start_block

    start_block.g = 0
    start_block.h = heuristic(start_block, end_block)
    start_block.f = start_block.g + start_block.h

    # while the open set is not empty
    while len(open_set) > 0:
        if draw:
            draw()
        # get the block with the lowest f score
        current_block = None
        for block in open_set:
            if current_block is None or block.f < current_block.f:
                current_block = block

        # if the current block is the end block
        if current_block == end_block:
            # get the path
            path = []
            current_block = end_block

            # while the current block is not the start block
            while current_block != start_block:
                if draw:
                    draw()
                # add the current block to the path
                current_block.is_checked = False
                current_block.is_path = True
                path.append(current_block)

                # set the current block to its parent
                current_block = current_block.parent

            # reverse the path and return it
            path.reverse()
            return path

        # remove the current block from the open set and add it to the closed set
        open_set.remove(current_block)
        closed_set.add(current_block)

        # get the neighbors of the current block
        neighbors = get_neighbors(current_block, cells)

        # for each neighbor
        for neighbor in neighbors:
            # if the neighbor is not a wall and not in the closed set
            if not neighbor.is_wall and neighbor not in closed_set:
                # calculate the new g score
                new_g = current_block.g + 1

                # if the neighbor is not in the open set or the new g score is less than the old g score
                if neighbor not in open_set or new_g < neighbor.g:
                    # set the g score of the neighbor to the new g score
                    neighbor.g = new_g

                    # calculate the new h score
                    neighbor.h = heuristic(neighbor, end_block)

                    # calculate the new f score
                    neighbor.f = neighbor.g + neighbor.h

                    # set the parent of the neighbor to the current block
                    neighbor.parent = current_block

                    # if the neighbor is not in the open set
                    if neighbor not in open_set:
                        # add the neighbor to the open set
                        neighbor.is_checked = True
                        open_set.add(neighbor)

    # return None if no path exists
    return None


# dfs algorithm that finds shortest path from start to end
# and paints the path purple if it exists and yellow if checked
# return the cells as a list that are in the path
def dfs(cells: list[list[Block]], start: tuple, end: tuple, draw=None) -> list[tuple]:
    # check if start and end are valid
    if start is None or end is None:
        return None

    # set start and end blocks
    start_block = cells[start[1]][start[0]]
    end_block = cells[end[1]][end[0]]

    # set start block as checked and add it to the stack
    start_block.is_checked = True
    stack = [start_block]

    # set the parent of the start block to itself
    start_block.parent = start_block

    # while the stack is not empty
    while len(stack) > 0:
        if draw:
            draw()
        # get the first block in the stack
        block = stack.pop()

        # if the block is the end block
        if block == end_block:
            # get the path
            path = []
            current_block = block

            # while the current block is not the start block
            while current_block != start_block:
                if draw:
                    draw()
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
        neighbors = get_neighbors(block, cells)

        # for each neighbor
        for neighbor in neighbors:
            # if the neighbor is not a wall and not checked
            if not neighbor.is_wall and not neighbor.is_checked:
                # set the neighbor as checked
                neighbor.is_checked = True

                # set the parent of the neighbor to the block
                neighbor.parent = block

                # add the neighbor to the stack
                stack.append(neighbor)

    # return None if no path exists
    return None


# dijkstra algorithm that finds shortest path from start to end
# and paints the path purple if it exists and yellow if checked
# return the cells as a list that are in the path
def dijkstra(
    cells: list[list[Block]], start: tuple, end: tuple, draw=None
) -> list[tuple]:

    # check if start and end are valid
    if start is None or end is None:
        return None

    # set start and end blocks
    start_block = cells[start[1]][start[0]]
    end_block = cells[end[1]][end[0]]

    # set the parent of the start block to itself
    start_block.parent = start_block

    # set of unvisited blocks with all blocks
    unvisited = set()
    for row in cells:
        for block in row:
            unvisited.add(block)

    # set the distance of the start block to 0
    start_block.distance = 0

    # while the unvisited set is not empty
    while len(unvisited) > 0:
        if draw:
            draw()
        # get the block with the smallest distance
        current_block = None
        for block in unvisited:
            if current_block is None or block.distance < current_block.distance:
                current_block = block

        current_block.is_checked = True

        # if the current block is the end block
        if current_block == end_block:
            # get the path
            path = []
            current_block = end_block

            # while the current block is not the start block
            while current_block != start_block:
                if draw:
                    draw()
                # add the current block to the path
                current_block.is_checked = False
                current_block.is_path = True
                path.append(current_block)

                # set the current block to its parent
                current_block = current_block.parent

            # reverse the path and return it
            path.reverse()
            return path

        # remove the current block from the unvisited set
        unvisited.remove(current_block)

        # get the neighbors of the current block
        neighbors = get_neighbors(current_block, cells)

        # for each neighbor
        for neighbor in neighbors:
            # if the neighbor is not a wall
            if not neighbor.is_wall:
                # calculate the new distance
                new_distance = current_block.distance + 1

                # if the new distance is less than the old distance
                if new_distance < neighbor.distance:
                    # set the distance of the neighbor to the new distance
                    neighbor.distance = new_distance

                    # set the parent of the neighbor to the current block
                    neighbor.parent = current_block

    # return None if no path exists
    return None
