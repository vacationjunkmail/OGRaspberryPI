#!/usr/bin/env python3

#/usr/local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#https://stackoverflow.com/questions/247770/how-to-retrieve-a-modules-path
#vi /home/pi/.local/lib/python3.4/site-packages/mysql_conn/connect_mysql.py
#in_transaction
#https://overiq.com/mysql-connector-python-101/handling-transactions-with-connector-python/
import os, datetime, re, sys, time
from mysql_conn.connect_mysql import get_connection

doc = "/var/www/cal_app/scripts/game_and_characters.txt"

select_character = '''select id from games.characters where name = %s;'''
insert_video_game = ''' insert into games.video_games(name,console_id)values(%s,%s);'''
insert_character = ''' insert into games.characters(name)values(%s);'''
insert_game_and_character = '''insert into games.video_game_and_characters(video_game_id,character_id)values(%s,%s);'''

def _sql(_query,_param):
        mysql_db = get_connection()
        query_data = mysql_db.select_params(_query,_param)
        mysql_db.close_connection()
        return query_data

def _insert(_query,_params):
        mysql_db = get_connection()
        r = mysql_db.insert_statement(_query,_params)
        mysql_db.close_connection()
        return r

with open(doc,'r') as r:
	for row in r:
		row = row.strip()
		row = row.split('::')
		if len(row) != 2:
			print("The row does not have the correct amount of data length of :: is not 2")
			sys.exit()
		video_game_data = row[0].split('=')
		if len(video_game_data) != 2:
			print("The row does not have the correct amount of data length of = is not 1")
			sys.exit()
		params=[video_game_data[0],video_game_data[1]]
		results = _insert(insert_video_game,params)
		#print(results)
		try:
			game_id = results[1]
			characters_list = row[1].split(',')
			#print("{} id is {}".format(video_game_data[0],game_id))
			for character in characters_list:
				character = character.strip()
				param = [character]
				character_data = _sql(select_character,param)	
				if len(character_data[1])>0:
					character_id = character_data[1][0]['id']		
				else:
					param = [character]
					c_results = _insert(insert_character,param)
					character_id = c_results[1]
				params = [game_id,character_id]
				_insert(insert_game_and_character,params)
			print("{} is complete".format(video_game_data[0]))
		except Exception as e:
			print(e)

