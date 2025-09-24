import os
import sys
import time
import tty
import termios
import random

# Paramètres du plateau
grille_largeur = 13
grille_hauteur = 11

# Caractères ASCII
VIDE = ' '
MUR = '#'
MUR_DESTRUCTIBLE = '%'
JOUEUR = 'P'
BOMBE = 'B'
EXPLOSION = '*'

# Plateau de jeu (murs sur le contour et murs destructibles)
grille = [[VIDE for _ in range(grille_largeur)] for _ in range(grille_hauteur)]
for y in range(grille_hauteur):
    for x in range(grille_largeur):
        if x == 0 or x == grille_largeur-1 or y == 0 or y == grille_hauteur-1:
            grille[y][x] = MUR
        elif (x, y) != (1, 1) and random.random() < 0.2:
            grille[y][x] = MUR_DESTRUCTIBLE

# Position initiale du joueur
joueur_x, joueur_y = 1, 1
grille[joueur_y][joueur_x] = JOUEUR

# Balle (une seule à la fois pour simplifier)
balle = None  # (x, y, temps_pose)

def afficher_grille():
    os.system('clear')
    for ligne in grille:
        print(''.join(ligne))
    print("Utilisez ZQSD pour bouger, Espace pour poser une balle, X pour quitter.")

def deplacer_joueur(dx, dy):
    global joueur_x, joueur_y
    nx, ny = joueur_x + dx, joueur_y + dy
    if grille[ny][nx] == VIDE:
        grille[joueur_y][joueur_x] = VIDE
        joueur_x, joueur_y = nx, ny
        grille[joueur_y][joueur_x] = JOUEUR

def lire_touche():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def detruire_autour(x, y):
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < grille_largeur and 0 <= ny < grille_hauteur:
            if grille[ny][nx] == MUR_DESTRUCTIBLE:
                grille[ny][nx] = EXPLOSION

def main():
    global balle
    afficher_grille()
    derniere_explosion = None
    while True:
        # Gestion du timer de la balle
        maintenant = time.time()
        if balle:
            bx, by, t_pose = balle
            # Balle explose après 2 secondes
            if maintenant - t_pose >= 2:
                grille[by][bx] = EXPLOSION
                detruire_autour(bx, by)
                derniere_explosion = (bx, by, maintenant)
                balle = None
                afficher_grille()
        # Efface l'explosion après 0.5s
        if derniere_explosion:
            bx, by, t_expl = derniere_explosion
            if maintenant - t_expl >= 0.5:
                # Efface explosion centrale et autour
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]:
                    nx, ny = bx+dx, by+dy
                    if 0 <= nx < grille_largeur and 0 <= ny < grille_hauteur:
                        if grille[ny][nx] == EXPLOSION:
                            grille[ny][nx] = VIDE
                derniere_explosion = None
                afficher_grille()

        touche = lire_touche().lower()
        rafraichir = False
        if touche == 'z':
            deplacer_joueur(0, -1)
            rafraichir = True
        elif touche == 's':
            deplacer_joueur(0, 1)
            rafraichir = True
        elif touche == 'q':
            deplacer_joueur(-1, 0)
            rafraichir = True
        elif touche == 'd':
            deplacer_joueur(1, 0)
            rafraichir = True
        elif touche == ' ':  # Espace pour poser une balle
            if not balle:
                # Pose la balle à la position du joueur
                balle = (joueur_x, joueur_y, time.time())
                grille[joueur_y][joueur_x] = BOMBE
                rafraichir = True
        elif touche == 'x':
            print("Fin du jeu.")
            break
        if rafraichir:
            afficher_grille()

if __name__ == "__main__":
    main()
