from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen 
import sqlite3  
 
                                                                                                                                       
app = Flask(__name__)                                                                                                                   
                                                                                                                                       
@app.route('/')
def CJBAT():
    return render_template('index.html')

@app.route("/about/")
def A_propos():
    return render_template("about.html")

@app.route("/services/")
def Nos_services():
    return render_template("services.html")

@app.route("/projects/")
def Realisations():
    return render_template("projects.html")

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # 🔧 Ici tu peux :
    # - Envoyer un email
    # - Enregistrer dans une base de données
    # - Log dans un fichier

    print("Message reçu :", name, email, message)

    return jsonify({"message": "Merci pour votre message, nous vous répondrons rapidement."})


  
if __name__ == "__main__":
  app.run(debug=True)
