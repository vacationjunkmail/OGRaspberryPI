from flask import Flask, jsonify, render_template, request, g
from flask_wtf.csrf import CSRFProtect, CSRFError
#from flask_wtf import Form
from db_conn.my_sql import get_connection
#from werkzeug.debug import DebuggedApplication
from os.path import expanduser

import os, datetime, re

from picamera import PiCamera
from time import sleep

csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'MoneyGrowsOnTrees'

#app.wsgi_app = DebuggedApplication(app.wsgi_app,True)
#app.debug = True

@app.before_request
def before_request():
	g.mysql_db = get_connection()
		
@app.after_request
def after_request(resp):
	g.mysql_db.close_connection()
	return resp
	
@app.route("/")
def hello():
    sequence = [0,1]
    while sequence[-1] < 9000:
        sequence.append(sequence[-2] + sequence[-1])
    
    query = 'select * from site_info.web_apps;'

    query = g.mysql_db.select_query(query)
    
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
           
    config_file = "{}/".format(expanduser("~"))
    return render_template('index.html', name = 'Je Suis', menu_data = data, menu_columns = columns)

@app.route("/me/<string:yourname>/")
def me(yourname):
    return "The me route with {} argument".format(yourname)

@app.route("/calendar/")
def calendar():
    return render_template('calendar.html')

@app.route("/calendar_data/")
def calendar_data():
    print(request.headers)
    events = []
    cal_month = request.args['date'].split('/')
    params = [int(cal_month[1])]
    query = '''select `date` as start, `date` as end, `title` 
				from dinner.menu where month(`date`) = ?
			'''    
    
    data = g.mysql_db.select_params(query,params)
    
    return jsonify(data = data[1])

@app.route("/pythonscripts/")
def pythonscripts():

    query = 'select id,`name`,"" as script from pythonscripts.scripts;'
    query = g.mysql_db.select_query(query)
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

@app.route('/calendar/add/')
def add_item():
	return 'nothing'
		
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
    app.run(host =  '0.0.0.0', debug = True)
