#!/usr/bin/env python3

from mysql_conn.connect_mysql import get_connection

import sys

title_len = 0
char_len = 0
title_name = ''
char_name = ''

mysql_db = get_connection()
find_title_query = '''select id from games.video_games where `name`= %s and console_id = %s;'''
find_character_query = '''select id from games.characters where name = %s;'''
new_title_insert = '''insert into games.video_games(name,console_id)values(%s,%s);'''
new_character_insert = '''insert into games.characters(name)values(%s);'''
video_character_insert = '''insert into games.video_game_and_characters(video_game_id,character_id)values(%s,%s);'''
delete_video_character = '''delete from games.video_game_and_characters where video_game_id = %s;'''
update_game_description = '''update games.video_games set game_description = %s where id = %s;'''

def _select(q,p):
	results = mysql_db.select_params(q,p)
	vid = 0
	if len(results[1]) > 0:
		vid = results[1][0]['id']
	return vid

def _error_mysql(e):
	print(e[0])
	print(e[1])
	mysql_db.close_connection()
	sys.exit()
	return ""

with open("/home/pi/Desktop/_games.txt") as f:
	for line in f:
		line = line.strip().split('|&|')
		title_console = line[0].split(',')
		title = title_console[0]
		console_id = title_console[1]
		title_params=[title,console_id]
		r = _select(find_title_query,title_params)
		game_id = int(r)
		print("Working on {}:".format(title))
		description_text = line[2]
		if len(description_text) == 0:
			print("{} has no description fix and re-run script.".format(title))
			sys.exit()
		if game_id == 0:
			print("\tInsert new game {}".format(title))
			r = mysql_db.insert_statement(new_title_insert,title_params)
			if r[0] == 'Error':
				_error_mysql(r)
			game_id = int(r[1])
		del_params = [game_id]
		u = mysql_db.update_statement(update_game_description,[description_text,game_id])
		d = mysql_db._delete(delete_video_character,del_params)
		characters = line[1].split(',')
		print("\tAdding Characters:")
		for item in characters:
			item = item.strip()
			char_params = [item]
			c_results = _select(find_character_query,char_params)
			character_id = int(c_results)
			if character_id == 0:
				print("\tNew character:{}".format(item))
				character_data = mysql_db.insert_statement(new_character_insert,char_params)
				if character_data[0] == 'Error':
					_error_mysql(character_data)
				character_id = int(character_data[1])
			else:
				print("\t{}".format(item))
			vgc_params = [game_id,character_id]
			mysql_db.insert_statement(video_character_insert,vgc_params)
mysql_db.close_connection()
