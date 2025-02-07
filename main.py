import pygame, sys, random

# Initialisation de Pygame
pygame.init()

# --- Création de la fenêtre en plein écran ---
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Application LED Pygame")

clock = pygame.time.Clock()

# --- Définition de la matrice LED ---
matrix_width = 26
matrix_height = 104

# Création d'une surface "LED" en résolution native 
led_surface = pygame.Surface((matrix_width, matrix_height))

# La matrice qui contient la couleur de chaque pixel (initialement noir)
led_matrix = [[(0, 0, 0) for _ in range(matrix_width)] for _ in range(matrix_height)]

# Couleur courante utilisée pour l'animation (par défaut blanche)
current_color = (255, 255, 255)

# Mode d'animation : "normal" pour le décalage avec la couleur sélectionnée,
# "neige" pour l'effet de neige.
mode = "normal"

# --- Définition des zones (positions et tailles) ---
# 1. Zone LED native (pour la capture externe)
led_area_pos = (64, 63)  # modifiez cette position selon vos besoins

# 2. Rendu utilisateur (zoomé) : chaque pixel de la matrice est agrandi
# Ici, on inverse largeur et hauteur pour obtenir l'effet renversé
user_view_pos = (200, 50)  # position modifiable
user_view_scale = 10
user_view_size = (matrix_height * user_view_scale, matrix_width * user_view_scale)

# 3. Boutons (4 boutons) – on place les boutons horizontalement avec un petit écart
button_width = 150
button_height = 50
button_gap = 20
button1_rect = pygame.Rect(50, 400, button_width, button_height)  # Rouge
button2_rect = pygame.Rect(button1_rect.right + button_gap, 400, button_width, button_height)  # Vert
button3_rect = pygame.Rect(button2_rect.right + button_gap, 400, button_width, button_height)  # Bleu
button4_rect = pygame.Rect(button3_rect.right + button_gap, 400, button_width, button_height)  # Neige

# --- Fonctions d'actualisation et de dessin ---

def update_led_surface():
    """
    Met à jour la surface led_surface à partir de la matrice led_matrix.
    """
    for y in range(matrix_height):
        for x in range(matrix_width):
            led_surface.set_at((x, y), led_matrix[y][x])

def update_matrix():
    """
    Mode "normal" : décalage de chaque ligne en insérant la couleur courante
    en début de ligne et en supprimant le dernier pixel.
    """
    for y in range(matrix_height):
        row = led_matrix[y]
        row.insert(0, current_color)
        row.pop()

def update_neige():
    """
    Mode "neige" : simule la chute de flocons blancs.
    - On décale toutes les lignes vers le bas.
    - On crée, dans la première ligne, des pixels blancs apparaissant aléatoirement.
    """
    # Décalage vers le bas
    for y in range(matrix_height - 1, 0, -1):
        for x in range(matrix_width):
            led_matrix[y][x] = led_matrix[y - 1][x]
    # Pour chaque colonne de la première ligne, on ajoute un flocon avec une certaine probabilité
    for x in range(matrix_width):
        if random.random() < 0.1:  # 10% de chance d'apparition d'un flocon blanc
            led_matrix[0][x] = (255, 255, 255)
        else:
            led_matrix[0][x] = (0, 0, 0)

def draw_buttons(surface, font):
    """
    Dessine les 4 boutons avec leur fond coloré et leur libellé.
    """
    pygame.draw.rect(surface, (200, 0, 0), button1_rect)  # bouton rouge
    pygame.draw.rect(surface, (0, 200, 0), button2_rect)  # bouton vert
    pygame.draw.rect(surface, (0, 0, 200), button3_rect)  # bouton bleu
    pygame.draw.rect(surface, (120, 120, 120), button4_rect)  # bouton neige (gris)
    
    text1 = font.render("Rouge", True, (255, 255, 255))
    text2 = font.render("Vert", True, (255, 255, 255))
    text3 = font.render("Bleu", True, (255, 255, 255))
    text4 = font.render("Neige", True, (255, 255, 255))
    surface.blit(text1, (button1_rect.x + 10, button1_rect.y + 10))
    surface.blit(text2, (button2_rect.x + 10, button2_rect.y + 10))
    surface.blit(text3, (button3_rect.x + 10, button3_rect.y + 10))
    surface.blit(text4, (button4_rect.x + 10, button4_rect.y + 10))

# Préparation d'une police pour le texte des boutons
font = pygame.font.SysFont("Arial", 24)

# --- Boucle principale ---
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Quitter en appuyant sur Echap
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Bouton Rouge
            if button1_rect.collidepoint(mouse_pos):
                current_color = (255, 0, 0)
                mode = "normal"  # On repasse en mode normal
                # Remplit toute la matrice de la couleur sélectionnée
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color
            # Bouton Vert
            elif button2_rect.collidepoint(mouse_pos):
                current_color = (0, 255, 0)
                mode = "normal"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color
            # Bouton Bleu
            elif button3_rect.collidepoint(mouse_pos):
                current_color = (0, 0, 255)
                mode = "normal"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color
            # Bouton Neige
            elif button4_rect.collidepoint(mouse_pos):
                mode = "neige"
                # On remet la matrice à zéro (fond noir) pour le mode neige
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)

    # Mise à jour de la matrice en fonction du mode choisi
    if mode == "normal":
        update_matrix()
    elif mode == "neige":
        update_neige()

    # Mise à jour de la surface LED à partir de la matrice
    update_led_surface()

    # Effacer l'écran (fond gris foncé)
    screen.fill((30, 30, 30))

    # --- Dessin des zones ---
    # 1. Zone LED native (affichage en résolution native)
    screen.blit(led_surface, led_area_pos)

    # 2. Rendu utilisateur (zoomé)
    zoomed_surface = pygame.transform.scale(led_surface, user_view_size)
    screen.blit(zoomed_surface, user_view_pos)

    # 3. Boutons
    draw_buttons(screen, font)

    # Actualisation de l'écran et limitation à 30 FPS
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
