from models.joueur import Joueur
from models.tournoi import Tournoi
from tinydb import TinyDB, Query, where
from controllers.controller import Controller
import datetime


class View:


    # Vues Menu
    def show_menu(self):
        print("Joueurs..........................entrez 1 : ")
        print("Tournois.........................entrez 2 : ")
        print("Rapports.........................entrez 3 : ")
        print("Quitter..........................entrez Q : ")
        choix = input("Entrez Votre Choix : ")
        return choix

    def show_menu_joueurs(self):
        print("Créer Joueurs....................entrez 1 : ")
        print("Modifier Classement..............entrez 2 : ")
        print("Afficher Joueurs.................entrez 3 : ")
        print("Revenir Menu Principal...........entrez 4 : ")
        print("Quitter..........................entrez Q : ")
        choix = input("Entrez Votre Choix : ")
        return choix

    def show_menu_tournois(self):
        print("Créer Tournois...................entrez 1 : ")
        print("Afficher Liste Tournois..........entrez 2 : ")
        print("Saisir Resultats.................entrez 3 : ")
        print("Revenir Menu Principal...........entrez 4 : ")
        print("Quitter..........................entrez Q : ")
        choix = input("Entrez Votre Choix : ")
        return choix

    def show_menu_rapports(self):
        print("Joueurs par Ordre Alphabetique.....................entrez 1 : ")
        print("Joueurs par Classement.............................entrez 2 : ")
        print("Joueurs d'un Tournoi par Ordre Alphabetique........entrez 3 : ")
        print("Joueurs d'un Tournoi par Classement................entrez 4 : ")
        print("Liste de Tous les Tournois.........................entrez 5 : ")
        print("Liste des Tours d'un Tournoi.......................entrez 6 : ")
        print("Liste des Matchs d'un Tournoi......................entrez 7 : ")
        print("Revenir Menu Principal.............................entrez 8 : ")
        print("Quitter............................................entrez Q : ")
        choix = input("Entrez Votre Choix : ")
        return choix

    def prompt_joueur(self):
        nom_joueur = input("Entrez le Nom du Joueur : ")
        prenom_joueur = input("Entrez le Prenom du Joueur : ")
        date_de_naissance = input("Entrez la Date de Naissance du Joueur : ")
        sexe = input("Entrez le Sexe du Joueur : ")
        classement = input("Entrer le Classement ELO du Joueur : ")
        joueur_info = [nom_joueur, prenom_joueur, date_de_naissance, sexe, classement]
        return joueur_info

    def prompt_get_id(self):
        joueur_id = input("Entrez l'identifiant du joueur que vous souhaitez modifier : ")
        return joueur_id

    def prompt_get_nouveau_classement(self):
        nouveau_classement = input("Entrez le nouveau classement du joueur : ")
        return nouveau_classement

    def prompt_tournoi(self):
        nom_tournoi = input("Entrez le nom du tournoi : ")
        lieu_du_tournoi = input("Entrez le lieu du tournoi : ")
        date_debut = input("Entrez la date du debut du tournoi : ")
        date_fin = input("Entrez la date de fin du tournoi : ")
        nombre_de_tours = 4
        controle_du_temps = input("Entrez le controle du temps : ")
        description_tournoi = input("Entrez une description pour le tournoi : ")
        tournoi = [nom_tournoi, lieu_du_tournoi, date_debut, date_fin, nombre_de_tours,
                   controle_du_temps, description_tournoi
                   ]
        return tournoi

    def prompt_joueur_tournoi(self, i):
        indice = input("Veuillez entrer l'indice du joueur " + str(i) + " : ")
        return indice

    def prompt_resultat_match(self, joueur_blanc, joueur_noir):
        resultat = input(f"Si {joueur_blanc.prenom} {joueur_blanc.nom} est le gagnant entrez 1 \n"
                         f"Si {joueur_noir.prenom} {joueur_noir.nom} est le gagnant entrez 2 \n"
                         f"Si Match est Nul entrez x \n"
                         f"Entrez le resultat : ")
        return resultat

    def prompt_choisir_tournoi(self):
        indice_tournoi = input("Entrez l'indice du tournoi : ")
        return indice_tournoi

    def prompt_choisir_tour(self):
        num_tour = input("Entrez l'indice du tour : ")
        return num_tour

    def prompt_alerte_joueurs(self):
        print("pas assez de joueurs pour creer un tournoi")

    def prompt_alerte_saisie_tour(self):
        print("Vous ne pouvez Entrer de Resultats Que Pour Le Dernier Tour En Cours")

    def prompt_modification_succes(self):
        print("Changement effectué avec succès")

    def affichage_generique(self, data):
        print(data)