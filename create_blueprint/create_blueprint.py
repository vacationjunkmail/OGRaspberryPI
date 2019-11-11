#!/usr/bin/env python3

import os
import sys
import re
from pathlib import Path
import argparse
from shutil import copyfile

parser = argparse.ArgumentParser(description="Will create basic Flask Blue Print")
parser.add_argument("-d","--dir", help="Please add the directory name")
parser.add_argument("-r","--route",help="Add your default route")

args = parser.parse_args()

#new_directory = "{}/{}".format(Path().absolute().parent,args.dir)
current_directory = Path().absolute()
new_directory = "{}/{}".format(Path().absolute(),args.dir)
bp_directory_list = ['templates','static','routes']
bp_files_list = ['app.py','uwsgi.ini','example_app.service','routes_file.py','templates_file.html']
port_file = "{}/port.txt".format(current_directory)
if not Path(new_directory).is_dir():
	
	with open(port_file, 'r') as f:
		line = f.readlines()
	
	port = int(line[-1].strip())+1

	os.mkdir(new_directory)
	for folder in bp_directory_list:
		if folder == 'templates':
			os.mkdir(new_directory+"/"+folder)
			os.mkdir(new_directory+"/"+folder+"/"+args.route)
		else:
			os.mkdir(new_directory+"/"+folder)
		#print("{}/{}".format(new_directory,folder))

	init_file = "{}/__init__.py".format(new_directory)
	
	with open(init_file,'a+') as f:
		f.write('')

	#copy files
	for file in bp_files_list:
		source = "{}/{}".format(current_directory,file)
		#source = Path(source)
		destination = "{}/{}".format(new_directory,file)
		#destination = Path(destination)
		#print("source = {}\n  dest= {}".format(source,destination))
		copyfile(source, destination)

	#replace in file
	for file in bp_files_list:
		file = "{}/{}".format(new_directory,file)
		with open(file) as f:
			fileData = f.read().replace('{route}',args.route).replace('{dir}',args.dir).replace('{port}',str(port))
		with open(file,"w+") as newfile:
			newfile.write(fileData)

	#Move files to location
	for file in bp_files_list:
		dir = file.split("_")
		if len(dir) > 0:
			dir = "{}/{}".format(new_directory,dir[0])
			d = Path(dir)
			if d.is_dir():
				f = file.replace("_file","")
				if f == "templates.html":
					d = "{}/{}".format(d,args.route)
					f = "{}.html".format(args.route)
				else:
					f = "{}.py".format(args.route)
				destination = "{}/{}".format(d,f)
				source = "{}/{}".format(new_directory,file)
				Path(source).rename(destination)
		if file == "uwsgi.ini":
			mv_uwsgi = "{}/{}".format(new_directory,file)
			to_uwsgi = "{}/{}.ini".format(new_directory,args.route)
			Path(mv_uwsgi).rename(to_uwsgi)
		if file == "example_app.service":
			mv_service = "{}/{}".format(new_directory,file)
			to_service = "{}/{}.service".format(new_directory,args.dir)
			Path(mv_service).rename(to_service)
		

	#append most recent port id to file
	port = "{}\n".format(port)
	with open(port_file,'a+') as f:
		f.write(port)
	print("New app {} created.\nLocation {}".format(args.dir,new_directory))
	
else:
	print("{} was not created.\nSeems like the app already exists\nlocation {}".format(args.dir,new_directory))
