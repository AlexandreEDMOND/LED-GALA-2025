import pygame
import sys
import random
import math
import colorsys
import pygame_gui
 
from pygame_gui.windows import UIColourPickerDialog

# Initialisation de Pygame
pygame.init()

# --- Création de la fenêtre en plein écran ---
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("LED Matrix – Boutons et Effets")

clock = pygame.time.Clock()

""" # --- Définition de la matrice LED --- REGLAGEs ALEXT
matrix_width = 104  # Colonnes
matrix_height = 26  # Lignes

# Position de la matrice LED Output sur l'écran 
offset_x = 65
offset_y = 60 """

# --- Définition de la matrice LED --- REGLAGES THIBAUT
matrix_width = 128  # Colonnes # Réglage Alext
matrix_height = 32  # Lignes

# Position de la matrice LED Output sur l'écran 
offset_x = 80 #réglage Thib
offset_y = 80

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

def choose_color():
    colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
    ui_manager,
    window_title="Change Colour...",
    initial_colour=picker_color)
    return colour_picker

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
strobe_activate = False

# --- Slider ---
slider_x, slider_y = 50 + 10 * (button_width + button_gap), base_y - 30
slider_width, slider_height = 150, 10
slider_pos = slider_x
min_value, max_value = 0, 100
strobe_value = min_value
dragging = False

# --- GUI pour le color picker ---
colour_picker = None
ui_manager = pygame_gui.UIManager((1920, 1080))
    
button0_rect = pygame.Rect(50, base_y, button_width, button_height)  # Color picker
button1_rect = pygame.Rect(50 + (button_width + button_gap), base_y, button_width, button_height)  # Rouge
button2_rect = pygame.Rect(50 + 2* (button_width + button_gap), base_y, button_width, button_height)  # Vert
button3_rect = pygame.Rect(50 + 3 * (button_width + button_gap), base_y, button_width, button_height)  # Bleu
button4_rect = pygame.Rect(50 + 4 * (button_width + button_gap), base_y, button_width, button_height)  # Neige
button5_rect = pygame.Rect(50 + 5 * (button_width + button_gap), base_y, button_width, button_height)  # BDF
button6_rect = pygame.Rect(50 + 6 * (button_width + button_gap), base_y, button_width, button_height)  # Gala
button7_rect = pygame.Rect(50 + 7 * (button_width + button_gap), base_y, button_width, button_height)  # Dégradé

buttonfx_rect = pygame.Rect(50 + 10 * (button_width + button_gap), base_y, button_width, button_height)  # Strobe

def draw_elements(surface, font):
    """Affichage des boutons avec texte."""
    pygame.draw.rect(surface, (0, 0, 0), button0_rect)  # Color picker
    pygame.draw.rect(surface, (200, 0, 0), button1_rect)  # Rouge
    pygame.draw.rect(surface, (0, 200, 0), button2_rect)  # Vert
    pygame.draw.rect(surface, (0, 0, 200), button3_rect)  # Bleu
    pygame.draw.rect(surface, (120, 120, 120), button4_rect)  # Neige
    pygame.draw.rect(surface, (120, 120, 120), button5_rect)  # BDF
    pygame.draw.rect(surface, (120, 120, 120), button6_rect)  # Gala
    pygame.draw.rect(surface, (255, 165, 0), button7_rect)  # Dégradé (orange)
    pygame.draw.rect(surface, (255, 255, 255), buttonfx_rect)  # Strobe (blanc)

    # Draw slider line
    pygame.draw.rect(screen, (0, 0, 0), (slider_x, slider_y, slider_width, slider_height)) 
    # Draw slider knob
    pygame.draw.rect(screen, (255, 255, 255), (slider_pos, slider_y - slider_height // 2, slider_height , slider_height*2))

    if current_color >= (200, 200, 200):
        label_color_picker = (255,255,255)
    else:
        label_color_picker = (0,0,0)
    labels = ["Couleur","Rouge", "Vert", "Bleu", "Neige", "BDF", "Gala", "Dégradé", "Strobe"]
    buttons = [button0_rect,button1_rect, button2_rect, button3_rect, button4_rect, button5_rect, button6_rect, button7_rect,buttonfx_rect]
    colors = [label_color_picker, (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),(255, 255, 255), (255, 255, 255), (0, 0, 0)]

    for i, button in enumerate(buttons):
        text = font.render(labels[i], True, colors[i])
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

            if button0_rect.collidepoint(mouse_pos):  # color picker
                picker_color = pygame.Color(0, 0, 0) #Couleur par défaut du color picker
                picker_color = choose_color()
                mode = "color_picker"

            elif button1_rect.collidepoint(mouse_pos):  # Rouge
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

            elif buttonfx_rect.collidepoint(mouse_pos):  # Strobe
                strobe_activate = False if strobe_activate == True else True

            if (slider_x <= mouse_pos[0] <= slider_x + slider_width) and (slider_y - slider_height/4 <= mouse_pos[1] <= slider_y + slider_height+ slider_height/4) :
                dragging = True
                slider_pos = max(slider_x, min(mouse_pos[0], slider_x + slider_width))  # Constrain position within bounds
                strobe_value = int((slider_pos - slider_x) / slider_width * (max_value - min_value))

        if event.type == pygame.MOUSEBUTTONUP: #Condition poour pouvoir arreter le slider
                dragging = False

        if event.type == pygame.MOUSEMOTION and dragging: #Condition poour pouvoir bouger le slider et rester appuyer
            mouse_pos = pygame.mouse.get_pos()
            slider_pos = max(slider_x, min(mouse_pos[0], slider_x + slider_width))  # Constrain position within bounds
            strobe_value = int((slider_pos - slider_x) / slider_width * (max_value - min_value))

        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            picker_color = event.colour
            for y in range(matrix_height):
                for x in range(matrix_width):
                    led_matrix[y][x] = picker_color
        
        ui_manager.process_events(event)

    ui_manager.update(0.01)

    # Mise à jour en fonction du mode
    if mode == "normal":
        update_matrix()
    elif mode == "neige":
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
    elif mode == "color_picker":
        pass
    elif mode == "degrade":
        animate_gradient()

    update_led_surface()

    # Affichage
    screen.fill((30, 30, 30))

    trance += 1
    strobe_freq = (100-strobe_value)/100*5 + 3 #fréquence de clignotement
    if trance > strobe_freq/2 and strobe_activate == True:
        # Todo : Affiche un écran blanc
        screen.fill((0, 0, 0))
        if trance > strobe_freq:
            trance = 0
    else:
        screen.blit(pygame.transform.rotate(led_surface, 90), (offset_x, offset_y))
    
    screen.blit(pygame.transform.scale(led_surface, (matrix_width * 10, matrix_height * 10)), (300, 50))
    draw_elements(screen, font)
    ui_manager.draw_ui(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
