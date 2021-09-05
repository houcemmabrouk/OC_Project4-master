from datetime import datetime
from tinydb import TinyDB, Query
from typing import List
from models.joueur import Joueur
from models.tournoi import Tournoi
from models.match import Match
from models.tour import Tour


class Controller:




    def __init__(self, view):
        self.view = view
        self.joueurs: List[Joueur] = []
        self.matchs_tour: List[Match] = []
        self.tours_tournoi: List[Tour] = []
        self.ranked_joueurs: List[Joueur] = []
        self.tours: List[Match] = []
        db = TinyDB('db.json')
        self.table_joueurs = db.table("joueurs")
        self.table_tournois = db.table("tournois")




    def nombre_de_joueurs_db(self):
        nb_joueurs = 0
        for joueur in self.table_joueurs:
            if joueur.doc_id != None:
                nb_joueurs += 1
        return nb_joueurs

    def set_joueur(self):

        joueur_info = self.view.prompt_joueur()
        joueur = Joueur(joueur_info[0], joueur_info[1], joueur_info[2],
                        joueur_info[3], joueur_info[4], 0)
        serialized_joueur = {
            'nom': joueur.nom.upper(),
            'prenom': joueur.prenom.capitalize(),
            'date_de_naissance': joueur.date_de_naissance,
            'sexe': joueur.sexe,
            'classement': joueur.classement,
            'score_tournoi': joueur.score_tournoi
        }
        self.table_joueurs.insert(serialized_joueur)
        return joueur

    def get_joueurs_ids(self, joueurs):
        joueurs_ids = []
        for joueur in joueurs:
            joueur_id = self.get_joueur_id(joueur)
            joueurs_ids.append(joueur_id)
        return joueurs_ids

    def serialize_joueur(self, joueur):
        serialized_joueur = {
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_de_naissance': joueur.date_de_naissance,
            'sexe': joueur.sexe,
            'classement': joueur.classement,
            'score_tournoi': joueur.score_tournoi
        }
        return serialized_joueur

    def deserialize_joueur(self, serialized_joueur):
        joueur = Joueur(
            nom=serialized_joueur['nom'],
            prenom=serialized_joueur['prenom'],
            date_de_naissance=serialized_joueur['date_de_naissance'],
            sexe=serialized_joueur['sexe'],
            classement=serialized_joueur['classement'],
            score_tournoi=serialized_joueur['score_tournoi']
        )
        return joueur

    def serialize_match(self, match):
        joueur_blanc_id = self.get_joueur_id(match.resultat[0][0])
        score_blanc = match.resultat[0][1]
        joueur_noir_id = self.get_joueur_id(match.resultat[1][0])
        score_noir = match.resultat[1][1]
        match_resultat = ([joueur_blanc_id, score_blanc], [joueur_noir_id, score_noir])
        serialized_match = {'resultat': match_resultat}
        return serialized_match

    def deserialize_match(self, serialized_match):
        joueur_blanc = self.get_joueur(serialized_match[0][0])
        score_blanc = serialized_match[0][1]
        joueur_noir = self.get_joueur(serialized_match[1][0])
        score_noir = serialized_match[1][1]
        resultat_match = ([joueur_blanc, score_blanc], [joueur_noir, score_noir])
        match = Match(resultat=resultat_match)
        return match

    def serialize_tour(self, tour):
        tour_matchs = []
        for match in tour.tour_matchs:
            tour_match = self.serialize_match(match)
            tour_matchs.append(tour_match)

        serialized_tour = {'num_tour': tour.num_tour,
                           'nom_tour': tour.nom_tour,
                           'date_debut': tour.date_debut,
                           'date_fin': tour.date_fin,
                           'tour_matchs': tour_matchs,
                           'flag': tour.flag,
                           'id_tournoi': tour.id_tournoi,
                           }
        return serialized_tour

    def deserialize_tour(self, serialized_tour):
        tour_matchs = []
        for match in serialized_tour['tour_matchs']:
            deserialized_match = self.deserialize_match(match)
            tour_matchs.append(deserialized_match)

        tour = Tour(
            num_tour=serialized_tour['num_tour'],
            nom_tour=serialized_tour['nom'],
            date_debut=serialized_tour['date_debut'],
            date_fin=serialized_tour['date_fin'],
            tour_matchs=serialized_tour['tour_matchs'],
            flag=serialized_tour['flag'],
            id_tournoi=serialized_tour['id_tournoi']
        )
        return tour

    def serialize_tournoi(self, tournoi):
        serialized_tours = []
        for tour in tournoi.tours:
            serialized_tour = self.serialize_tour(tour)
            serialized_tours.append(serialized_tour)

        serialized_tournoi = {
            'nom_tournoi': tournoi.nom_tournoi,
            'lieu': tournoi.lieu,
            'date_debut': tournoi.date_debut,
            'date_fin': tournoi.date_fin,
            'nombre_tours': tournoi.nombre_tours,
            'joueurs': self.get_joueurs_ids(tournoi.joueurs),
            'controle_du_temps': tournoi.controle_du_temps,
            'description': tournoi.description,
            'tours': serialized_tours,
            'flag': tournoi.flag
        }
        return serialized_tournoi

    def deserialize_tournoi(self, serialized_tournoi):
        tournoi = Tournoi(
            nom_tournoi=serialized_tournoi['nom_tournoi'],
            lieu=serialized_tournoi['lieu'],
            date_debut=serialized_tournoi['date_debut'],
            date_fin=serialized_tournoi['date_fin'],
            nombre_tours=serialized_tournoi['nombre_tours'],
            joueurs=serialized_tournoi['joueurs'],
            controle_du_temps=serialized_tournoi['controle_du_temps'],
            description=serialized_tournoi['description'],
            tours=serialized_tournoi['tours'],
            flag=serialized_tournoi['flag']
        )
        return tournoi

    def get_joueur_id(self, joueur):
        User = Query()
        serialized_joueur = self.serialize_joueur(joueur)
        documents = self.table_joueurs.search(User.nom == str(serialized_joueur['nom']))
        id_joueur = None
        for document in documents:
            id_joueur = document.doc_id
        return id_joueur

    def get_joueurs(self, ids_joueurs):
        joueurs = []
        for id_joueur in ids_joueurs:
            for joueur in self.table_joueurs:
                if str(id_joueur) == str(joueur.doc_id):
                    joueur = Joueur(
                        joueur['nom'],
                        joueur['prenom'],
                        joueur['date_de_naissance'],
                        joueur['sexe'],
                        joueur['classement'],
                        joueur['score_tournoi']
                    )
                    joueurs.append(joueur)
        return joueurs

    def get_joueur(self, id_joueur):
        for joueur_in_table in self.table_joueurs:
            if str(id_joueur) == str(joueur_in_table.doc_id):
                joueur = Joueur(
                    joueur_in_table['nom'],
                    joueur_in_table['prenom'],
                    joueur_in_table['date_de_naissance'],
                    joueur_in_table['sexe'],
                    joueur_in_table['classement'],
                    joueur_in_table['score_tournoi']
                )

        return joueur

    def afficher_joueurs(self, joueurs_tournoi):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        User = Query()
        for joueur in table_joueurs:
            if str(joueur.doc_id) not in joueurs_tournoi:
                results = str(joueur.doc_id) + " : " + joueur["prenom"].capitalize() + " " + \
                          joueur["nom"].upper() + " (" + joueur["classement"] + ")"
                self.view.affichage_generique(results)

    def update_joueur_classement(self):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        self.afficher_joueurs([])
        joueur_id = self.view.prompt_get_id()
        nouveau_classement = self.view.prompt_get_nouveau_classement()

        for joueur in table_joueurs:
            if str(joueur.doc_id) == joueur_id:
                table_joueurs.update({"classement": nouveau_classement}, doc_ids=[joueur.doc_id])
                self.view.prompt_modification_succes()

    def creer_tournoi(self):
        if self.nombre_de_joueurs_db() >= 8:
            tournoi_info = self.view.prompt_tournoi()
            joueurs_tournoi = []
            i = 1
            while i < 9:
                self.afficher_joueurs(joueurs_tournoi)
                id_joueur = self.view.prompt_joueur_tournoi(i)
                if self.verifier_indice(id_joueur) == True and id_joueur not in joueurs_tournoi:
                    i += 1
                    joueur = self.get_joueur(id_joueur)
                    self.joueurs.append(joueur)
                    joueurs_tournoi.append(id_joueur)

            ''' Creation du premier tour'''
            tournoi_tours = []
            premier_tour = Tour("1", "Tour 1", None, None, [], "En Cours", None)
            tournoi_tours.append(premier_tour)
            '''Creation de l'objet tournoi'''
            tournoi = Tournoi(tournoi_info[0], tournoi_info[1], tournoi_info[2], tournoi_info[3],
                              tournoi_info[4], tournoi_info[5], tournoi_info[6],
                              self.joueurs, tournoi_tours, flag="En Cours"
                              )
            '''Serialisation et sauvegarde du tournoi dans la base de donnée'''
            serialized_tournoi = self.serialize_tournoi(tournoi)
            self.table_tournois.insert(serialized_tournoi)
        else:
            self.view.prompt_alerte_joueurs()
            self.afficher_sous_menu("1")

    def translate_resultat(self, entry):
        score1 = 0
        score2 = 0
        if entry == str(1):
            score1 = 1
            score2 = 0
        elif entry == str(2):
            score1 = 0
            score2 = 1
        elif entry == "x":
            score1 = 0.5
            score2 = 0.5

        return [score1, score2]

    def get_tournoi(self, id_tournoi):
        for tournoi_in_table in self.table_tournois:
            if str(id_tournoi) == str(tournoi_in_table.doc_id):
                tournoi = Tournoi(nom_tournoi=tournoi_in_table['nom_tournoi'],
                                  lieu=tournoi_in_table['lieu'],
                                  date_debut=tournoi_in_table['date_debut'],
                                  date_fin=tournoi_in_table['date_fin'],
                                  nombre_tours=tournoi_in_table['nombre_tours'],
                                  controle_du_temps=tournoi_in_table['controle_du_temps'],
                                  description=tournoi_in_table['description'],
                                  joueurs=tournoi_in_table['joueurs'],
                                  tours=tournoi_in_table['tours'],
                                  flag=tournoi_in_table['flag']
                                  )
                return tournoi

    def get_tours(self, id_tournoi):
        all_tours = []
        for tournoi_in_table in self.table_tournois:
            if str(id_tournoi) == str(tournoi_in_table.doc_id):
                tours = tournoi_in_table['tours']
                for tour in tours:
                    all_tours.append(tour)
            return all_tours

    def recuperer_joueur(self, id_joueur):
        for joueur in self.table_joueurs:
            if str(joueur.doc_id) == id_joueur:
                return joueur

    def verifier_indice(self, indice):
        for joueur in self.table_joueurs:
            if str(joueur.doc_id) == indice:
                return True

    def afficher_liste_tournois(self):
        for tournoi in self.table_tournois:
            results = str(tournoi.doc_id) + " : " + tournoi["nom_tournoi"] + " " + \
                      tournoi["lieu"] + " (" + tournoi["date_debut"] + ")"  + " " + tournoi["flag"]
            self.view.affichage_generique(results)

    def get_flag_tour(self, num_tour, id_tournoi):
        flag = "Not Found"
        for tournoi_in_table in self.table_tournois:
            if str(tournoi_in_table.doc_id) == str(id_tournoi):
                tours_in_table = tournoi_in_table['tours']
                for tour_in_table in tours_in_table:
                    if tour_in_table['num_tour'] == str(num_tour):
                        flag = tour_in_table['flag']
                        return flag

    def dernier_tour_tournoi(self, id_tournoi):
        i = 0
        dernier_tour = 1
        for tournoi_in_table in self.table_tournois:
            if str(tournoi_in_table.doc_id) == id_tournoi:
                tours = tournoi_in_table['tours']
                for tour in tours:
                    i += 1
                    dernier_tour = i
        return dernier_tour

    def saisir_resultat(self):
        self.afficher_liste_tournois()
        id_tournoi = self.view.prompt_choisir_tournoi()
        self.afficher_tours_tournoi(id_tournoi)
        dernier_tour = self.dernier_tour_tournoi(id_tournoi)
        num_tour = self.view.prompt_choisir_tour()
        if num_tour == str(dernier_tour) and self.get_flag_tour(num_tour, id_tournoi) == "En Cours":
            self.generation_paires(num_tour, id_tournoi)
        else:
            self.view.prompt_alerte_saisie_tour()
            self.afficher_sous_menu("2")

    def score_cumule_joueur(self, id_joueur, id_tournoi):
        score_joueur = 0.0
        for tournoi_in_table in self.table_tournois:
            if str(id_tournoi) == str(tournoi_in_table.doc_id):
                tours = tournoi_in_table['tours']
                for tour in tours:
                    matchs = tour['tour_matchs']
                    for match in matchs:
                        if str(match['resultat'][0][0]) == id_joueur:
                            score_joueur += match['resultat'][0][1]
                        if match['resultat'][1][0] == id_joueur:
                            score_joueur += match['resultat'][0][1]
        return score_joueur

    def joueur_a_deja_joue_contre(self, id_joueur, id_adversaire, id_tournoi):
        tournoi = self.table_tournois.get(doc_id=int(id_tournoi))
        tours = tournoi['tours']
        matchs = []
        reponse = False
        for tour in tours:
            matchs_tournoi = tour['tour_matchs']
            for match in matchs_tournoi:
                matchs.append(match)

        for match in matchs:
            if str(id_joueur) == str(match['resultat'][0][0]) or str(id_joueur) == str(match['resultat'][1][0]):
                if str(id_adversaire) == match['resultat'][1][0] or str(id_joueur) == str(match['resultat'][1][0]) :
                    reponse = True

                return reponse

    def generation_paires(self, num_tour, id_tournoi):
        '''pour limiter le code mettre get_joueurs dans get_tournoi'''
        tournoi = self.get_tournoi(id_tournoi)
        tournoi.joueurs = self.get_joueurs(tournoi.joueurs)


        if str(num_tour) == "1":
            horodatage_debut_tour = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.ranked_joueurs = sorted(tournoi.joueurs, key=lambda x: x.classement, reverse=True)
            nb_joueurs = len(self.ranked_joueurs)
            i = 0
            while 2 * i < nb_joueurs:
                # Generation de la liste des matchs dans matchs_tour
                index1 = i
                index2 = (i + int(nb_joueurs / 2))
                resultat = self.view.prompt_resultat_match(self.ranked_joueurs[index1],
                                                           self.ranked_joueurs[index2])

                joueur_blanc = [self.ranked_joueurs[index1], self.translate_resultat(resultat)[0]]
                joueur_noir = [self.ranked_joueurs[index2], self.translate_resultat(resultat)[1]]

                match = Match(resultat=(joueur_blanc, joueur_noir))

                self.matchs_tour.append(match)
                i += 1

            # Enregistrement Objet Tour
            nom_tour = "Tour " + str(num_tour)
            horodatage_fin_tour = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tour = Tour(str(num_tour), nom_tour, horodatage_debut_tour, horodatage_fin_tour, self.matchs_tour,
                        "Termine", id_tournoi)

            # Serialisation du Tour
            serialized_tours = []
            serialized_tour = self.serialize_tour(tour)
            serialized_tours.append(serialized_tour)
            # Mise à Jour de Tour dans le Tournoi
            for tournoi_in_table in self.table_tournois:
                if str(tournoi_in_table.doc_id) == str(id_tournoi):
                    self.table_tournois.update({"tours": serialized_tours},
                                               doc_ids=[tournoi_in_table.doc_id])

            # Generation du Tour Suivant
            num_tour_suivant = str(int(num_tour) + 1)
            nom_tour_suivant = "Tour " + str(num_tour_suivant)
            tour_suivant = Tour(num_tour_suivant, nom_tour_suivant, None, None, [], "En Cours", None)
            serialized_tour_suivant = self.serialize_tour(tour_suivant)
            serialized_tours = self.get_tours(id_tournoi)
            serialized_tours.append(serialized_tour_suivant)
            # Mise à Jour de Tour dans le Tournoi
            for tournoi_in_table in self.table_tournois:
                if str(tournoi_in_table.doc_id) == str(id_tournoi):
                    self.table_tournois.update({"tours": serialized_tours},
                                               doc_ids=[tournoi_in_table.doc_id])

        if int(num_tour) > 1 and int(num_tour) <= 4:
            # Ecriture des score cumules
            for joueur in tournoi.joueurs:
                id_joueur = self.get_joueur_id(joueur)
                joueur.score_tournoi = self.score_cumule_joueur(id_joueur, id_tournoi)

            horodatage_debut_tour = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.ranked_joueurs = sorted(tournoi.joueurs, key=lambda x: (x.score_tournoi, x.classement), reverse=True)
            nb_joueurs = len(self.ranked_joueurs)


            i = 0
            self.matchs_tour = []
            while 2 * i < nb_joueurs:
                # Generation de la liste des matchs dans matchs_tour
                index1 = i
                index2 = (i + 1)

                resultat = self.view.prompt_resultat_match(self.ranked_joueurs[index1],
                                                           self.ranked_joueurs[index2])

                joueur_blanc = [self.ranked_joueurs[index1], self.translate_resultat(resultat)[0]]
                joueur_noir = [self.ranked_joueurs[index2], self.translate_resultat(resultat)[1]]
                match = Match(resultat=(joueur_blanc, joueur_noir))
                self.matchs_tour.append(match)
                i += 1


            # Enregistrement Objet Tour
            nom_tour = "Tour " + str(num_tour)
            horodatage_fin_tour = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tour = Tour(str(num_tour), nom_tour, horodatage_debut_tour, horodatage_fin_tour, self.matchs_tour,
                        "Termine", id_tournoi)

            # Serialisation du Tour
            serialized_tours = self.get_tours(id_tournoi)
            serialized_tours.pop()
            serialized_tour = self.serialize_tour(tour)
            serialized_tours.append(serialized_tour)

            # Mise à Jour de Tour dans le Tournoi
            for tournoi_in_table in self.table_tournois:
                if str(tournoi_in_table.doc_id) == str(id_tournoi):
                    self.table_tournois.update({"tours": serialized_tours},
                                               doc_ids=[tournoi_in_table.doc_id])

            # Generation du Tour Suivant
            if int(num_tour) < int(tournoi.nombre_tours):
                num_tour_suivant = str(int(num_tour) + 1)
                nom_tour_suivant = "Tour " + str(num_tour_suivant)
                tour_suivant = Tour(num_tour_suivant, nom_tour_suivant, None, None, [], "En Cours", None)
                serialized_tour_suivant = self.serialize_tour(tour_suivant)
                serialized_tours = self.get_tours(id_tournoi)
                serialized_tours.append(serialized_tour_suivant)

                # Mise à Jour de Tour dans le Tournoi
                for tournoi_in_table in self.table_tournois:
                    if str(tournoi_in_table.doc_id) == str(id_tournoi):
                        self.table_tournois.update({"tours": serialized_tours},
                                                   doc_ids=[tournoi_in_table.doc_id])
            # Flag Tournoi Termine
            if int(num_tour) == int(tournoi.nombre_tours):
                # Flag Tournoi Termine
                for tournoi_in_table in self.table_tournois:
                    if str(tournoi_in_table.doc_id) == str(id_tournoi):
                        self.table_tournois.update({'flag': 'Termine'},
                                                   doc_ids=[tournoi_in_table.doc_id])

    def afficher_joueurs_alphabetique(self):
        joueurs = []
        for joueur_in_table in self.table_joueurs:
            joueur = self.deserialize_joueur(joueur_in_table)
            joueurs.append(joueur)

        joueurs = sorted(joueurs, key=lambda x: x.nom, reverse=False)
        i = 0
        for joueur in joueurs:
            i += 1
            results = str(i) + " : " + joueur.nom.upper() + " " + \
                      joueur.prenom.capitalize() + " " + \
                      str(joueur.date_de_naissance) + " " + \
                      joueur.sexe + " " + \
                      str(joueur.classement)
            self.view.affichage_generique(results)

    def afficher_joueurs_classement(self):
        joueurs = []
        for joueur_in_table in self.table_joueurs:
            joueur = self.deserialize_joueur(joueur_in_table)
            joueurs.append(joueur)

        joueurs = sorted(joueurs, key=lambda x: x.classement, reverse=True)
        i = 0
        for joueur in joueurs:
            i += 1
            results = str(i) + " : (" + str(joueur.classement) + ") " + \
                      joueur.nom + " " + \
                      joueur.prenom + " " + \
                      str(joueur.date_de_naissance) + " " + \
                      joueur.sexe
            self.view.affichage_generique(results)

    def afficher_joueurs_tournoi_alphabetique(self):
        self.afficher_liste_tournois()

        joueurs = []
        indice_tournoi = self.view.prompt_choisir_tournoi()
        tournoi = self.table_tournois.get(doc_id=int(indice_tournoi))
        joueurs_ids = tournoi['joueurs']

        for joueurs_id in joueurs_ids:
            joueur = self.get_joueur(joueurs_id)
            joueurs.append(joueur)
        i = 0
        joueurs = sorted(joueurs, key=lambda x: x.nom, reverse=False)
        for joueur in joueurs:
            i += 1
            results = str(i) + " : " + joueur.nom + " " + \
                      joueur.prenom + " " + \
                      str(joueur.date_de_naissance) + " " + \
                      joueur.sexe + " (" + \
                      str(joueur.classement) + ")"
            self.view.affichage_generique(results)

    def afficher_joueurs_tournoi_classement(self):
        self.afficher_liste_tournois()
        joueurs = []
        indice_tournoi = self.view.prompt_choisir_tournoi()
        tournoi = self.table_tournois.get(doc_id=int(indice_tournoi))
        joueurs_ids = tournoi['joueurs']

        for joueurs_id in joueurs_ids:
            joueur = self.get_joueur(joueurs_id)
            joueurs.append(joueur)

        joueurs = sorted(joueurs, key=lambda x: x.classement, reverse=True)
        i = 0
        for joueur in joueurs:
            i += 1
            results = str(i) + " : (" + str(joueur.classement) + ") " + \
                      joueur.nom + " " + \
                      joueur.prenom + " " + \
                      str(joueur.date_de_naissance) + " " + \
                      joueur.sexe
            self.view.affichage_generique(results)

    def afficher_tours_tournoi(self, id_tournoi):
        for tournoi_in_table in self.table_tournois:
            if str(id_tournoi) == str(tournoi_in_table.doc_id):
                tours = tournoi_in_table['tours']
                for tour in tours:
                    results = str(tour['num_tour']) + " : " + tour['nom_tour'] + " " + \
                              str(tour['date_debut']) + " " + str(tour['date_fin']) + " " + tour['flag']
                    self.view.affichage_generique(results)

    def afficher_match_tournois(self):
        self.afficher_liste_tournois()
        id_tournoi = self.view.prompt_choisir_tournoi()
        tournoi = self.table_tournois.get(doc_id=int(id_tournoi))
        self.afficher_tours_tournoi(id_tournoi)
        id_tour = self.view.prompt_choisir_tour()
        tours = tournoi['tours']
        for tour in tours:
            if tour['num_tour'] == id_tour:
                matchs_tournoi = tour['tour_matchs']
                for match in matchs_tournoi:
                    joueur_blanc = self.get_joueur(match['resultat'][0][0])
                    joueur_noir = self.get_joueur(match['resultat'][1][0])
                    score_blanc = match['resultat'][0][1]
                    score_noir = match['resultat'][1][1]
                    results = (joueur_blanc.prenom + " " + joueur_blanc.nom + " " + str(score_blanc) + "     " +
                          joueur_noir.prenom + " " + joueur_noir.nom + " " + str(score_noir))
                    self.view.affichage_generique(results)

    def run(self):
        self.afficher_menu_principal()

    def afficher_menu_principal(self):
        index = self.view.show_menu()
        self.afficher_sous_menu(index)

    def afficher_sous_menu(self, index):
        if index == str(1):
            index2 = self.view.show_menu_joueurs()
            self.afficher_sous_menu_joueurs(index2)
        elif index == str(2):
            index2 = self.view.show_menu_tournois()
            self.afficher_sous_menu_tournois(index2)
        elif index == str(3):
            index2 = self.view.show_menu_rapports()
            self.afficher_sous_menu_rapports(index2)
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()

    def afficher_sous_menu_joueurs(self, index):
        if index == str(1):
            self.set_joueur()
        elif index == str(2):
            self.update_joueur_classement()
        elif index == str(3):
            self.afficher_joueurs([])
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()
        self.afficher_sous_menu("1")

    def afficher_sous_menu_tournois(self, index):
        if index == str(1):
            self.creer_tournoi()
        elif index == str(2):
            self.afficher_liste_tournois()
        elif index == str(3):
            self.saisir_resultat()
            self.afficher_sous_menu("2")
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()
        self.afficher_sous_menu("2")

    def afficher_sous_menu_rapports(self, index):
        if index == str(1):
            self.afficher_joueurs_alphabetique()
        elif index == str(2):
            self.afficher_joueurs_classement()
        elif index == str(3):
            self.afficher_joueurs_tournoi_alphabetique()
        elif index == str(4):
            self.afficher_joueurs_tournoi_classement()
        elif index == str(5):
            self.afficher_liste_tournois()
        elif index == str(6):
            self.afficher_liste_tournois()
            id_tournoi = self.view.prompt_choisir_tournoi()
            self.afficher_tours_tournoi(id_tournoi)
        elif index == str(7):
            self.afficher_match_tournois()
        elif index == str(8):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()
        self.afficher_sous_menu("3")
