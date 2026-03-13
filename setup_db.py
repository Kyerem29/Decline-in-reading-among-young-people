import sqlite3
import pandas as pd

def init_database():
    # Connexion (crée le fichier s'il n'existe pas)
    conn = sqlite3.connect('mon_projet.db')
    
    # Importation des 3 CSV vers SQL
    df_internet = pd.read_csv('daily_internet_usage_by_age_group.csv')
    df_lecture = pd.read_csv('reading_habits_students.csv')
    df_global = pd.read_csv('Global.csv')

    # Nettoyage rapide (enlever les espaces dans les noms de colonnes)
    df_lecture.columns = df_lecture.columns.str.strip()

    # Enregistrement en tables SQL
    df_internet.to_sql('internet', conn, if_exists='replace', index=False)
    df_lecture.to_sql('lecture', conn, if_exists='replace', index=False)
    df_global.to_sql('global_stats', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Base de données 'mon_projet.db' créée avec succès !")

if __name__ == "__main__":
    init_database()