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

# Liste des balles actives : chaque balle = (x, y, temps_pose)
balles = []
# Liste des explosions à effacer : chaque explosion = (x, y, temps_explosion)
explosions = []
# Liste des ennemis : chaque ennemi = (x, y)
ennemis = []

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
            elif grille[ny][nx] == BOMBE:
                # Explosion en chaîne
                for i, (bx, by, t) in enumerate(balles):
                    if bx == nx and by == ny:
                        balles.pop(i)
                        grille[ny][nx] = EXPLOSION
                        explosions.append((nx, ny, time.time()))
                        detruire_autour(nx, ny)
                        break

# Placement aléatoire des ennemis
def placer_ennemis(nb=2):
    global ennemis
    libres = [(x, y) for y in range(1, grille_hauteur-1) for x in range(1, grille_largeur-1)
              if grille[y][x] == VIDE and (x, y) != (joueur_x, joueur_y)]
    ennemis = random.sample(libres, min(nb, len(libres)))
    for ex, ey in ennemis:
        grille[ey][ex] = 'E'

# Déplacement aléatoire des ennemis
def deplacer_ennemis():
    global ennemis
    nouveaux = []
    for ex, ey in ennemis:
        grille[ey][ex] = VIDE
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = ex+dx, ey+dy
            if 0 <= nx < grille_largeur and 0 <= ny < grille_hauteur and grille[ny][nx] == VIDE:
                nouveaux.append((nx, ny))
                break
        else:
            nouveaux.append((ex, ey))
    ennemis = nouveaux
    for ex, ey in ennemis:
        grille[ey][ex] = 'E'

def main():
    global balles, joueur_x, joueur_y, ennemis
    placer_ennemis(2)
    afficher_grille()
    joueur_vivant = True
    while joueur_vivant:
        maintenant = time.time()
        # Gestion des explosions de balles
        nouvelles_explosions = []
        nouvelles_balles = []
        for bx, by, t_pose in balles:
            if maintenant - t_pose >= 2:
                grille[by][bx] = EXPLOSION
                detruire_autour(bx, by)
                explosions.append((bx, by, maintenant))
            else:
                nouvelles_balles.append((bx, by, t_pose))
        balles = nouvelles_balles
        # Efface les explosions après 0.5s
        nouvelles_explosions = []
        for ex, ey, t_expl in explosions:
            if maintenant - t_expl >= 0.5:
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]:
                    nx, ny = ex+dx, ey+dy
                    if 0 <= nx < grille_largeur and 0 <= ny < grille_hauteur:
                        if grille[ny][nx] == EXPLOSION:
                            grille[ny][nx] = VIDE
            else:
                nouvelles_explosions.append((ex, ey, t_expl))
        explosions[:] = nouvelles_explosions

        # Déplacement des ennemis
        deplacer_ennemis()
        # Si un ennemi touche le joueur
        if any((ex == joueur_x and ey == joueur_y) for ex, ey in ennemis):
            afficher_grille()
            print("Vous avez perdu ! Un ennemi vous a touché.")
            joueur_vivant = False
            break
        # Si un ennemi est sur une explosion, il meurt
        ennemis = [(ex, ey) for ex, ey in ennemis if grille[ey][ex] != EXPLOSION]

        # Vérifie si le joueur est sur une explosion
        if grille[joueur_y][joueur_x] == EXPLOSION:
            afficher_grille()
            print("Vous avez perdu ! Le joueur a été touché par une explosion.")
            joueur_vivant = False
            break

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
            if not any((bx == joueur_x and by == joueur_y) for bx, by, _ in balles):
                balles.append((joueur_x, joueur_y, time.time()))
                grille[joueur_y][joueur_x] = BOMBE
                rafraichir = True
        elif touche == 'x':
            print("Fin du jeu.")
            break
        if rafraichir:
            afficher_grille()

if __name__ == "__main__":
    main()
