from flask import Flask, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

def query_db(table_name):
    conn = sqlite3.connect('mon_projet.db')
    # On demande à SQL de nous donner tout le contenu de la table
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.route("/api/internet")
def get_internet():
    return jsonify(query_db('internet'))

@app.route("/api/lecture")
def get_lecture():
    return jsonify(query_db('lecture'))

@app.route("/api/global")
def get_global():
    return jsonify(query_db('global_stats'))

if __name__ == "__main__":
    app.run(port=5000)