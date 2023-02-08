from flask import Flask  # , render_template, request
from flask_mysqldb import MySQL
import requests
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'autobusiki'

mysql = MySQL(app)

url = "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e927d-4ad3-9500-4ab9e55deb59" \
      "&apikey=d" \
      "3267d41-972a-4eef-b555-b7df47526f15&type=1"
resp = requests.get(url)
print(resp.status_code)

parsed = json.loads(resp.content)
parsed2 = parsed['result']
for i in parsed2:
    print(i)

# with app.app_context():
#     for i in parsed2:
#         line = i["Lines"]
#         brigade = i['Brigade']
#         vehiclenumber = i["VehicleNumber"]
#         time = i['Time']
#         lon = i["Lon"]
#         lat = i["Lat"]
#         key = str(vehiclenumber+"_"+line)
#         print(key)
#         cursor = mysql.connection.cursor()
#         cursor.execute(''' INSERT INTO listaautobusow VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s)''',
#                        (vehiclenumber,line, brigade, lon, lat, time, time, line, key))
#         mysql.connection.commit()

with app.app_context():
    for i in parsed2:
        line = i["Lines"]
        brigade = i['Brigade']
        vehiclenumber = i["VehicleNumber"]
        time = i['Time']
        lon = i["Lon"]
        lat = i["Lat"]
        key = str(vehiclenumber+"_"+line)
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO listaautobusow VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                        Lon = IF(Vehicle_number = %s AND Line = %s, %s, Lon);''',
                       (vehiclenumber,line, brigade, lon, lat, time, time, line, key, vehiclenumber, line, lon))
        mysql.connection.commit()













# @app.route('/take')
# def take():
#     for j in parsed2:
#         line = j["Lines"]
#         brigade = j['Brigade']
#         vehiclenumber = j["VehicleNumber"]
#         time = j['Time']
#         lon = j["Lon"]
#         lat = j["Lat"]
#         cursor = mysql.connection.cursor()
#         cursor.execute(''' INSERT INTO listaautobusów VALUES(%s,%s) ''',(vehiclenumber,line))
#         mysql.connection.commit()
# Executing SQL Statements
# for i in parsed2:
#     cursor = mysql.connection.cursor()
#     Linia = i["linia"]
#     cursor.execute(''' INSERT INTO listaautobusów VALUES(Linia) ''')
#     cursor.close()
#     mysql.connection.commit()
