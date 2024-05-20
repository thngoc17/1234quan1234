import pygame
import sys
from modules.Main_Screen import *
from modules.Textbox import *
from modules.Accounts import *

def UserInterface(screen, cfg, mode):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    font_small = pygame.font.SysFont('Consolas', 20)
    clock = pygame.time.Clock()
    valid_users = load_users('users_data.pkl')

    if mode == 'interface':
        while True:
            screen.fill((192, 192, 192))
            login_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'LOGIN', font)
            register_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'REGISTER', font)
            exit_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3))), 'EXIT', font)
            expanded_login_button = login_button.inflate(130, 130)
            expanded_register_button = register_button.inflate(130, 130)
            expanded_exit_button = exit_button.inflate(130, 130)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if expanded_exit_button.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
                    elif expanded_login_button.collidepoint(pygame.mouse.get_pos()):
                        return UserInterface(screen, cfg, 'login')
                    elif expanded_register_button.collidepoint(pygame.mouse.get_pos()):
                        return UserInterface(screen, cfg, 'register')
            pygame.display.update()
            clock.tick(cfg.FPS)

    elif mode == 'login':
        username_box = TextBox(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), (200, 50)) 
        password_box = TextBox(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), (200, 50))
        while True:
            screen.fill((192, 192, 192))
            login_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2,(cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'LOGIN', font)
            return_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+2*(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'RETURN', font)
            expanded_login_button = login_button.inflate(130, 130)  
            expanded_return_button = return_button.inflate(130, 130)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if expanded_login_button.collidepoint(pygame.mouse.get_pos()):
                        entered_username = username_box.text
                        entered_password = password_box.text
                        if not entered_username or not entered_password:
                            showText(screen, font, 'Username or password cannot be empty', (255, 0, 0), (cfg.SCREENSIZE[0]//2-100, cfg.SCREENSIZE[1]//2+100))
                        elif entered_username in valid_users and valid_users[entered_username]['password'] == entered_password:
                            return True, entered_username, entered_password
                        else:
                            showText(screen, font, 'Invalid username or password', (255, 0, 0), (cfg.SCREENSIZE[0]//2-100, cfg.SCREENSIZE[1]//2+100))
                    elif expanded_return_button.collidepoint(pygame.mouse.get_pos()):
                        return UserInterface(screen, cfg, 'interface')
                username_box.check_focus(event)
                password_box.check_focus(event)
                username_box.update(event)
                password_box.update(event)
            username_box.draw()
            password_box.draw()
            if username_box.text == '':
                showText(screen, font_small, 'Enter username', (128, 128, 128), ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3+15))
            if password_box.text == '':
                showText(screen, font_small, 'Enter password', (128, 128, 128), ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2+15))
            
            pygame.display.update()
            clock.tick(cfg.FPS)

    elif mode == 'register':
        username_box = TextBox(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), (200, 50)) 
        password_box = TextBox(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), (200, 50))
        confirm_password_box = TextBox(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), (200, 50))
        while True:
            screen.fill((192, 192, 192))
            register_button = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+2*(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'REGISTER', font)
            return_button = Button(screen, ((cfg.SCREENSIZE[0]-00)//2, (cfg.SCREENSIZE[1]//2)+3*(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)), 'RETURN', font)
            expanded_register_button = register_button.inflate(130, 130)
            expanded_return_button = return_button.inflate(130, 130)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if expanded_register_button.collidepoint(pygame.mouse.get_pos()):
                        entered_username = username_box.text
                        entered_password = password_box.text
                        confirm_password = confirm_password_box.text
                        if not entered_username or not entered_password or not confirm_password:
                            showText(screen, font, 'Username, password or confirm password cannot be empty', (255, 0, 0), (cfg.SCREENSIZE[0]//2-100, cfg.SCREENSIZE[1]//2+100))
                        elif entered_username not in valid_users and entered_password == confirm_password:
                            save_users(entered_username, entered_password, 'users_data.pkl')
                            return True, entered_username, entered_password
                        else:
                            showText(screen, font, 'Passwords do not match or Username already exists', (255, 0, 0), (cfg.SCREENSIZE[0]//2-100, cfg.SCREENSIZE[1]//2+100))
                    elif expanded_return_button.collidepoint(pygame.mouse.get_pos()):
                        return UserInterface(screen, cfg, 'interface')
                username_box.check_focus(event)
                password_box.check_focus(event)
                confirm_password_box.check_focus(event)
                username_box.update(event)
                password_box.update(event)
                confirm_password_box.update(event)
                
            username_box.draw()
            password_box.draw()
            confirm_password_box.draw()
            if username_box.text == '':
                showText(screen, font_small, 'Enter username', (128, 128, 128), ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3+15))
            if password_box.text == '':
                showText(screen, font_small, 'Enter password', (128, 128, 128), ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2+15))
            if confirm_password_box.text == '':
                showText(screen, font_small, 'Confirm password', (128, 128, 128), ((cfg.SCREENSIZE[0]-200)//2, (cfg.SCREENSIZE[1]//2)+(cfg.SCREENSIZE[1]//2-cfg.SCREENSIZE[1]//3)+15))
            pygame.display.update()
            clock.tick(cfg.FPS)
def validate_credentials(username, password, confirm_password=None):
    valid_users = load_users('users_data.pkl')
    if username in valid_users:
        if confirm_password is None:  # For Login
            return valid_users[username]['password'] == password
        else:  # For Register
            return password == confirm_password
    else:
        return False
        