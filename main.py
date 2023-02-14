from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import date
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'autobusiki'

mysql = MySQL(app)

default_lower_limit = [40]
default_upper_limit = [60]

@app.route("/hello")
def hello_world():
    return "<p>Inteligenty system nawadniania!</p>"



@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/send_data', methods=['POST', 'GET'])
def send_data():
    if request.method == 'GET':
        return "wrong method, try post to post data"

    if request.method == 'POST':
        # temperature = request.json['temperature']
        json_data = request.json
        print(json_data)
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO watering (moisture, temperature, humidity, lighting)
                        VALUES(%(moisture)s, %(temperature)s, %(humidity)s, %(lighting)s)''',
                       {'moisture': str(json_data["moisture"]), 'temperature': str(json_data["temperature"]),
                        'humidity': str(json_data["humidity"]), 'lighting': str(json_data["lighting"])})
        mysql.connection.commit()
        cursor.close()
        return "Done!!"


@app.route("/read_data")
def data_reading():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM watering WHERE humidity = 49""")
    user = cur.fetchone()
    print(user)
    print(type(user))
    cur.close()
    return 'heh'



@app.route("/get_data", methods=["POST", "GET"])
def print_some_data():
    today = date.today()
    print(today)
    cur = mysql.connection.cursor()
    # cur.execute("""SELECT * FROM watering """)
    cur.execute("""SELECT * FROM watering WHERE time >= NOW() - INTERVAL 6 DAY """)
    data = cur.fetchall()

    print("Total number of rows in table: ", cur.rowcount)
    dates = []
    humidities = []
    moistures = []
    lightings = []
    temperatures = []
    for row in data:
        dates.append(str(row[0]))
        humidities.append(row[1])
        moistures.append(row[2])
        lightings.append(row[3])
        temperatures.append(row[4])
    print('\n')
    mean_moistures = moistures[:2]
    for i in range(2, len(moistures)):
        mean = (moistures[i] + moistures[i-1] + moistures[i-2]) / 3
        mean_moistures.append(mean)
    cur.close()
    if request.method == "GET":
        return render_template("newchart.html", labels=dates, values=mean_moistures, temperatures=temperatures,
                               humidities=humidities, lightings=lightings)
    else:
        lowlim = str(request.form["lower"])
        uplim = str(request.form["upper"])
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE watering SET upper_limit = %s, lower_limit = %s ORDER BY time DESC LIMIT 1",
                       (uplim, lowlim))
        mysql.connection.commit()
        cursor.close()
        return render_template("newchart.html", labels=dates, values=moistures, temperatures=temperatures,
                               humidities=humidities, lightings=lightings)

@app.route("/test")
def dolnyzakres():
    return str(default_lower_limit[-1])


@app.route("/get_lower_limit", methods=["POST", "GET"])
def getlowerlimit():
    lower_limit = default_lower_limit
    cur = mysql.connection.cursor()
    cur.execute("""SELECT lower_limit FROM watering WHERE lower_limit IS NOT NULL
    ORDER BY time DESC LIMIT 1""")
    limit_data = cur.fetchall()
    lower_limit = str(limit_data[0][0])
    if lower_limit:
        return lower_limit
    else:
        return default_lower_limit

@app.route("/get_upper_limit", methods=["POST", "GET"])
def get_upper_limit():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT upper_limit FROM watering WHERE upper_limit IS NOT NULL
    ORDER BY time DESC LIMIT 1""")
    limit_data = cur.fetchall()
    upper_limit = str(limit_data[0][0])
    if upper_limit:
        return upper_limit
    else:
        return default_lower_limit

