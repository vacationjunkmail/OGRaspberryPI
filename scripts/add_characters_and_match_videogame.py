#!/usr/bin/env python3

#/usr/local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection

select_character = '''select id,name from games.characters where name = %s;'''
insert_characters_statement = ''' insert into games.characters(name)values(%s);'''
insert_video_game_and_characters = '''insert into games.video_game_and_characters(video_game_id,character_id)values(%s,%s); '''

def stop_me():
	print("Planned exit Program did not finish!")
	sys.exit()
	return ''

script_name = os.path.abspath(__file__)

file = '/var/www/cal_app/scripts/add_characters_and_match_videogame.txt'

def _sql(_query,_param):
	mysql_db = get_connection()
	query_data = mysql_db.select_params(_query,_param)
	mysql_db.close_connection()
	return query_data

def _insert(_query,_params):
	mysql_db = get_connection()
	r = mysql_db.insert_statement(_query,_params)
	mysql_db.close_connection()
	print(r)
	return ''

with open(file,'r+') as f:
	for row in f:
		row = row.strip()
		if len(row)>0:
			row = row.split(':')
			id = row[0]
			data = row[1].split(',')
			for item in data:
				param = [item.strip()]
				query_data = _sql(select_character,param)

				if len(query_data[1])>0:
					character_id = query_data[1][0]['id']
					params = [id,character_id]
					_insert(insert_video_game_and_characters,params)
				else:
					param = [item.strip()]
					_insert(insert_characters_statement,param)
					query_data = _sql(select_character,param)
					if len(query_data[1])>0:
						character_id = query_data[1][0]['id']
						params = [id,character_id]
						_insert(insert_video_game_and_characters,params)
stop_me()
