import pandas as pd 
from dateutil.parser import parse
from utils import apiCallObject
from utils import isDir, isFile, extract_dir_name, extract_file_name


class Comparateur_csv:


    def __init__(self, file_path1, file_path2,delimiter1=";",delimiter2=";"):
                
        if not isFile(file_path1):
            raise ValueError(f"The path {file_path1} is not a file.")
        if not isFile(file_path2):
            raise ValueError(f"The path {file_path2} is not a file.")
        
        self.delimiter1 = delimiter1
        self.delimiter2 = delimiter2

        self.df1 = self.load_dataframe(file_path1,delimiter=self.delimiter1)
        self.df2 = self.load_dataframe(file_path2,delimiter=self.delimiter2)

    def load_dataframe(self, file_path,delimiter=";"):
        # Lire le fichier CSV en tant que DataFrame avec le bon séparateur
        df = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=delimiter)
        self.df_cleaner(df)  # Nettoyer le DataFrame
        return df

    def df_cleaner(self, df):
        num_columns = len(df.columns)
        for col_idx in range(num_columns):
            if col_idx not in [num_columns - 2, num_columns - 1]:  # Colonnes sauf les deux dernières
                df.iloc[:, col_idx].fillna(method='ffill', inplace=True)  # Remplir les valeurs NaN avec la valeur précédente

        df.iloc[:, -2].fillna(0, inplace=True)  # Remplir les valeurs NaN de la colonne VOLUME avec 0

        # Supprimer les lignes où la colonne VOLUME est égale à 0
        df.drop(df[df.iloc[:, -2] == 0].index, inplace=True)

    def compare_noms_colonne(self):

        if len(self.df1.columns) == len(self.df2.columns):
            return "Test nom des colonnes =", True
        else:
            return "Test nom des colonnes =", False

    def nombre_colonne(self):
        if set(self.df1.columns) == set(self.df2.columns):
            return "Test nombre de colonnes =", True
        else:
            return "Test nombre de colonnes =", False

    def compare_noms_attribues(self):
        selected_columns_df1 = self.df1.columns[1:-3].tolist()
        if selected_columns_df1 != self.df2.columns[1:-3].tolist():
            return "Test noms des attributs =", False
        else:
            return "Test noms des attributs =", True

    def compare_catégorie_attribues(self):
        selected_columns_df1 = self.df1.columns[1:-3].tolist()
        for col in selected_columns_df1:
            if sorted(self.df1[col].unique()) != sorted(self.df2[col].unique()):
                return f"Test catégories des attributs pour {col} =", False
        return "Test catégories des attributs =", True
    
    def compare_volume_attribues(self):
        attrib_cols = self.df1.columns[1:-3].tolist()

        volumes_by_attrib_df1 = {col: self.df1.groupby(col).sum().iloc[:, -2] for col in attrib_cols}
        volumes_by_attrib_df2 = {col: self.df2.groupby(col).sum().iloc[:, -2] for col in attrib_cols}

        for col in attrib_cols:
            if not volumes_by_attrib_df1[col].equals(volumes_by_attrib_df2[col]):
                return "Test volumes pour l'attribut {} =".format(col), False

        return "Test volumes par attribut =", True

    # Test 7 : Avoir les même format de dates
    def detect_date_formats(self, series):
        """
        Détecte les formats de date distincts dans une série de dates.

        Args:
        series: Une série Pandas contenant des dates.

        Returns:
            set: Un ensemble de formats de date distincts.
        """
        date_formats = set()
        for date_str in series:
            try:
                parse(date_str, fuzzy=True)
                date_formats.add("fuzzy")
            except ValueError:
                try:
                    parse(date_str)
                    date_formats.add("strict")
                except ValueError:
                    date_formats.add("invalide")
        return date_formats

    def compare_date_formats(self):
        dates_df1 = self.df1.iloc[:, 0]
        dates_df2 = self.df2.iloc[:, 0]

        formats_df1 = self.detect_date_formats(dates_df1)
        formats_df2 = self.detect_date_formats(dates_df2)

        if formats_df1 == formats_df2:
            return "Test format date =", True
        else:
            return "Test format date =", False
        
    # Test 8 : Avoir les même volumes par dates distinctes
    def compare_volume_dates_distinctes(self):
        # Sélectionnez la colonne de dates et de volumes dans les deux DataFrames
        dates_df1 = self.df1.iloc[:, 0]
        volumes_df1 = self.df1.iloc[:, -2]

        dates_df2 = self.df2.iloc[:, 0]
        volumes_df2 = self.df2.iloc[:, -2]

        # Créez un DataFrame pour stocker les volumes par date et DataFrame
        volumes_dates_df1 = pd.DataFrame({'Date': dates_df1, 'Volume_df1': volumes_df1})
        volumes_dates_df2 = pd.DataFrame({'Date': dates_df2, 'Volume_df2': volumes_df2})

        # Fusionnez les DataFrames en utilisant la colonne 'Date' comme clé
        merged_df = volumes_dates_df1.merge(volumes_dates_df2, on='Date', how='outer')

        # Comparez les volumes pour chaque date
        for index, row in merged_df.iterrows():
            if row['Volume_df1'] != row['Volume_df2']:
                return "Test volumes par dates distinctes =", False

        return "Test volumes par dates distinctes =", True

    # Test 9 : Avoir les même moyenne de JO par dates
    def compare_moyenne_JO_dates(self):
        # Sélectionnez la dernière colonne (JO) dans les deux DataFrames
        jo_df1 = self.df1.iloc[:, -1]
        jo_df2 = self.df2.iloc[:, -1]

        #  Sélectionnez la colonne de dates dans les deux DataFrames
        dates_df1 = self.df1.iloc[:, 0]
        dates_df2 = self.df2.iloc[:, 0]

        # Créez un DataFrame pour stocker les dates et les JO de chaque DataFrame
        jo_dates_df1 = pd.DataFrame({'Date': dates_df1, 'JO_df1': jo_df1})
        jo_dates_df2 = pd.DataFrame({'Date': dates_df2, 'JO_df2': jo_df2})

        # Fusionnez les DataFrames en utilisant la colonne 'Date' comme clé
        merged_df = jo_dates_df1.merge(jo_dates_df2, on='Date', how='outer')

        # Calculez la moyenne des JO pour chaque date
        merged_df['Moyenne_JO'] = (merged_df['JO_df1'] + merged_df['JO_df2']) / 2

        # Comparez les moyennes des JO pour chaque date
        for index, row in merged_df.iterrows():
            if not pd.isna(row['JO_df1']) and not pd.isna(row['JO_df2']) and row['JO_df1'] != row['JO_df2']:
                return "Test moyenne JO pour la date {} =".format(row['Date']), False

        return "Test moyenne JO par dates distinctes =", True
    
    def run_tests(self):
        # Liste pour stocker les résultats des tests
        test_results = []

        # Test 1 : Avoir les même noms de colonnes
        test_results.append(self.compare_noms_colonne())

        # Test 2 : Avoir les même nombre de colonnes
        test_results.append(self.nombre_colonne())

        test_results.append(self.compare_date_formats())

        # Test 3 : Avoir les même nombre d'attributs
        test_results.append(self.compare_noms_attribues())

        # Test 4 : Avoir les même "valeur" ou catégorie dans les attributs
        test_results.append(self.compare_catégorie_attribues())

        # Test 6 : Avoir les même volumes par attributs et par catégorie d'attribut
        test_results.append(self.compare_volume_attribues())

        # Test 8 : Avoir les même volumes par dates distinctes
        test_results.append(self.compare_volume_dates_distinctes())

        # Test 9 : Avoir les même moyenne de JO par dates
        test_results.append(self.compare_moyenne_JO_dates())

        # Affiche les résultats des tests
        for test_result in test_results:
            print(test_result)



if __name__ == "__main__":

    comparator = Comparateur_csv("output.csv", "DATE_PRV_FF.CSV")
    print(comparator.run_tests())




