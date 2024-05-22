import pickle
import os
import copy

def save_to_leaderboard(difficulty, username, used_steps, time):
    # Load existing leaderboard data
    try:
        with open('leaderboard.pkl', 'rb') as f:
            leaderboard_data = pickle.load(f)
    except (FileNotFoundError, EOFError):
        leaderboard_data = {'easy': [], 'medium': [], 'hard': []}
    if difficulty not in leaderboard_data:
        leaderboard_data[difficulty] = []
    # Add new player data
    leaderboard_data[difficulty].append({
        'Players': username,
        'used_steps': used_steps,
        'time': time
    })
    # Sort players by used_steps in ascending order, then by time in ascending order
    leaderboard_data[difficulty].sort(key=lambda x: (x['used_steps'], x['time']))
    # Assign ranks based on order in the list
    last_steps = None
    last_time = None
    number = 0
    for player_data in leaderboard_data[difficulty]:
        if player_data['used_steps'] != last_steps or player_data['time'] != last_time:
            number += 1
        player_data['number'] = number
        last_steps = player_data['used_steps']
        last_time = player_data['time']
    # Save leaderboard data
    with open('leaderboard.pkl', 'wb') as f:
        pickle.dump(leaderboard_data, f)

def load_leaderboard():
    try:
        with open('leaderboard.pkl', 'rb') as f:
            leaderboard_data = pickle.load(f)
    except (FileNotFoundError, EOFError):
        leaderboard_data = None
    return leaderboard_data

print(load_leaderboard())