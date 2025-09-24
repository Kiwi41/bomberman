import os
import sys
import time
import tty
import termios

# Paramètres du plateau

        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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
                derniere_explosion = (bx, by, maintenant)
                balle = None
                afficher_grille()
        # Efface l'explosion après 0.5s
        if derniere_explosion:
            bx, by, t_expl = derniere_explosion
            if maintenant - t_expl >= 0.5:
                if grille[by][bx] == EXPLOSION:
                    grille[by][bx] = VIDE
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
    return ch

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
                derniere_explosion = (bx, by, maintenant)
                balle = None
                afficher_grille()
        # Efface l'explosion après 0.5s
        if derniere_explosion:
            bx, by, t_expl = derniere_explosion
            if maintenant - t_expl >= 0.5:
                if grille[by][bx] == EXPLOSION:
                    grille[by][bx] = VIDE
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
