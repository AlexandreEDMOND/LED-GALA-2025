import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# --- Création de la fenêtre en plein écran ---
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("LED Matrix – Boutons et Neige")

clock = pygame.time.Clock()
clock.tick(30)

# --- Définition de la matrice LED canonique ---
matrix_width = 104    # nombre de colonnes
matrix_height = 26  # nombre de lignes

# La matrice de base contenant les infos de chaque LED (initialement noire)
led_matrix = [[(0, 0, 0) for _ in range(matrix_width)] for _ in range(matrix_height)]

# Création d'une surface "canonique" de taille (26, 104)
led_surface = pygame.Surface((matrix_width, matrix_height))

def update_led_surface():
    """
    Met à jour la surface 'led_surface' en copiant la couleur de chaque pixel
    depuis la matrice 'led_matrix'.
    """
    for y in range(matrix_height):
        for x in range(matrix_width):
            led_surface.set_at((x, y), led_matrix[y][x])

def update_matrix():
    """
    Mode NORMAL :
    Pour chaque ligne de la matrice, on insère en début de ligne la couleur
    courante (current_color) puis on retire le dernier pixel, simulant ainsi un décalage.
    """
    for y in range(matrix_height):
        row = led_matrix[y]
        row.insert(0, current_color)
        row.pop()

def update_neige():
    """
    Mode NEIGE :
    On décale toutes les lignes vers le bas et on met à jour la première ligne de façon
    aléatoire pour simuler l'apparition de flocons blancs (probabilité de 10% par pixel).
    """
    # Décalage vertical vers le bas
    for y in range(matrix_height - 1, 0, -1):
        for x in range(matrix_width):
            led_matrix[y][x] = led_matrix[y - 1][x]
    # Première ligne : apparition aléatoire de flocons blancs
    for x in range(matrix_width):
        if random.random() < 0.05:  # 10% de chance
            led_matrix[0][x] = (255, 255, 255)
        else:
            led_matrix[0][x] = (0, 0, 0)

# --- Boutons ---
# Définition des rectangles (position et taille)
button_width = 150
button_height = 50
button_gap = 20
# On place les boutons en bas de l'écran (ajustez 'base_y' selon vos besoins)
base_y = screen_height - 70
button1_rect = pygame.Rect(50, base_y, button_width, button_height)                     # Rouge
button2_rect = pygame.Rect(50 + (button_width + button_gap), base_y, button_width, button_height)  # Vert
button3_rect = pygame.Rect(50 + 2*(button_width + button_gap), base_y, button_width, button_height)  # Bleu
button4_rect = pygame.Rect(50 + 3*(button_width + button_gap), base_y, button_width, button_height)  # Neige
button5_rect = pygame.Rect(50 + 4*(button_width + button_gap), base_y, button_width, button_height)  # Logo BDF
button6_rect = pygame.Rect(50 + 5*(button_width + button_gap), base_y, button_width, button_height)  # Logo Gala

def draw_buttons(surface, font):
    """
    Dessine les 4 boutons avec leur fond coloré et leur libellé.
    """
    pygame.draw.rect(surface, (200, 0, 0), button1_rect)   # Bouton Rouge
    pygame.draw.rect(surface, (0, 200, 0), button2_rect)   # Bouton Vert
    pygame.draw.rect(surface, (0, 0, 200), button3_rect)   # Bouton Bleu
    pygame.draw.rect(surface, (120, 120, 120), button4_rect)  # Bouton Neige (gris)
    pygame.draw.rect(surface, (120, 120, 120), button5_rect)  # Bouton BDF
    pygame.draw.rect(surface, (120, 120, 120), button6_rect)  # Bouton Gala

    
    text1 = font.render("Rouge", True, (255, 255, 255))
    text2 = font.render("Vert", True, (255, 255, 255))
    text3 = font.render("Bleu", True, (255, 255, 255))
    text4 = font.render("Neige", True, (255, 255, 255))
    text5 = font.render("BDF", True, (255, 255, 255))
    text6 = font.render("Gala", True, (255, 255, 255))
    surface.blit(text1, (button1_rect.x + 10, button1_rect.y + 10))
    surface.blit(text2, (button2_rect.x + 10, button2_rect.y + 10))
    surface.blit(text3, (button3_rect.x + 10, button3_rect.y + 10))
    surface.blit(text4, (button4_rect.x + 10, button4_rect.y + 10))
    surface.blit(text5, (button5_rect.x + 10, button5_rect.y + 10))
    surface.blit(text6, (button6_rect.x + 10, button6_rect.y + 10))

