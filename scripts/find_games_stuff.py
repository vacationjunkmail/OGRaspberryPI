#!/usr/bin/env python3

#/usr/local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection

console_id = 12
select_statement = '''select v.id,v.`name`,g.console_shortname 
			from games.video_games as v inner join games.game_console as g on g.id=v.console_id 
			where g.id = {} and (v.small_image ='' or v.large_image = '' or v.small_image is null or v.large_image is null);'''.format(console_id)
select_consoles = 'select console_shortname from games.game_console where id = {};'.format(console_id)
update_query = ''' update games.video_games set large_image=%s, small_image=%s where id = %s;'''
def stop_me():
	print("Planned exit Program did not finish!")
	sys.exit()
	return ''

script_name = os.path.abspath(__file__)

#path = '/var/www/blue_print_app/static/images'
path = '/var/www/public/images'

mysql_db = get_connection()
video_game_query = mysql_db.select_query(select_statement)
video_game_data = video_game_query.fetchall()
mysql_db.close_connection()

mysql_db = get_connection()
console_query = mysql_db.select_query(select_consoles)
console_data = console_query.fetchall()
mysql_db.close_connection()
sub_dir=['small','large']
nested_dict = {}
d = {}
for row in console_data:
	parent_dir = row[0]
	if isinstance(row[0], bytes):
		parent_dir = row[0].decode()
	#d = {}
	d[parent_dir]={}
	for item in sub_dir:
		d[parent_dir][item] = []
		search_path = "{}/{}/{}".format(path,parent_dir,item)
		#files = [f for f in os.listdir('./my_dir') if f.endswith('.txt')]
		files = [f for f in os.listdir(search_path)]# if f.endswith('.txt')]
		if len(files):
			#d[parent_dir][item].append(files)
			d[parent_dir][item]=files
for row in video_game_data:
	params = []
	print(row[1])
	if isinstance(row[1], bytes):
		image = row[1].decode().lower()
		system = row[2].decode()
	else:
		image = row[1].lower()
		system = row[2]
	image = image.replace(' ','')
	regex = re.compile(r'^{}\.'.format(image),re.IGNORECASE)
	small = [f for f in d[system]['small'] if regex.search(f)]
	large = [f for f in d[system]['large'] if regex.search(f)]
	print(small)
	s = ''
	l = ''
	if len(small):
		s = small[0]

	if len(large):
		l = large[0]

	if len(small) == 0 and len(large) == 0:
		continue
			
	params = [l,s,row[0]]
	mysql_db = get_connection()
	a = mysql_db.update_statement(update_query,params)
	print(a)
	mysql_db.close_connection()

