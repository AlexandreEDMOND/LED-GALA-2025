import pygame

def create_fullscreen_window():
    pygame.init()
    
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        screen.fill((0, 0, 0))
        
        # Petit rectangle en haut à gauche
        rect1_x, rect1_y = 10, 10
        rect1_width, rect1_height = 26, 104
        pygame.draw.rect(screen, (255, 0, 0), (rect1_x, rect1_y, rect1_width, rect1_height))
        
        pygame.display.flip()
    
    pygame.quit()

create_fullscreen_window()

