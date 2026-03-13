import gradio as gr
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1. TES FONCTIONS DE GRAPHIQUES (LES RECETTES)

def graph_internet(df):
    tranches_voulues = ['13-18', '19-25', '26-35', '36-45', '46-60']
    df_filtre = df[df['age_group'].isin(tranches_voulues)]
    
    # Calcul des moyennes
    df_grouped = df_filtre.groupby('age_group')[['social_media_hours', 'work_or_study_hours', 'entertainment_hours']].mean()
    df_grouped = df_grouped.reindex(tranches_voulues)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    df_grouped.plot(kind='bar', stacked=True, ax=ax, color=['#FF9999', '#66B3FF', '#99FF99'])
    
    # Force le dessin pour calculer les positions des textes
    fig.canvas.draw()

    for p in ax.patches:
        h = p.get_height()
        if h > 0.4: # N'affiche que si la case est assez grande
            ax.text(p.get_x() + p.get_width()/2, 
                    p.get_y() + h/2, 
                    f'{h:.1f}h', 
                    ha='center', va='center', 
                    fontweight='bold', 
                    zorder=10) # Texte au premier plan
    
    plt.title("Temps d'écran moyen par activité et âge")
    plt.ylabel("Heures")
    plt.tight_layout()
    return fig

def graph_lecture(df):
    df.columns = df.columns.str.strip()
    reading_col = "Amount of time spent reading books per day"
    df[reading_col] = pd.to_numeric(df[reading_col], errors="coerce")
    
    # Filtrage 18-24 ans
    df_filtered = df[(df["Age"] >= 18) & (df["Age"] <= 24)].copy()
    avg_hours_by_age = df_filtered.groupby("Age")[reading_col].mean()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    plt.plot(avg_hours_by_age.index, avg_hours_by_age.values, 
             marker='o', linestyle='-', color='b', linewidth=2, markersize=8)

    for x, y in zip(avg_hours_by_age.index, avg_hours_by_age.values):
        plt.text(x, y + 0.05, f"{y:.2f} h", ha='center', fontweight='bold', color='blue')

    plt.xlabel("Âge")
    plt.ylabel("Heures de lecture")
    plt.title("Évolution du temps de lecture moyen (18-24 ans)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(range(18, 25))
    plt.tight_layout()
    return fig


# 2. LE PILOTE (LE LIEN AVEC L'API)


def piloter(choix):
    try:
        if choix == "Consommation Internet":
            r = requests.get("http://127.0.0.1:5000/api/internet")
            return graph_internet(pd.DataFrame(r.json()))
        
        elif choix == "Habitudes de Lecture":
            r = requests.get("http://127.0.0.1:5000/api/lecture")
            return graph_lecture(pd.DataFrame(r.json()))
            
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

# 3. L'INTERFACE GRADIO SIMPLIFIÉE

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("#  Mon Analyse de Données")
    gr.Markdown("Sélectionnez l'analyse que vous souhaitez visualiser.")
    
    with gr.Row():
        selection = gr.Radio(
            ["Consommation Internet", "Habitudes de Lecture"], 
            label="Choisir l'analyse", 
            value="Consommation Internet"
        )
    
    plot_output = gr.Plot()

    # Mise à jour quand on clique
    selection.change(fn=piloter, inputs=selection, outputs=plot_output)
    
    # Chargement initial
    demo.load(fn=piloter, inputs=selection, outputs=plot_output)

if __name__ == "__main__":
    demo.launch()