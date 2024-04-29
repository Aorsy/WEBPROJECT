from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

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


if __name__ == '__main__':
     app.run(debug=True)

