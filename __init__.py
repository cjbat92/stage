from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen 
import sqlite3
import requests
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def Mapagedecontact():
    return render_template("Pagecontact.html")

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def colonnes():
    return render_template("histogrammeTawarano.html")

@app.route("/commits/")
def commits_graph():
    # Récupération des commits depuis l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    data = response.json()

    # Extraire les minutes depuis chaque commit
    minutes = []
    for commit in data:
        date_str = commit["commit"]["author"]["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        minutes.append(date_obj.minute)

    # Compter le nombre de commits par minute
    minute_counts = Counter(minutes)

    # Transformer en format utilisable pour le frontend
    chart_data = [["Minute", "Commits"]]
    for i in range(60):
        chart_data.append([f"{i:02d}", minute_counts.get(i, 0)])

    return render_template("commits.html", chart_data=chart_data)

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


  
if __name__ == "__main__":
  app.run(debug=True)
