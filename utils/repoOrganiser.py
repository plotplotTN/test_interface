

from pathlib import Path
import os 
import shutil
from utils import isDir, isFile, extract_dir_name, extract_file_name

class repoOrganiser():

    def __init__(self,repo):
        if not isDir(repo):
            raise ValueError(f"The path {repo} is not a directory.")
        
        self.repo = repo
        print("hle")
        pass

    def organise(self):
        repertoire_source = self.repo
        fichiers_dict = {}
        fichiers_fichiers_dict = {}
        for element in os.listdir(repertoire_source):
            element_path = os.path.join(repertoire_source, element)
    
            # Vérifie si fichier .CSV ou .htm
            if element.lower().endswith('.csv') or element.lower().endswith('.htm'):
                # Obtient du nom 
                nom_requete = os.path.splitext(element)[0].lower()
        
                # Ajouter à la liste dans le dictionnaire
                if nom_requete in fichiers_dict:
                    fichiers_dict[nom_requete].append(element_path)
                else:
                    fichiers_dict[nom_requete] = [element_path]
    
            # Vérifie si dossier "_fichiers"
            elif os.path.isdir(element_path) and element.lower().endswith('_fichiers'):
                nom_requete = element[:-len('_fichiers')].lower()        
                fichiers_fichiers_dict[nom_requete] = element_path

        # création du répertoire et déplacement des fichiers correspondants
        for nom_requete, fichiers in fichiers_dict.items():
            sous_repertoire = os.path.join(repertoire_source, nom_requete)
            os.makedirs(sous_repertoire, exist_ok=True)
    
            for fichier in fichiers:
                shutil.move(fichier, sous_repertoire)

        # déplace les dossiers "_fichiers" dans le répertoire
        for nom_requete, dossier_fichiers in fichiers_fichiers_dict.items():
            sous_repertoire = os.path.join(repertoire_source, nom_requete)
            shutil.move(dossier_fichiers, sous_repertoire)

        # suppression les dossiers "_fichiers" vides
        for element in os.listdir(repertoire_source):
            element_path = os.path.join(repertoire_source, element)
            if os.path.isdir(element_path) and element.lower().endswith('_fichiers') and not os.listdir(element_path):
                os.rmdir(element_path)

    def setRepo(self,newRepo):
        if not isDir(newRepo):
            raise ValueError(f"The path {newRepo} is not a directory.")
        self.repo = newRepo
        pass

    def getRepo(self):
        return self.repo

if __name__ == "__main__":

    repo = r"C:\\Users\\romai\\Downloads\\bordereauxcsv-20230911T144458Z-001\\bordereauxcsv"
    print("oui")
    repoOrg = repoOrganiser(repo)
    repoOrg.organise()
    pass