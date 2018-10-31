from flask import Flask, jsonify, render_template
from db_conn.my_sql import get_connection
from werkzeug.debug import DebuggedApplication
from os.path import expanduser

app = Flask(__name__)
#app.wsgi_app = DebuggedApplication(app.wsgi_app,True)
app.debug = True

@app.route("/")
def hello():
    sequence = [0,1]
    while sequence[-1] < 9000:
        sequence.append(sequence[-2] + sequence[-1])
    
    mysql_db = get_connection()
    
    query = 'select * from dinner.menu;'

    query = mysql_db.select_query(query)
    columns = query.column_names
    data = []
    for recordset in query.fetchall():
        c = 0
        d = {}
        for row_value in recordset:
            if type(row_value) == int:
                d[columns[c]] = row_value
            else:
                try:
                    #row_value = row_value.decode()
                    d[columns[c]] = str(row_value.decode())
                except:
                    d[columns[c]] = str(row_value)
            c += 1
        data.append(d)
    mysql_db.close_connection()
    
    config_file = "{}/".format(expanduser("~"))
    print(config_file)
    return render_template('index.html', name = 'Je Suis', menu_data = data, menu_columns = columns)
    #return jsonify(a = sequence)
    #return jsonify(a = data)

@app.route("/me/<string:yourname>/")
def me(yourname):
    return "The me route with {} argument".format(yourname)

@app.route("/calendar/")
def calendar():
    return render_template('calendar.html')

@app.route("/calendar_data/")
def calendar_data():
    print('here we go')
    events =[ {'title': 'All Day Event',
              'start': '2018-03-01'}
              ]

    return jsonify(events = events)

@app.errorhandler(Exception)
def code_error(e):
    print(e)
    return 'error {}'.format(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)