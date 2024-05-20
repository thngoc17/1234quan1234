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
	
	User_Info = load_users('users_data.pkl')
	print(User_Info)
	
	if Siuu:
		Interface_Game_Start(screen, cfg)
		# Interface_Load_Game(screen, cfg)
		# Interface_Difficulty(screen, cfg)
		_,MAZESIZE,Difficulty_Level = Interface_Difficulty(screen, cfg)
		BLOCKSIZE = 600//MAZESIZE[0]
	Loading_Bar(screen, cfg)
	
	
	
	# Record the number of levels
	num_levels = 0
	# Record the minimum steps to clear
	best_scores = 'None'
	# Cycle through levels
	while True:
		num_levels += 1
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode(cfg.SCREENSIZE)
		# --Randomly generate level maps
		maze_now = RandomMaze(MAZESIZE, BLOCKSIZE, cfg.BORDERSIZE)
		# --Generate maze solver
		maze_solver = Maze_solver(maze_now, screen)
		# --Generate hero
		hero_now = Hero(cfg.HEROPICPATH, list(maze_solver.start.coordinate), BLOCKSIZE, cfg.BORDERSIZE)
		
		# --Statistics steps
		num_steps = 0
		
		# --Main loop within the level
		solution = None
		draw_solution=False
		
		while True:
			dt = clock.tick(cfg.FPS)
			screen.fill(oak_wood_color)
			is_move = False
			solution = maze_solver.a_star_search(maze_now.blocks_list[hero_now.coordinate[1]][hero_now.coordinate[0]])
			hero_now.draw(screen)
			maze_now.draw(screen)
			estimated_steps= len(maze_solver.a_star_search(maze_now.blocks_list[hero_now.coordinate[1]][hero_now.coordinate[0]]))
			# ---Show some info
			showText(screen, font, 'LEVELDONE: %d' % num_levels, (255, 0, 0), (10, 10))
			showText(screen, font, 'BESTSCORE: %s' % best_scores, (255, 0, 0), (210, 10))
			showText(screen, font, 'USEDSTEPS: %s' % num_steps, (255, 0, 0), (410, 10))
			showText(screen, font, 'ESTIMATED STEPS: %s' % estimated_steps, (255, 0, 0), (610, 10))
			
			# Start and end signs
			showText(screen, font, 'S', (255, 0, 0), (maze_solver.start.coordinate[0]*BLOCKSIZE+cfg.BORDERSIZE[0], maze_solver.start.coordinate[1]*BLOCKSIZE+cfg.BORDERSIZE[1]-17))
			showText(screen, font, 'D', (255, 0, 0), (maze_solver.end.coordinate[0]*BLOCKSIZE+cfg.BORDERSIZE[0], maze_solver.end.coordinate[1]*BLOCKSIZE+cfg.BORDERSIZE[1]+17))
			key_to_direction = {
				pygame.K_UP: 'up',
				pygame.K_DOWN: 'down',
				pygame.K_LEFT: 'left',
				pygame.K_RIGHT: 'right',
			}
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(-1)
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					mods = pygame.key.get_mods()
					if event.key in key_to_direction:
						direction = key_to_direction[event.key]
						is_move = hero_now.move(direction, maze_now)
					elif event.key == pygame.K_r:
						hero_now.coordinate[0] = maze_solver.end.coordinate[0]
						hero_now.coordinate[1] = maze_solver.end.coordinate[1]
					elif event.key == pygame.K_SPACE:
						draw_solution = True
						# maze_solver=Maze_solver(maze_now, screen, hero_now.coordinate)
						
					elif event.key == pygame.K_BACKSPACE:
						draw_solution = False
						
					elif mods & pygame.KMOD_CTRL and keys[pygame.K_s]:
						save_users(Username, Password, 'users_data.pkl', {'maze_now': maze_now, 'maze_solver': maze_solver, 'hero_now': hero_now, 'num_steps': num_steps, "Difficulty": Difficulty_Level})
					
					if is_move:
						num_steps += 1							
			# ----↑↓←→Control hero
			if draw_solution:
				current = maze_solver.end
				while current in solution:
					prev = current
					current = solution[current]
					pygame.draw.line(screen, (0, 255, 0), 
									(prev.coordinate[0]*BLOCKSIZE + cfg.BORDERSIZE[0] + BLOCKSIZE//2, prev.coordinate[1]*BLOCKSIZE + cfg.BORDERSIZE[1] + BLOCKSIZE//2), 
									(current.coordinate[0]*BLOCKSIZE + cfg.BORDERSIZE[0] + BLOCKSIZE//2, current.coordinate[1]*BLOCKSIZE + cfg.BORDERSIZE[1] + BLOCKSIZE//2), 
									BLOCKSIZE//4)
				pygame.display.update()
			if (hero_now.coordinate[0] == maze_solver.end.coordinate[0]) and (hero_now.coordinate[1] == maze_solver.end.coordinate[1]):
				break
			pygame.display.update()
		
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
	