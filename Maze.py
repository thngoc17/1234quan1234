import cfg
import pygame
import pickle
from modules.misc import *
from modules.mazes import *
from modules.Characters import *
from modules.maze_solver import *
from modules.saver import *	
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
	# Start Interface
	Interface(screen, cfg, 'game_start')
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
		maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE)
		# --Generate maze solver
		maze_solver = Maze_solver(maze_now, screen)
		# --Generate hero
		hero_now = Hero(cfg.HEROPICPATH, list(maze_solver.start.coordinate), cfg.BLOCKSIZE, cfg.BORDERSIZE)
		# --Statistics steps
		num_steps = 0
		# --Main loop within the level
		solution = None
		draw_solution=False
		while True:
			dt = clock.tick(cfg.FPS)
			screen.fill((255, 255, 255))
			is_move = False
			num_steps += int(is_move)
			hero_now.draw(screen)
			maze_now.draw(screen)
			
			# ---Show some info
			showText(screen, font, 'LEVELDONE: %d' % num_levels, (255, 0, 0), (10, 10))
			showText(screen, font, 'BESTSCORE: %s' % best_scores, (255, 0, 0), (210, 10))
			showText(screen, font, 'USEDSTEPS: %s' % num_steps, (255, 0, 0), (410, 10))
			showText(screen, font, 'S: your starting point    D: your destination', (255, 0, 0), (10, 600))
			
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
					if event.key in key_to_direction:
						direction = key_to_direction[event.key]
						is_move = hero_now.move(direction, maze_now)
					elif event.key == pygame.K_r:
						hero_now.coordinate[0] = cfg.MAZESIZE[1] - 1 
						hero_now.coordinate[1] = cfg.MAZESIZE[0] - 1
					elif event.key == pygame.K_SPACE:
						draw_solution = True
						solution = maze_solver.a_star_search()
					elif event.key == pygame.K_BACKSPACE:
						draw_solution = False
						solution = None
					elif event.key == pygame.K_s:
						save_objects(maze_now, maze_solver, hero_now)
					elif event.key == pygame.K_l:
						with open('data.pkl', 'rb') as f:
							data = pickle.load(f)

						# Access the objects from the dictionary
						maze_now = data['maze_now']
						maze_solver = data['maze_solver']
						hero_now = data['hero_now']
						
			# ----↑↓←→Control hero
			if draw_solution and solution:
				# Draw the solution here
				current = maze_solver.end
				while current in solution:
					prev = current
					current = solution[current]
					pygame.draw.line(screen, (0, 255, 0), 
									(prev.coordinate[0]*cfg.BLOCKSIZE + cfg.BORDERSIZE[0] + cfg.BLOCKSIZE//2, prev.coordinate[1]*cfg.BLOCKSIZE + cfg.BORDERSIZE[1] + cfg.BLOCKSIZE//2), 
									(current.coordinate[0]*cfg.BLOCKSIZE + cfg.BORDERSIZE[0] + cfg.BLOCKSIZE//2, current.coordinate[1]*cfg.BLOCKSIZE + cfg.BORDERSIZE[1] + cfg.BLOCKSIZE//2), 
									cfg.BLOCKSIZE//4)
				pygame.display.update()
			if (hero_now.coordinate[0] == cfg.MAZESIZE[1] - 1) and (hero_now.coordinate[1] == cfg.MAZESIZE[0] - 1):
				break
			pygame.display.update()
		
		# ---Update Best Score
		if best_scores == 'None':
			best_scores = num_steps
		else:
			if best_scores > num_steps:
				best_scores = num_steps
		# --Level switching
		Interface(screen, cfg, mode='game_switch')


'''run'''
if __name__ == '__main__':
	main(cfg)