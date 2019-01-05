from flask import Flask, jsonify, render_template, request
from db_conn.my_sql import get_connection
#from werkzeug.debug import DebuggedApplication
from os.path import expanduser

import os, datetime, re

from picamera import PiCamera
from time import sleep

app = Flask(__name__)
#app.wsgi_app = DebuggedApplication(app.wsgi_app,True)
app.debug = True

@app.route("/")
def hello():
    sequence = [0,1]
    while sequence[-1] < 9000:
        sequence.append(sequence[-2] + sequence[-1])
	
    mysql_db = get_connection()
    
    query = 'select * from site_info.web_apps;'

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
    return render_template('index.html', name = 'Je Suis', menu_data = data, menu_columns = columns)
    #return jsonify(a = sequence)
    #return jsonify(a = data)

@app.route("/me/<string:yourname>/")
def me(yourname):
    return "The me route with {} argument".format(yourname)

@app.route("/calendar/")
def calendar():
    return render_template('calendar.html')
    #return render_template('json.html')

@app.route("/cal_test/")
def cal_test():
    return render_template('cal_test.html')

@app.route("/calendar_data/")
def calendar_data():
    
    events = []
    d_ = {}
    d_['title']='Beans'
    d_['start']='2018-03-01'
    events.append(d_)

    d_ = {}
    d_['title'] = 'Greens'
    d_['start'] = '2018-11-01'
    events.append(d_)

    
    return jsonify(data = events)
    #return jsonify({'teest':'nothing'})
    #return jsonify({'events':events})

@app.route("/pythonscripts/")
def pythonscripts():

    mysql_db = get_connection()
    query = 'select id,`name`,"" as script from pythonscripts.scripts;'
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
                    if columns[c] == 'script':
                       script_name = d['name'].split("/")
                       d[columns[c]] = script_name[-1]
                except:
                    d[columns[c]] = str(row_value)
            c += 1
        data.append(d)
    mysql_db.close_connection()
    return render_template("pythonscripts.html",menu_data = data, menu_columns = columns)

@app.route('/runscript/')
def runscript():
	
	os.system("python3 /home/pi/code/python/test.py")
	print('runscript route')
	return 'aaa'

@app.route('/camera/')
def camera():
		
	if len(request.args):
		
		my_time = datetime.datetime.now()
		image_directory = "{}/static".format(os.getcwd())
		image_name = '_image.jpg';
		
		#removes file if exists
		check_file_exists(image_directory,image_name)
		
		image_name = "{}{}".format(int(my_time.timestamp()),image_name)
		#print('{}/{}'.format(image_directory,image_name))
		
		pic_time = str(my_time.strftime('%A %B %-d %Y %-I:%M:%S %p'))
		image_name = "{}/{}".format(image_directory,image_name)
		
		camera = PiCamera(resolution=(1280, 720))
		sleep(10)
		#camera.annotate_text = pic_time
		#camera.start_preview()
		
		camera.capture(image_name)
		#camera.stop_preview()
		camera.close()
		
		image_name = image_name.split('/')
		image_name = "/".join(image_name[-2:])
		
		data = []
		data.append({'photo':image_name})
		data.append({'name':pic_time})

		#return jsonify({'photo':image_name})
		return jsonify(data = data)
	else:	
		return render_template("camera.html")
		
@app.errorhandler(Exception)
def code_error(e):
    print(e)
    return 'error {}'.format(e)

def check_file_exists(d,e):
	
	#e = '_{}.jpg'.format(e)
	
	text_files = [f for f in os.listdir(d) if f.endswith(e)]
	
	for file in text_files:
		os.remove("{}/{}".format(d,file))	
		
	return ''
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
