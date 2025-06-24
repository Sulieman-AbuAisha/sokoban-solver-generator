

from heapq import heappop, heappush
import numpy as np
import pygame
from ..utils import can_move, get_state, is_deadlock, is_solved


def USC(matrix, player_pos, widget=None, visualizer=False):
    shape = matrix.shape
    initial_state = get_state(matrix)
    initial_cost = 0 
    curr_depth = 0

    seen = {None}
    heap = []
    heappush(heap, (initial_cost, initial_state, player_pos, curr_depth, ''))

    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    direction = {
        (1, 0): 'D', 
        (-1, 0): 'U',
        (0, -1): 'L',
        (0, 1): 'R'
    }

    while heap:
        if widget:
            pygame.event.pump()  

        path_cost, state, pos, depth, path = heappop(heap)
        seen.add(state)
        
        for move in moves:
            new_state, move_cost = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            
            if new_state in seen or deadlock:
                continue
                
            new_pos = pos[0] + move[0], pos[1] + move[1]
            
            heappush(heap, (
                path_cost + move_cost ,  
                new_state,
                new_pos,
                depth + 1,
                path + direction[move],
            ))
            
            if is_solved(new_state):
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'UCS Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return (path + direction[move], depth + 1)
            if widget and visualizer:
                widget.set_text(f'USC Solution Depth: {depth + 1}\n{path + direction[move]}', 20)
                pygame.display.update()
    if widget and visualizer:
        widget.set_text('UCS Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return (None, -1)

def solve_USC(puzzle, widget=None, visualizer=False):
    matrix = puzzle
    where = np.where((matrix == '*') | (matrix == '%'))
    player_pos = where[0][0], where[1][0]
    return USC(matrix, player_pos, widget, visualizer)
