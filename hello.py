from flask import Flask, jsonify, render_template, request, g, session, flash, redirect,url_for
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
app.config['SECRET_KEY'] = 'MoneyGrowsOnTrees'
csrf.init_app(app)

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
    #client_flags=[ClientFlag.LOCAL_FILES])
    #load data local infile '' into table test_db.test_tbl fields terminated by ',' optionally enclosed by '"' lines terminated by '\n' (id,username,pwd);
    load_file = '''load data local infile '{}' into table test_db.test_tbl fields terminated by ',' optionally enclosed by '\"' lines terminated by '\\n' (id,username,pwd);'''.format('/home/pi/Downloads/load_data_infile.txt')
    
    return render_template('index.html', name = 'Je Suis', menu_data = data, menu_columns = columns)

@app.route("/me/<string:yourname>/")
def me(yourname):
    return "The me route with {} argument".format(yourname)

@app.route("/calendar/")
def calendar():
    return render_template('calendar.html')

@app.route("/calendar_data/")
def calendar_data():
    #print(request.headers)
    events = []
    date_split = request.args['date'].split('/')
    params = [int(date_split[1]),int(date_split[0])]
    
    query = '''select `start_date` as start, `end_date` as end, `title` 
				from dinner.menu_2 where month(`start_date`) = ? and year(`start_date`) = ?
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

@app.route('/calendar/add/', methods = ['POST'])
def add_item():
	print('adding itme')
	return 'nothing'

@app.route('/calendar/login/', methods = ['GET'])
def login():
	
	#insert_query = '''insert into test_db.test_tbl(username,pwd)values(%s,%s);'''

	#for num in range(1,2):
		#username = "dana_{}".format(num)
		#pwd = "pwd_{}".format(num)
		#params = [username,pwd]
		
		#return_msg = g.mysql_db.insert_statement(insert_query,params)
		#print(return_msg)
		
		#print(params)
	
	if not session.get('logged_in'):
		#flash('wrong username/password!')
		return render_template('login.html')
	else:
		return 'here'#calindex()


@app.route('/calendar/login_check/', methods = ['POST'])
def login_check():
	print(request.form)
	try:
		query = 'select id,username from auth_users.users where username = %s and pwd = %s;'
		params = [request.form['username'],request.form['password']]
		
		data = g.mysql_db.select_params(query,params)
		if len(data[1]) == 1:
			print(data[1][0]['username'])
			print(data[1][0]['id'])
		else:
			flash('wrong username/password!','error')
			#return render_template('login.html')
			#return login()
			return redirect(url_for('login'))
			
	except Exception as e:
		print(e)
		print("asdf-------------------------------")
	
	return'no'

@app.route('/calendar/index/', methods =['GET'])
def calindex():
	if not session.get('logged_in'):
		return render_template('login.html')
	
	return render_template('calindex.html')
		
@app.errorhandler(500)
def handle_csrf_error(e):
    print("an error happened\n\t{}".format(e))
    
    return 'error {}'.format(e)

def check_file_exists(d,e):
	
	#e = '_{}.jpg'.format(e)
	
	text_files = [f for f in os.listdir(d) if f.endswith(e)]
	
	for file in text_files:
		os.remove("{}/{}".format(d,file))	
		
	return ''
	
if __name__ == "__main__":
    app.run(host =  '0.0.0.0', debug = True)
