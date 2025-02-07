import pygame
import sys
import random
import math

# Initialisation de Pygame
pygame.init()

# --- Création de la fenêtre en plein écran ---
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("LED Matrix – Boutons et Effets")

clock = pygame.time.Clock()

# --- Définition de la matrice LED ---
matrix_width = 104  # Colonnes
matrix_height = 26  # Lignes

# Dégradé animé
gradient_step = 0  # Étape pour l'animation du dégradé
gradient_speed = 0.01  # Vitesse du dégradé (ajustez pour ralentir/accélérer)

# Matrice initiale (noire)
led_matrix = [[(0, 0, 0) for _ in range(matrix_width)] for _ in range(matrix_height)]

# Surface pour la matrice LED
led_surface = pygame.Surface((matrix_width, matrix_height))


def update_led_surface():
    """Mise à jour de la surface à partir de la matrice LED."""
    for y in range(matrix_height):
        for x in range(matrix_width):
            led_surface.set_at((x, y), led_matrix[y][x])

def update_matrix():
    """Décalage horizontal pour le mode normal."""
    for y in range(matrix_height):
        row = led_matrix[y]
        row.insert(0, current_color)
        row.pop()

def update_neige():
    """Effet de neige."""
    for y in range(matrix_height - 1, 0, -1):
        for x in range(matrix_width):
            led_matrix[y][x] = led_matrix[y - 1][x]
    
    for x in range(matrix_width):
        led_matrix[0][x] = (255, 255, 255) if random.random() < 0.05 else (0, 0, 0)


import math
import colorsys
import random

def generate_initial_gradient():
    """Génère un dégradé où chaque pixel est aléatoire puis adouci avec ses voisins."""
    gradient_matrix = [[(0, 0, 0) for _ in range(matrix_width)] for _ in range(matrix_height)]

    # Initialisation de la matrice avec des couleurs totalement aléatoires
    for y in range(matrix_height):
        for x in range(matrix_width):
            hue = random.random()  # Teinte aléatoire (0.0 à 1.0)
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)  # Conversion en RGB
            gradient_matrix[y][x] = (int(r * 255), int(g * 255), int(b * 255))

    # Application d'une moyenne avec les pixels voisins pour adoucir le rendu
    smoothed_matrix = [[(0, 0, 0) for _ in range(matrix_width)] for _ in range(matrix_height)]

    for y in range(matrix_height):
        for x in range(matrix_width):
            total_r, total_g, total_b, count = 0, 0, 0, 0

            # Parcours des voisins (et du pixel lui-même)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < matrix_height and 0 <= nx < matrix_width:
                        r, g, b = gradient_matrix[ny][nx]
                        total_r += r
                        total_g += g
                        total_b += b
                        count += 1
            
            # Moyenne des couleurs
            smoothed_matrix[y][x] = (total_r // count, total_g // count, total_b // count)

    # Copier la matrice lissée dans la matrice LED
    for y in range(matrix_height):
        for x in range(matrix_width):
            led_matrix[y][x] = smoothed_matrix[y][x]


def animate_gradient():
    """Anime le dégradé en faisant varier la teinte sans recalculer la diffusion."""
    global trance

    for y in range(matrix_height):
        for x in range(matrix_width):
            # Convertir la couleur actuelle en HSV
            r, g, b = led_matrix[y][x]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

            # Faire évoluer la teinte de manière fluide
            h = (h + 0.05) % 1.0  # Rotation lente de la teinte

            # Reconvertir en RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            led_matrix[y][x] = (int(r * 255), int(g * 255), int(b * 255))
    
    




# --- Boutons ---
button_width = 150
button_height = 50
button_gap = 20
base_y = screen_height - 70

button1_rect = pygame.Rect(50, base_y, button_width, button_height)  # Rouge
button2_rect = pygame.Rect(50 + (button_width + button_gap), base_y, button_width, button_height)  # Vert
button3_rect = pygame.Rect(50 + 2 * (button_width + button_gap), base_y, button_width, button_height)  # Bleu
button4_rect = pygame.Rect(50 + 3 * (button_width + button_gap), base_y, button_width, button_height)  # Neige
button5_rect = pygame.Rect(50 + 4 * (button_width + button_gap), base_y, button_width, button_height)  # BDF
button6_rect = pygame.Rect(50 + 5 * (button_width + button_gap), base_y, button_width, button_height)  # Gala
button7_rect = pygame.Rect(50 + 6 * (button_width + button_gap), base_y, button_width, button_height)  # Dégradé

def draw_buttons(surface, font):
    """Affichage des boutons avec texte."""
    pygame.draw.rect(surface, (200, 0, 0), button1_rect)  # Rouge
    pygame.draw.rect(surface, (0, 200, 0), button2_rect)  # Vert
    pygame.draw.rect(surface, (0, 0, 200), button3_rect)  # Bleu
    pygame.draw.rect(surface, (120, 120, 120), button4_rect)  # Neige
    pygame.draw.rect(surface, (120, 120, 120), button5_rect)  # BDF
    pygame.draw.rect(surface, (120, 120, 120), button6_rect)  # Gala
    pygame.draw.rect(surface, (255, 165, 0), button7_rect)  # Dégradé (orange)

    labels = ["Rouge", "Vert", "Bleu", "Neige", "BDF", "Gala", "Dégradé"]
    buttons = [button1_rect, button2_rect, button3_rect, button4_rect, button5_rect, button6_rect, button7_rect]

    for i, button in enumerate(buttons):
        text = font.render(labels[i], True, (255, 255, 255))
        surface.blit(text, (button.x + 10, button.y + 10))

# Police pour le texte
font = pygame.font.SysFont("Arial", 24)

# --- Modes ---
mode = "normal"
current_color = (255, 255, 255)

trance = 0

# --- Boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if button1_rect.collidepoint(mouse_pos):  # Rouge
                current_color = (255, 0, 0)
                mode = "normal"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color

            elif button2_rect.collidepoint(mouse_pos):  # Vert
                current_color = (0, 255, 0)
                mode = "normal"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color

            elif button3_rect.collidepoint(mouse_pos):  # Bleu
                current_color = (0, 0, 255)
                mode = "normal"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = current_color

            elif button4_rect.collidepoint(mouse_pos):  # Neige
                mode = "neige"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)

            elif button5_rect.collidepoint(mouse_pos):  # Logo BDF
                mode = "affichage_bdf"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)

            elif button6_rect.collidepoint(mouse_pos):  # Logo Gala
                mode = "affichage_gala"
                for y in range(matrix_height):
                    for x in range(matrix_width):
                        led_matrix[y][x] = (0, 0, 0)

            elif button7_rect.collidepoint(mouse_pos):  # Dégradé
                mode = "degrade"
                generate_initial_gradient()  # Génère une seule fois le dégradé de base

    # Mise à jour en fonction du mode
    if mode == "normal":
        update_matrix()
    elif mode == "neige":
        pygame.time.wait(40)
        update_neige()
    elif mode == "degrade":
        animate_gradient()



    update_led_surface()

    # Affichage
    screen.fill((30, 30, 30))

    trance += 1
    if trance > 2 and strobe_activate == True:
        # Todo : Affiche un écran blanc
        screen.fill((0, 0, 0))
        if trance > 4:
            trance = 0
    else:
        screen.blit(pygame.transform.rotate(led_surface, 90), (65, 60))
    
    screen.blit(pygame.transform.scale(led_surface, (matrix_width * 10, matrix_height * 10)), (300, 50))
    draw_buttons(screen, font)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
