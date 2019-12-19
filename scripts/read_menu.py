#!/usr/bin/env python3

#/usr/local/lib/python4.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection

insert_query = '''insert into dinner.menu(`date`,`title`)values(%s,%s);'''
insert_error = '''insert into error_db.error_log(error_message,data,file_source,script_source)values(%s,%s,%s,%s)'''

insert_query = '''insert into dinner.menu_2(`title`,`start_date`,end_date)values(%s,%s,%s);'''

def stop_me():
	print("Planned exit Program did not finish!")
	sys.exit()
	return ''


mysql_db = get_connection()

script_name = os.path.abspath(__file__)

path = '/home/pi/Downloads/'

date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}',re.IGNORECASE)
error_regex = re.compile(r'^error message',re.IGNORECASE)
transaction_regex = re.compile(r'transaction',re.IGNORECASE)
def get_data(data):
	return_data = []
	title = ''
	dates_list = []	
	for k,v in enumerate(data):
		if date_regex.fullmatch(v):
			v = datetime.datetime.strptime(v,'%Y-%m-%d')
			my_date = v
			dates_list.append(v)
		else:
			title = v
	return_data.append(title)
	if dates_list[0] <= dates_list[1]:
		for item in dates_list:
			return_data.append(item)
	else:
		for item in reversed(dates_list):
			return_data.append(item)
	return return_data 

for file in os.listdir(path):
	error_list = []
	if file.endswith("menu.txt"):
		remove_file = os.path.join(path, file)
		with open(os.path.join(path, file),'r+') as f:
			data = f.readlines()
		for line in data:
			line = line.replace("\n","").split(":")
			if len(line) == 3:
				params = get_data(line)
				response = mysql_db.insert_statement(insert_query,params)
				response = str(response)
				if error_regex.search(response):
					line = ":".join(line)
					error_params=[response,line,remove_file,script_name]
					error_insert = mysql_db.insert_statement(insert_error,error_params)
					if error_regex.search(error_insert):
						error_list.append(error_insert)
		if len(error_list)>0:
			print("Not deleted because of errors\n\t{}".format(remove_file))
		else:
			os.remove(remove_file)
	if file.endswith("infile.txt"):
		load_data_infile = '/home/pi/Downloads/load_data_infile.txt'
	
		#code = "LOAD DATA LOCAL-INFILE '{}' INTO TABLE test_db.test_tbl FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\n'".format(load_data_infile)
		#print(code)
		code = "load data local infile '{}' into table test_db.test_tbl fields terminated by ',' optionally enclosed by '\"' lines terminated by '\\n' (id,username,pwd);"
		#print(code)
		#mysql_db.load_data_infile(code)	
mysql_db.close_connection()
stop_me()
q = mysql_db.select_query('''select id,`date`,title from dinner.menu order by `date`;''')
q = q.fetchall()
menu_start_dict = {}
menu_end_dict = {}
for recordset in q:
	title = str(recordset[2].decode())
	title = title.strip().replace('&','#amp;')
	date = recordset[1]
	year_month = date.strftime("%Y_%b")

	if year_month in menu_start_dict and title in menu_start_dict[year_month]:
		#menu_end_dict[year_month] = {title:date}
		menu_end_dict[year_month][title] = date
	else:
		if year_month in menu_start_dict:
			menu_start_dict[year_month][title] = date
			menu_end_dict[year_month][title] = date
		else:
			menu_start_dict[year_month] = {}
			menu_end_dict[year_month] = {}
			menu_start_dict[year_month][title] = date
			menu_end_dict[year_month][title] = date			

	#with open('/home/pi/Desktop/merged_data.txt','a+') as f:
	#	f.write("{} {}\n".format(recordset[1],t))

#for key_one in menu_start_dict:
#	for key_two in menu_start_dict[key_one]:
#		#print("title = {}\tstart date = {}\tend date = {}".format(key_two,menu_start_dict[key_one][key_two],menu_end_dict[key_one][key_two]))
#		params = [key_two,menu_start_dict[key_one][key_two],menu_end_dict[key_one][key_two]]
#		response = mysql_db.insert_statement(insert_menu2_query,params)
#		print("{}\n\t{}".format(response,params))
#mysql_db.close_connection()
