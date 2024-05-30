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
app.config['MYSQL_DB'] = 'hotel'
app.config['MYSQL_PORT'] =  3306

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

#CRUD - insertar
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Acceso a los campos del formulario
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        email = request.form['email']
        password = request.form['password']
    
        cursor = mysql.connection.cursor()
        #Instrucción SQL
        cursor.execute("INSERT INTO huesped VALUES(%s, %s, %s, %s)", (nombre, cedula, email, password))
            
        #El commit finaliza la transacción actual
        cursor.connection.commit()      
       
        #Redirecciona al index luego de ejecutar el formulario       
        return redirect(url_for('index'))    
    
    cursor = mysql.connection.cursor()
    #Consula SQL
    cursor.execute("SELECT * FROM huesped")
    #Recorrido de la información almaceda en coches
    huesped = cursor.fetchall()
    #Cierre de cursor
    cursor.close() 
    return render_template('login.html', huesped=huesped)


@app.route('/login-editar/<cedula>', methods=['GET','POST'])
def login_editar(cedula):
    if request.method == 'POST':
        
        #Acceso a los campos del formulario
        nombre = request.form['nombre']
        nueva_cedula = request.form['cedula']
        email = request.form['email']
        password = request.form['password']
        
        #cargue de cursor SQL
        cursor = mysql.connection.cursor()
        #Instrucción SQL
        cursor.execute("""
            UPDATE huesped
            SET nombre=%s, cedula=%s, email=%s, password=%s WHERE cedula = %s
                       """, (nombre, nueva_cedula, email, password, cedula))
        
        #cursor.execute("UPDATE coches SET placa = %s, marca = %s, modelo = %s, precio = %s, ciudad = %s WHERE placa = %s", (placa, marca, modelo, precio, ciudad, placa_id))

        #El commit finaliza la transacción actual
        cursor.connection.commit()        
               
        #Redirecciona al index luego de ejecutar el formulario       
        return redirect(url_for('login'))    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM huesped WHERE cedula = %s", (cedula,))
    huesped = cursor.fetchall()
    #Cierre de cursor
    cursor.close()
    
    return render_template('login.html', huesped=huesped) 

@app.route('/login-eliminar/<cedula>')
def login_eliminar(cedula):
    #cargue de cursor SQL
    cursor = mysql.connection.cursor()
    #Instrucción SQL con clausula WHERE
    #cursor.execute(f"DELETE FROM coches WHERE placa={placa_id}")
    cursor.execute("DELETE FROM huesped WHERE cedula = %s", (cedula,))
    

    #El commit finaliza la transacción actual
    mysql.connection.commit() 
    
    return redirect(url_for('login')) 


###########################################################

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

