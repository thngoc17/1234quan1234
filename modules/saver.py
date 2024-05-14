import pickle

def save_objects(maze_now, maze_solver, hero_now):
    # Put the objects into a dictionary
    data = {
        'maze_now': maze_now,
        'maze_solver': maze_solver,
        'hero_now': hero_now
    }

    # Save the dictionary to a pickle file
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)
