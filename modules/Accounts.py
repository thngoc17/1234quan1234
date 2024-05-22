import logging
import pickle
import copy
from modules.Textbox import *

def save_users(username, password, filename, maze_data=None):
    try:
        with open(filename, 'rb') as f:
            users = pickle.load(f)
    except (EOFError, FileNotFoundError):
        users = {}
    # Create a deep copy of the users dictionary to preserve original data
    updated_users = copy.deepcopy(users)
    if username in updated_users:
        user_info = updated_users[username]
    else:
        user_info = {'password': password, 'mazes': [{'number': i+1, 'maze': None} for i in range(7)]}
    if maze_data is not None:
        maze_count = sum(1 for maze in user_info['mazes'] if maze['maze'] is not None)
        if maze_count >= 7:
            print("You have reached the maximum number of saved mazes (7). Please delete a maze before saving a new one.")
            return False
        for maze in user_info['mazes']:
            if maze['maze'] is None:
                maze['maze'] = {
                    'maze_now': maze_data['maze_now'],
                    'maze_solver': maze_data['maze_solver'],
                    'hero_now': maze_data['hero_now'],
                    'num_steps': maze_data['num_steps'],
                    'time': maze_data['time'],
                    'Difficulty': maze_data['Difficulty'],
                }
                break
    updated_users[username] = user_info

    try:
        with open(filename, 'wb') as f:
            pickle.dump(updated_users, f)
    except Exception as e:
        logging.error(f"An error occurred while saving users: {str(e)}")
        return False

    return True
def update_pickle_file(user_data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(user_data, f)
def load_users(filename, Username = None, number = None):
    try:
        with open(filename, 'rb') as f:
            users = pickle.load(f)
    except (EOFError, FileNotFoundError):
        return []
    if Username is not None:
        # Get the first (and probably only) key in the selected_user dictionary
        key = list(users[Username].keys())[1]
        user_info = users.get(key, {})
        return user_info.get('mazes', [])
    if Username and number is not None:
        # Get the first (and probably only) key in the selected_user dictionary
        key = list(users[Username].keys())[1]
        user_info = users.get(key, {})
        return user_info.get('mazes', [])[number]
    return users