# Préparation d'une police pour le texte
font = pygame.font.SysFont("Arial", 24)

# --- Définition des vues d'affichage ---
# 1. Vue native rotatée de -90° (la surface sera tournée, passant de 26x104 à 104x26)
rotated_view_pos = (65, 60)

# 2. Vue agrandie x10 (chaque pixel de la matrice devient un carré de 10x10)
enlarged_view_pos = (300, 50)
scale_factor = 10
enlarged_size = (matrix_width * scale_factor, matrix_height * scale_factor)  # (26*10, 104*10)

# --- Variables de mode ---
# mode = "normal" pour décalage horizontal, mode = "neige" pour effet de chute de neige
mode = "normal"
current_color = (255, 255, 255)  # Couleur par défaut pour le mode normal

# --- Boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Quitter en appuyant sur Échap
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Bouton Rouge
            if button1_rect.collidepoint(mouse_pos):
                current_color = (255, 0, 0)
                mode = "normal"
                # Remplit toute la matrice de rouge
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
                current_color = (255, 140, 26)
                mode = "normal"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color
            # Bouton Neige
            elif button4_rect.collidepoint(mouse_pos):
                mode = "neige"

                # Réinitialise la matrice avec un fond noir
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)
            # Bouton Logo BDF
            elif button5_rect.collidepoint(mouse_pos):
                mode = "affichage_bdf"

                # Réinitialise la matrice avec un fond noir
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)
            # Bouton Logo BDF
            elif button6_rect.collidepoint(mouse_pos):
                mode = "affichage_gala"

                # Réinitialise la matrice avec un fond noir
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)
                
                        
    # Mise à jour de la matrice selon le mode
    if mode == "normal":
        update_matrix()
    elif mode == "neige":
        # Met en pause pendant 0.1 seconde
        pygame.time.wait(40)
        update_neige()
    elif mode == "affichage_bdf":
        # Affiche l'image
        img = pygame.image.load('img/Banderoles BDF (5).png')
        img = pygame.transform.scale(img, (matrix_width, matrix_height))
        for y in range(matrix_height):
            for x in range(matrix_width):
                led_matrix[y][x] = img.get_at((x, y))
    elif mode == "affichage_gala":
        # Affiche l'image
        # img = pygame.image.load('img/Banderoles BDF (6).png')
        img = pygame.image.load('img/feu de cheminée.jpg')
        img = pygame.transform.scale(img, (matrix_width, matrix_height))
        for y in range(matrix_height):
            for x in range(matrix_width):
                led_matrix[y][x] = img.get_at((x, y))
    
    # Mise à jour de la surface à partir de la matrice
    update_led_surface()
    
    # --- Création des vues d'affichage ---
    # Vue rotatée de -90°
    rotated_surface = pygame.transform.rotate(led_surface, 90)
    # Vue agrandie x10 (conserve l'orientation canonique)
    enlarged_surface = pygame.transform.scale(led_surface, enlarged_size)
    
    # --- Affichage ---
    screen.fill((30, 30, 30))  # fond gris foncé
    screen.blit(rotated_surface, rotated_view_pos)
    screen.blit(enlarged_surface, enlarged_view_pos)
    draw_buttons(screen, font)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
