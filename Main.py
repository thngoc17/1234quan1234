import cfg
import pygame

import pickle
import sys
from modules.Main_Screen import *
from modules.Maze_Generator import *
from modules.Hero import *
from modules.Maze_Solver import *
from modules.Login_System import *
from modules.Load_Game import *
from modules.Loading_bar import *

oak_wood_color = (139, 69, 19) 
'''Main function'''

        

def main(cfg):
	# intialization
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()
	# pygame.mixer.music.load(cfg.BGMPATH)
	# pygame.mixer.music.play(-1, 0.0)
	screen = pygame.display.set_mode(cfg.SCREENSIZE)
	pygame.display.set_caption('2D MAZE')
	font = pygame.font.SysFont('Consolas', 15)
	
	Siuu, Username, Password = UserInterface(screen, cfg, 'interface')
	
	User_Info = load_users('Data_Users.pkl')
	print(User_Info)
	
	# Record the number of levels
	num_levels = 0
	# Record the minimum steps to clear
	best_scores = 'None'
	# Cycle through levels
	while True:
		if Siuu:
		# Interface_Load_Game(screen, cfg)
		# Interface_Difficulty(screen, cfg)
			MAZESIZE, BLOCKSIZE, maze_now, maze_solver, hero_now, num_steps, Difficulty_Level = Interface(screen, cfg, Username, Password)
					
		Loading_Bar(screen, cfg)
		num_levels += 1
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode(cfg.SCREENSIZE)
		# --Randomly generate level maps
		
		# --Main loop within the level
		solution = None
		draw_solution=False
		Interface_Game_Play(screen, cfg, font, clock, maze_now, maze_solver, hero_now, draw_solution, num_steps, num_levels, best_scores, Difficulty_Level, BLOCKSIZE, oak_wood_color, Username, Password)
		# ---Update Best Score
		if best_scores == 'None':
			best_scores = num_steps
		else:
			if best_scores > num_steps:
				best_scores = num_steps
		# --Level switching
		Interface_Game_Switch(screen, cfg)



'''run'''
if __name__ == '__main__':
	main(cfg)
	