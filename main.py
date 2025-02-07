import pygame, sys

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

# --- Définition des zones (positions et tailles) ---
# 1. Zone LED native (pour la capture externe)
led_area_pos = (64, 63)  # modifiez cette position selon vos besoins

# 2. Rendu utilisateur (zoomé) : chaque pixel de la matrice devient 10x10, soit 1280x320 pixels
user_view_pos = (200, 50)  # position modifiable
user_view_scale = 10
user_view_size = (matrix_width * user_view_scale, matrix_height * user_view_scale)  # (1280, 320)

# Si vous souhaitez afficher une version "renversée" (par exemple en pivotant la matrice),
# vous pouvez utiliser pygame.transform.rotate ou pygame.transform.flip.
# Exemple (commenté) : rotation de 90° avant le zoom
rotated = pygame.transform.rotate(led_surface, 90)
rotated_zoom_size = (matrix_height * user_view_scale, matrix_width * user_view_scale)  # (320, 1280)

# 3. Boutons (3 boutons) – ici nous les plaçons horizontalement avec un petit écart
button_width = 150
button_height = 50
button_gap = 20
button1_rect = pygame.Rect(50, 400, button_width, button_height)
button2_rect = pygame.Rect(button1_rect.right + button_gap, 400, button_width, button_height)
button3_rect = pygame.Rect(button2_rect.right + button_gap, 400, button_width, button_height)
button4_rect = pygame.Rect(button3_rect.right + button_gap, 400, button_width, button_height)

# --- Fonctions d'actualisation et de dessin ---

def update_led_surface():
    """
    Met à jour la surface led_surface à partir de la matrice led_matrix.
    On parcourt chaque pixel et on définit sa couleur.
    """
    for y in range(matrix_height):
        for x in range(matrix_width):
            led_surface.set_at((x, y), led_matrix[y][x])

def update_matrix():
    """
    Exemple d’animation : on déplace chaque ligne en insérant la couleur courante
    au début et en supprimant le dernier pixel.
    Vous pouvez modifier cette fonction pour réaliser l’animation souhaitée.
    """
    for y in range(matrix_height):
        row = led_matrix[y]
        row.insert(0, current_color)  # insère la couleur courante en début de ligne
        row.pop()  # supprime le dernier pixel

def draw_buttons(surface, font):
    """
    Dessine les trois boutons avec un fond coloré et leur texte.
    """
    pygame.draw.rect(surface, (200, 0, 0), button1_rect)  # bouton rouge
    pygame.draw.rect(surface, (0, 200, 0), button2_rect)  # bouton vert
    pygame.draw.rect(surface, (0, 0, 200), button3_rect)  # bouton bleu
    pygame.draw.rect(surface, (0, 200, 200), button4_rect)  # bouton bleu
    
    text1 = font.render("Rouge", True, (255, 255, 255))
    text2 = font.render("Vert", True, (255, 255, 255))
    text3 = font.render("Bleu", True, (255, 255, 255))
    surface.blit(text1, (button1_rect.x + 10, button1_rect.y + 10))
    surface.blit(text2, (button2_rect.x + 10, button2_rect.y + 10))
    surface.blit(text3, (button3_rect.x + 10, button3_rect.y + 10))

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
            # Vérification des clics sur les boutons
            if button1_rect.collidepoint(mouse_pos):
                current_color = (255, 0, 0)
                # Remplit toute la matrice de la couleur sélectionnée
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color
            elif button2_rect.collidepoint(mouse_pos):
                current_color = (0, 255, 0)
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color
            elif button3_rect.collidepoint(mouse_pos):
                current_color = (0, 0, 255)
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color

    # Mise à jour de la matrice (animation)
    update_matrix()
    # Mise à jour de la surface LED à partir de la matrice
    update_led_surface()

    # Effacer l'écran (fond gris foncé)
    screen.fill((30, 30, 30))

    # --- Dessin des zones ---
    # 1. Zone LED native (128x32) – affichée sans mise à l'échelle
    screen.blit(led_surface, led_area_pos)

    # 2. Rendu utilisateur (zoomé) – chaque pixel de led_surface est agrandi
    zoomed_surface = pygame.transform.scale(led_surface, user_view_size)
    screen.blit(zoomed_surface, user_view_pos)

    # Si vous souhaitez afficher la version « renversée » (par exemple pivotée de 90°),
    # décommentez les lignes suivantes et ajustez user_view_size si nécessaire :
    rotated = pygame.transform.rotate(led_surface, 90)
    rotated_zoom = pygame.transform.scale(rotated, user_view_size)
    screen.blit(rotated_zoom, user_view_pos)

    # 3. Boutons
    draw_buttons(screen, font)

    # Actualisation de l'écran et limitation de la boucle à 30 FPS
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
