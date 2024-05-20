import sys
import pygame
import pickle
import os
import cfg
import Main
from modules.Textbox import *
from modules.Accounts import *
from modules.Load_Game import *



'''Game start / level switching / game end interface'''


def Interface(screen, cfg, mode='game_start'):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    clock = pygame.time.Clock()
    Interface_Running = True
    while Interface_Running:
        screen.fill((192, 192, 192))

        buttons = []
        if mode == 'game_start':
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'START', font))
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'LOAD GAME', font))
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'QUIT', font))
        elif mode == 'game_switch':
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'NEXT', font))
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'MAIN MENU', font))
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'QUIT', font))
        elif mode == 'game_end':
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'RESTART', font))
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'MAIN MENU', font))   
            buttons.append(Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'QUIT', font))
        # elif mode == 'game_save':
        #     with open('data.pkl', 'rb') as f:
        #         all_data = pickle.load(f)
        else:
            raise ValueError('Interface.mode unsupport <%s>...' % mode)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    expanded_button = button.inflate(130, 130)
                    if expanded_button.collidepoint(pygame.mouse.get_pos()):
                        print("Button clicked") 
                        if i == len(buttons) - 1:  # If the last button (quit button) is clicked
                            pygame.quit()
                            sys.exit(-1)
                        # elif mode == 'game_start' and i == 0:  # If the second button (load game button) is clicked
                        #     Interface_Load_Game(screen, cfg)
                        elif mode == 'game_start' and i == 1:  # Load_Game
                            Interface_Load_Game(screen, cfg) 
                        elif (mode == 'game_switch' or 'game_end') and i == 1:  #Main_Menu
                            Interface(screen, cfg, mode = 'game_start')
                        else:
                            return True  # If any other button is clicked

        pygame.display.update()
        clock.tick(cfg.FPS)


def Interface_Difficulty(screen, cfg):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    clock = pygame.time.Clock()
    while True:
        screen.fill((192, 192, 192))
        easy_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'EASY', font)
        medium_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'MEDIUM', font)
        hard_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'HARD', font)
        main_menu_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)*2), 'MAIN MENU', font)
        expanded_easy_button = easy_button.inflate(130, 130)
        expanded_medium_button = medium_button.inflate(130, 130)
        expanded_hard_button = hard_button.inflate(130, 130)
        expanded_main_menu_button = main_menu_button.inflate(130, 130)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if expanded_easy_button.collidepoint(pygame.mouse.get_pos()):
                    return True, (20, 20), 'easy'
                elif expanded_medium_button.collidepoint(pygame.mouse.get_pos()):
                    return True, (40, 40), 'medium'
                elif expanded_hard_button.collidepoint(pygame.mouse.get_pos()):
                    return True, (100, 100), 'hard'
                elif expanded_main_menu_button.collidepoint(pygame.mouse.get_pos()):
                    Interface(screen, cfg, mode='game_start')

        pygame.display.update()
        clock.tick(cfg.FPS)
def Mode_Option(screen,cfg):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    clock = pygame.time.Clock()
    while True:
            screen.fill((192, 192, 192))
            easy_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'EASY', font)
            medium_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'MEDIUM', font)
            hard_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'HARD', font)
            expanded_easy_button = easy_button.inflate(130, 130)
            expanded_medium_button = medium_button.inflate(130, 130)
            expanded_hard_button = hard_button.inflate(130, 130)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if expanded_easy_button.collidepoint(pygame.mouse.get_pos()):
                        return True, (20, 20), 'easy'
                    elif expanded_medium_button.collidepoint(pygame.mouse.get_pos()):
                        return True, (40, 40), 'medium'
                    elif expanded_hard_button.collidepoint(pygame.mouse.get_pos()):
                        return True, (100, 100), 'hard'

            pygame.display.update()
            clock.tick(cfg.FPS)
def Interface_Load_Game(screen, cfg):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    clock = pygame.time.Clock()
    user_data=load_users('users_data.pkl')
    while True:
        screen.fill((192, 192, 192))
        main_menu_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'MAIN MENU', font)
        exit_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'EXIT', font)
        expanded_main_menu_button = main_menu_button.inflate(130, 130)
        expanded_exit_button = exit_button.inflate(130, 130)
        showText(screen, font, 'USERNAME: qyan8', (0, 0, 0), ((cfg.SCREENSIZE[0]-700)//2, cfg.SCREENSIZE[1]//2.5))
        # Display numbers 1 to 7 as text
        play_buttons=[]
        exit_buttons=[]
        for i in range(1, 8):
            showText(screen, font, str(i)+'.', (0, 0, 0), ((cfg.SCREENSIZE[0]-700)//2, cfg.SCREENSIZE[1]//2.5 + i*50))
            maze_data = user_data['qyan8']['mazes'][i-1]['maze']
            if maze_data is not None:
                # maze_now = maze_data['maze_now']
                # maze_solver = maze_data['maze_solver']
                # hero_now = maze_data['hero_now']
                num_steps = maze_data['num_steps']
                Difficulty = maze_data['Difficulty']
                showText(screen, font, f'Used Steps: {num_steps}, Difficulty: {Difficulty}', (0, 0, 0), ((cfg.SCREENSIZE[0]-700)//2+30, cfg.SCREENSIZE[1]//2.5 + i*50))
                play_buttons.append(HalfButton(screen, ((cfg.SCREENSIZE[0]+600)//2, cfg.SCREENSIZE[1]//2.6 + i*50), 'PLAY', font))
                exit_buttons.append(HalfButton(screen, ((cfg.SCREENSIZE[0]+600)//2+150, cfg.SCREENSIZE[1]//2.6 + i*50), 'DEL', font))
            else:
                showText(screen, font, 'No maze data', (0, 0, 0), ((cfg.SCREENSIZE[0]-700)//2+30, cfg.SCREENSIZE[1]//2.5 + i*50))
            
            # Display the username as text
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(play_buttons):
                    expanded_button = button.inflate(100, 100)
                    if expanded_button.collidepoint(pygame.mouse.get_pos()):
                        Main.main(cfg)
                for i, button in enumerate(exit_buttons):
                    expanded_button = button.inflate(100, 100)
                    if expanded_button.collidepoint(pygame.mouse.get_pos()):
                        return True
                if expanded_exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit(-1)
                elif expanded_main_menu_button.collidepoint(pygame.mouse.get_pos()):
                    Interface(screen, cfg, 'game_start')

        pygame.display.update()
        clock.tick(cfg.FPS)

    