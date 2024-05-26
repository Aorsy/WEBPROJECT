from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
from amadeus import Client, ResponseError
import requests

app = Flask(__name__)

amadeus = Client(
    client_id='1gzHP1s7mAriS2H39q0moTGmKHvYcZ3b',
    client_secret='Sec09AlTO4QeVCZA'
)

# Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_PORT'] =  3308

city_mapping = {
    'New York': 'NYC',
    'Paris': 'PAR',
    'London': 'LON',
    'Tokyo': 'TYO',
    'Sydney': 'SYD',
}

#Almacenamiento de la conexión en una variable
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/habitaciones', methods=['GET', 'POST'])
def habitaciones():
    data = None
    if request.method == 'POST':
        city_name = request.form.get('city_name')
        if city_name:
            city_code = city_mapping.get(city_name)
            if city_code:
                try:
                    response = amadeus.shopping.hotel_offers_search.get(cityCode=city_code)
                    data = response.data
                except ResponseError as error:
                    print(f"Error al llamar a la API de Amadeus: {error}")
                    
                else:
                    print(f"Datos de la API de Amadeus: {data}")
    return render_template('habitaciones.html', data=data)

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/viajes')
def viajes():
    return render_template('viajes.html')

@app.route('/api', methods=['GET', 'POST'])
def api():
    data = None
    if request.method == 'POST':
        search_term = request.form.get('buscar')
        if search_term:
            url = f"https://www.datos.gov.co/resource/w735-yw39.json?nombre={search_term}"
            response = requests.get(url)
            data = response.json()
    return render_template('api.html', data=data)



if __name__ == '__main__':
     app.run(debug=True)

