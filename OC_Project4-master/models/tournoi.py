class Tournoi:

    def __init__(self, nom_tournoi, lieu, date_debut, date_fin, nombre_tours, controle_du_temps, description, joueurs, tours, flag):
        self.nom_tournoi = nom_tournoi
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.joueurs = joueurs
        self.controle_du_temps = controle_du_temps
        self.description = description
        self.tours = tours
        self.flag = flag