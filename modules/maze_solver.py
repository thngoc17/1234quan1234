import pygame
from modules.Maze_Generator import *
import random
from queue import PriorityQueue
from collections import deque
class Maze_solver:
    def __init__(self, maze, screen):
        self.maze = maze
        self.screen = screen
        self.maze_size = maze.maze_size
        self.block_size = maze.block_size   
        self.border_size = maze.border_size
        self.start = None
        self.end = None
        self.START()
        self.END()
    def __getstate__(self):
        state = self.__dict__.copy()
        # Check if 'screen' attribute exists before deleting it
        if 'screen' in state:
            del state['screen']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
    def get_neighbors(self, blocks_list):
        x, y = blocks_list.coordinate
        neighbors = []
        directions = [(0, -1, 1), (0, 1, 0), (-1, 0, 3), (1, 0, 2)]  # (dx, dy, wall_index)

        for dx, dy, wall_index in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze_size[0] and 0 <= ny < self.maze_size[1] and not self.maze.blocks_list[ny][nx].has_walls[wall_index]:
                neighbors.append(self.maze.blocks_list[ny][nx])

        return neighbors
    def START(self, start_point=None):
        if start_point is None:
            rand_start = random.randint(0, self.maze_size[0]-1)
            start = self.maze.blocks_list[0][rand_start]
        else:
            start = self.maze.blocks_list[start_point[1]][start_point[0]]
        start.has_walls[0] = False
        self.start = start

    def END(self, end_point=None):
        if end_point is None:
            rand_end = random.randint(0, self.maze_size[0]-1)
            end = self.maze.blocks_list[self.maze.maze_size[0]-1][rand_end]
        else:
            end = self.maze.blocks_list[end_point[1]][end_point[0]]
        end.has_walls[1] = False
        self.end = end
    def a_star_search(self, current_pos):
        count = 0
        start = current_pos
        end = self.end
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {block: float("inf") for row in self.maze.blocks_list for block in row}
        g_score[start] = 0
        f_score = {block: float("inf") for row in self.maze.blocks_list for block in row}
        f_score[start] = h(start.coordinate, end.coordinate)
        open_set_hash = {start}
        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)
            if current == end:
                return came_from
            for neighbor in self.get_neighbors(current):
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.coordinate, end.coordinate)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)         
        return False
    def bfs_search(self, start_pos):
        start = start_pos
        end = self.end
        queue = deque([start])
        came_from = {}
        distance = {block: float("inf") for row in self.maze.blocks_list for block in row}
        distance[start] = 0
        while queue:
            current = queue.popleft()
            if current == end:
                return came_from
            for neighbor in self.get_neighbors(current):
                if distance[neighbor] == float("inf"):  # If neighbor has not been visited
                    queue.append(neighbor)
                    came_from[neighbor] = current
                    distance[neighbor] = distance[current] + 1
        return False
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    