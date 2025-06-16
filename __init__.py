from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen 
import sqlite3

                                                                                                                                       
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

@app.route('/commits/')
def commits_graph():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
            data = json.loads(content)
    except Exception as e:
        return f"Erreur : {e}"

    minutes_count = {}

    for commit in data:
        date_str = commit.get("commit", {}).get("author", {}).get("date")
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_obj.minute
            minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # On transforme le dictionnaire en liste de tuples pour le graphique
    chart_data = sorted(minutes_count.items())

    return render_template('commits.html', chart_data=chart_data)
  
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
