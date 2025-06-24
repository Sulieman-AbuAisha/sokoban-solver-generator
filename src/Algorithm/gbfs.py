

from heapq import heappop, heappush
import numpy as np
import pygame
from ..utils import can_move, get_state, is_deadlock, is_solved, manhattan_sum

def GBFS(matrix, player_pos, widget=None, visualizer=False, heuristic='manhattan', dict=None):
    shape = matrix.shape
    initial_state = get_state(matrix)
    curr_depth = 0
    curr_cost = manhattan_sum(initial_state, player_pos, shape)

    seen = {None}
    heap = []
    heappush(heap, (curr_cost, initial_state, player_pos, curr_depth, ''))

    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    direction = {
		(1, 0): 'D', 
		(-1, 0): 'U',
		(0, -1): 'L',
		(0, 1): 'R'
	}
    count = 0
    max_frontier = 0
    while heap:
        if widget:
            pygame.event.pump()  

        _, state, pos, depth, path = heappop(heap)
        seen.add(state)
        count += 1
        if max_frontier < len(heap):
            max_frontier = len(heap)
            
        for move in moves:
            new_state, move_cost = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            if new_state in seen or deadlock:
                continue
            new_pos = pos[0] + move[0], pos[1] + move[1]
            new_cost = manhattan_sum(new_state, new_pos, shape)
            heappush(heap, (
                new_cost,
                new_state,
                new_pos,
                depth + 1,
                path + direction[move],
            ))
            if is_solved(new_state):
                if dict is not None:
                    dict["moves"] = len(path + direction[move])
                    dict["depth"] = depth + 1
                    dict["node expanded"] = count
                    dict["max frontier"] = max_frontier
                    dict["Outcome"] = 'Success'
                    dict["solution"] = path + direction[move]
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'GBFS Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return (path + direction[move], depth + 1)
            if widget and visualizer:
                widget.set_text(f'GBFS Solution Depth: {depth + 1}\n{path + direction[move]}', 20)
                pygame.display.update()
    print(f'GBFS Solution not found!\n')
    if dict is not None:
        dict["moves"] = len(path + direction[move])
        dict["depth"] = depth + 1
        dict["node expanded"] = count
        dict["max frontier"] = max_frontier
        dict["Outcome"] = 'Failure'
        dict["solution"] = path + direction[move]

    if widget and visualizer:
        widget.set_text(f'GBFS Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return (None, -1 )



def solve_gbfs(puzzle, widget=None, visualizer=False, heuristic='manhattan', benchmark_dict=None):
    matrix = puzzle
    where = np.where((matrix == '*') | (matrix == '%'))
    player_pos = where[0][0], where[1][0]
    return GBFS(matrix, player_pos, widget, visualizer, heuristic, dict=benchmark_dict)
