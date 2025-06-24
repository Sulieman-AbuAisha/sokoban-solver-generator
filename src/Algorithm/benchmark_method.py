import time
from collections import defaultdict

from .astar import solve_astar
from .gbfs import solve_gbfs
from .bfs import solve_bfs
from .ucs import solve_USC



def solve_with_benchmark_method(puzzle, widget=None, visualizer=False, heuristic='manhattan'):
    """
    Solve the puzzle using the specified benchmark method.
    
    Parameters:
        puzzle (np.ndarray): The puzzle matrix.
        method (str): The method to use for solving ('astar', 'gbfs', etc.).
        widget (optional): A widget for displaying progress or results.
        visualizer (bool): Whether to visualize the solving process.
        heuristic (str): The heuristic to use for the method.
        
    Returns:
        tuple: A tuple containing the solution path and depth.
    """
    benchmark_dict = {
        "A*": {},  
        "BFS": {},
        "GBFS": {},
        "USC": {}
    }
    start = time.time()
    solve_bfs(puzzle, widget=widget, visualizer=visualizer, benchmark_dict=benchmark_dict['BFS'])  
    runtime = round(time.time() - start, 5)
    benchmark_dict['BFS']['runtime'] = runtime    

    start = time.time()
    solve_astar(puzzle, widget=widget, visualizer=visualizer, heuristic=heuristic, benchmark_dict=benchmark_dict['A*'])
    runtime = round(time.time() - start, 5)
    benchmark_dict['A*']['runtime'] = runtime
    
    start = time.time()
    solve_gbfs(puzzle, widget=widget, visualizer=visualizer, heuristic=heuristic, benchmark_dict=benchmark_dict['GBFS'])
    runtime = round(time.time() - start, 5)
    benchmark_dict['GBFS']['runtime'] = runtime    
    
    start = time.time()
    solve_USC(puzzle, widget=widget, visualizer=visualizer, benchmark_dict=benchmark_dict['USC'])
    runtime = round(time.time() - start, 5)
    benchmark_dict['USC']['runtime'] = round(time.time() - start, 5)
    
    return benchmark_dict

    