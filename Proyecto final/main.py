from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

# Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_PORT'] =  3308

#Almacenamiento de la conexión en una variable
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api',methods=['GET','POST'])
def api():
    if request.method == 'GET':
        return render_template('api.html')
  #Si se recibe por POST
    if request.form['search']:
        url = "https://www.datos.gov.co/resource/w735-yw39.json?nombre=" +request.form['search']
    #Obtener la información y almacenarla en una variable
        giphy = requests.get(url)
    #Obtener los datos en formato JSON
        dataG = giphy.json()
    #Renderizado de la data
        return render_template('api.html', data=dataG)
    else:
        return render_template('api.html')


if __name__ == '__main__':
     app.run(debug=True)

