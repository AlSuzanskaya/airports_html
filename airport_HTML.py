import flask
import mysql.connector
import configuration as c

app = flask.Flask(__name__)
@app.route('/login', methods=['GET'])
def get_form():
    return flask.render_template('airports.html')

@app.route('/login', methods=['POST'])
def post_form():
    depart = flask.request.form['departure']
    arr = flask.request.form['arrival']


    cnx = mysql.connector.connect(user=c.user, password=c.password,
                                  host=c.host,
                                  database=c.database)

    cursor = cnx.cursor()
    query = (f"SELECT  r.src_airport, ai.airport,  ai.city, ai.country, r.dst_airport, air.airport, air.city, air.country \
         FROM airports AS ai INNER JOIN routes AS r ON ai.iata=r.src_airport INNER JOIN airports AS air ON air.iata=r.dst_airport \
        WHERE ai.city LIKE '%{depart}%' AND air.city LIKE '%{arr}%'")

    cursor.execute(query)

    cont = '<body bgcolor="#CD5C5C" style="color:#fff; font-family: Verdana, Arial, Helvetica, sans-serif;font-size:80%" align="center"> \
    <table  bgcolor="#CD5C5C" style="width:100%"; border-collapse:collapse; font-family: Verdana, Arial, Helvetica,\
     sans-serif>\
     <tr><th align="left">iata</th><th align="left">airport</th><th align="left">city</th><th align="left">country</th>\
     <th align="left">iata</th><th align="left">airport</th><th align="left">city</th><th align="left">country</th></tr>'
    for (dep_code, dep_airport,  dep_city, dep_country, ar_code, ar_airport, ar_city, ar_country) in cursor:
        cont += f'<tr><td>{dep_code}</td><td>{dep_airport}</td><td>{dep_city}</td><td>{dep_country}</td><td>{ar_code}</td><td>{ar_airport}</td><td>{ar_city}</td><td>{ar_country}</td><</tr>'

    cursor.close()
    cont += '</table> </body>'
    cnx.close()

    return cont

if __name__ == '__main__':
    app.run()