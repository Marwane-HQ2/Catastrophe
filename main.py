import pygame, sys
from pygame.locals import *
from random import randint

def play():
    # ----------------------------- PARAMETRAGES DU JEU -----------------------------

    pygame.init()
    
    FPS = 60
    FramePerSec = pygame.time.Clock()
    
    # COULEURS PREDEFINIES
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    BNW = False # VERSION NOIR ET BLANC

    # TEXTE 
    police_titre = pygame.font.Font("DeliciousHandrawn-Regular.ttf", 45) # CREER UNE POLICE
    police_principale = pygame.font.Font("DeliciousHandrawn-Regular.ttf", 35) # CREER UNE POLICE

    # INFOS ECRAN
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 600

    DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # SURFACE DE JEU
    DISPLAYSURFACE.fill(WHITE)
    pygame.display.set_caption("Catastrophe")


    # ----------------------------- CLASSES -----------------------------
    class Chat(pygame.sprite.Sprite) :
        def __init__(self):
            super().__init__()

            # CHARGEMENT DE L'IMAGE
            self.image = pygame.image.load("cat_idle.png")
            # REDIMENSION DE L'IMAGE
            self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))
            self.rect = self.image.get_rect()

            self.rect.center = (SCREEN_WIDTH//2 - 5, 60) # SPAWN POINT - ICI AU MILIEU DE L'ECRAN
            
            self.gauche = (150, SCREEN_HEIGHT - 20)
            self.droite = (350, SCREEN_HEIGHT - 20)

            self.flag = None

            self.flag_gauche = (360, 35)
            self.flag_droite = (130, 35)

        def afficher(self, surface):
            """
            Affiche l'élément sur la surface donnée en paramètre
            pre: surface (SURFACE)
            post:
            """
            surface.blit(self.image, self.rect)
            if self.flag != None:
                self.flag.afficher(surface)
        
        def jeter_objets(self, images, groupe_objets, v):
            
            self.image = pygame.image.load("cat_throwing.png")
            # REDIMENSION DE L'IMAGE
            self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH//2 - 5, 60)

            nouvel_objet = Objets(images[randint(0, len(images) - 1)])
            nouvel_objet.definir_vitesse(v)

            # OU LEVER LE DRAPEAU ?
            if nouvel_objet.rect.center == nouvel_objet.gauche:
                self.flag = Flag(self.flag_droite, True)
            elif nouvel_objet.rect.center == nouvel_objet.droite:
                self.flag = Flag(self.flag_gauche, False)
            
            groupe_objets.add(nouvel_objet) # CREATION DE L'OBJET
            all_sprites.add(nouvel_objet)

    class Flag(pygame.sprite.Sprite):
        def __init__(self, position, reverse):
            super().__init__()

            self.image = pygame.image.load("flag.png")
            self.rect = self.image.get_rect()
            self.rect.center = position

            self.image = pygame.transform.flip(self.image, reverse, False) # RETOURNER HORIZONTALEMENT
        
        def afficher(self, surface):
            surface.blit(self.image, self.rect)


    class Objets(pygame.sprite.Sprite):
        def __init__(self, img):
            super().__init__()

            # CHARGEMENT DE L'IMAGE
            self.image = pygame.image.load(img)
            self.rect = self.image.get_rect()

            # DEPLACEMENTS ET POSITIONS
            self.gauche = (150, 100)
            self.droite = (350, 100)

            self.rect.center =  [self.gauche, self.droite][randint(0, 1)]

            self.delta_y = 5  
            self.delta_x = 0
            self.vitesse = 1

        
        def afficher(self, surface):
            """
            Affiche l'élément sur la surface donnée en paramètre
            pre: surface (SURFACE)
            post:
            """
            surface.blit(self.image, self.rect) 
        
        def deplacer(self):
            """
            Permet le deplacement de l'objet
            """
            if self.rect.bottom < SCREEN_HEIGHT: # SI LE LUTIN EST DANS L'ECRAN 
                self.rect.move_ip(0, self.delta_y * self.vitesse) # LE LUTIN TOMBE
            else: 
                self.kill() # SI LE LUTIN SORT DE L'ECRAN LE LUTIN EST DETRUIT
                game_over() # LE JOUEUR A PERDU

        def definir_vitesse(self, v):
            self.vitesse = v

    class Boite(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()

            # CHARGEMENT DE L'IMAGE
            self.image = pygame.image.load("box.png")
            self.rect = self.image.get_rect()

            # DEPLACEMENTS ET POSITIONS
            self.gauche = (150, SCREEN_HEIGHT - 100)
            self.droite = (350, SCREEN_HEIGHT - 100)

            self.rect.center = [self.gauche, self.droite][randint(0, 1)]  # SPAWN POINT

            # SCORE
            self.score = 0

            # 
            self.joue = True

        def afficher(self, surface):
            """
            Affiche l'élément sur la surface donnée en paramètre
            pre: surface (SURFACE)
            post:
            """
            surface.blit(self.image, self.rect) 
        
        def deplacer(self):
            """
            Permet le deplacement de la boite
            """
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                if self.rect.center == self.droite: # SI LA BOITE EST A GAUCHE
                    self.rect.center = self.gauche

            if pressed_keys[K_RIGHT]:
                if self.rect.center == self.gauche:
                    self.rect.center = self.droite

        def augmenter_score(self):
            self.score += 1
        
        def est_en_etat(self):
            return self.joue
                        


    # ----------------------------- VARIABLES -----------------------------
    # ------- LUTINS ET ASSETS -------
    CHAT = Chat()
    BOITE = Boite()

    OBJETS = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group() # GROUPE UTILISE POUR AFFICHER
    all_sprites.add(CHAT)
    all_sprites.add(BOITE)

    # ------- TEMPS -------
    horloge_globale = pygame.time.get_ticks()
    horloge_globale_delais = pygame.time.get_ticks()
    horloge_globale_vitesse = pygame.time.get_ticks()

    cooldown = 500
    vitesse = 1
    # ----------------------------- FONCTIONS -----------------------------

    # COLLISIONS
    def attraper_objet(boite, grp_obj):
        objet_touche = pygame.sprite.spritecollideany(boite, grp_obj)
        if objet_touche != None:
            objet_touche.kill()
            boite.augmenter_score()


    # ------- TEXTE -------
    def afficher_score(surface, score):
        texte_score = police_principale.render(f"Saved furnitures: {score}", True, BLACK)
        surface.blit(texte_score, (55, 550))

    def texte_game_over(surface, score):
        surface.fill(WHITE)
        text = police_titre.render("- GAME OVER -", True, BLACK)
        surface.blit(text, (120, 100))
        text = police_principale.render(f"Your score was {score}", True, BLACK)
        surface.blit(text, (145, 265))
        text = police_principale.render("Press space to play again", True, BLACK)
        surface.blit(text, (95, 420))

    # JEU 
    def game_over():
        BOITE.joue = False

        BOITE.kill()
        CHAT.kill()
        for lutin in OBJETS:
            lutin.kill()
        for lutin in all_sprites:
            lutin.kill()
        
        DISPLAYSURFACE.fill(WHITE)

    def ecoute_rejouer():
        touches = pygame.key.get_pressed()
        if touches[K_SPACE]:
            play()

    # ----------------------------- BOUCLE DU JEU -----------------------------
    while True:
        # OBTENIR L'HEURE QU'IL EST A CHAQUE ITERATION
        heure = pygame.time.get_ticks()

        # ----------------- QUITTER JEU -----------------
        
        # SI APPUI SUR LA CROIX
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        # QUITTE LE JEU SI APPUI SUR ESC
        if pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # ----------------- JEU -----------------

        # SI LA BOITE EST ENCORE EN ETAT DE CONTINUER
        if BOITE.est_en_etat():
            # DEPLACEMENT
            # TOUJOURS PERMETTRE LE DEPLACEMENT DE LA BOITE ET DES OBJETS
            BOITE.deplacer()

            for objet in OBJETS:
                objet.deplacer()

            # JETER LES OBJETS
            if heure - horloge_globale_delais > cooldown:
                CHAT.jeter_objets(["livre.png", "vase.png"], OBJETS, vitesse)
                horloge_globale_delais = heure
            
            if heure - horloge_globale_vitesse > 2500: # TOUTES LES 2.5 SECONDES
                if vitesse <= 4.5:
                    vitesse += 0.25
                if cooldown >= 100:
                    cooldown -= 40
                horloge_globale_vitesse = heure

            # ATTRAPER LES OBJETS
            attraper_objet(BOITE, OBJETS) 

        # ----------------- AFFICHAGE -----------------

        # REPEINDRE L'ECRAN
        if BOITE.score > 60: DISPLAYSURFACE.fill((255, 172, 124))
        elif BOITE.score > 30: DISPLAYSURFACE.fill((255, 206, 142))
        elif BOITE.score > 15: DISPLAYSURFACE.fill((255, 238, 184))
        else: DISPLAYSURFACE.fill(WHITE)

        # AFFICHER CHAQUE ELEMENT
        for lutin in all_sprites:
            lutin.afficher(DISPLAYSURFACE)

        if BOITE.est_en_etat():
            afficher_score(DISPLAYSURFACE, BOITE.score)
        else: 
            texte_game_over(DISPLAYSURFACE, BOITE.score)
            ecoute_rejouer()

        # REAFFICHER L'ECRAN
        pygame.display.update()
        FramePerSec.tick(FPS)

play()