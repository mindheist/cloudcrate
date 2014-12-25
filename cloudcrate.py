#!/usr/bin/python

# https://docs.python.org/2/library/os.html#os.listdir
# Getting Started with AWS - https://aws.amazon.com/articles/3998
# Introduction to boto - http://boto.cloudhackers.com/en/latest/
# How to Install boto  - http://stackoverflow.com/questions/2481287/how-do-i-install-boto
# https://ariejan.net/2010/12/24/public-readable-amazon-s3-bucket-policy/
# http://aws.amazon.com/code/Amazon-S3/1713

print """
   ____ _                 _      ____           _       
  / ___| | ___  _   _  __| |    / ___|_ __ __ _| |_ ___ 
 | |   | |/ _ \| | | |/ _` |   | |   | '__/ _` | __/ _ 
 | |___| | (_) | |_| | (_| |   | |___| | | (_| | ||  __/
  \____|_|\___/ \__,_|\__,_|    \____|_|  \__,_|\__\___|

  Usage : python cloudcrate.py
  ============================
  Available tasks:

	setup      ................ If you are using cloudcrate for the first time , Run 'cloudcrate setup' to install all dependencies.  
                                      command: python cloudcrate.py setup 
	sync       ................ Run Sync from the cloudcrate folder to sync to the cloud 
                                      command: python cloudcrate.py sync 
	download   ................ Run Download and all files are automatically downloaded to folder s3_downloads on the Desktop
                                      command: python cloudcrate.py download 
  """

import sys
import os
from datetime import datetime
from collections import defaultdict

try:
	task = str(sys.argv[1])

	#args = str(sys.argv[2])
except IndexError:
	print "Enter one of the above command line arguments "
	sys.exit(1)

if task == 'setup' :
	try:
		import boto
		print "=================================================================================="
		print "All required libraries have already been installed , proceed to sync"
		print "Please note, your current folder is your 'cloudcrate' copy files in this and sync "
		print "Example sync command          : python cloudcrate.py sync"
		print "For list of all commands,type : python cloudcrate.py  "
		print "=================================================================================="

	except ImportError,e:
		print "============================================================="
		raw_input("Missing Libraries - Press Hit Enter to Install them")

		print "============================================================="
		print "Installing boto - python interface to Amazon S3"
		print "============================================================="
		os.system("tar -zxvf boto.0.tar.gz")
		os.chdir("boto-2.34.0")
		os.system("sudo python setup.py install ")
		print "=================================================================================="
		print "All required libraries have been installed, proceed to sync "
		print "Please note, your current folder is your 'cloudcrate' copy files in this and sync "
		print "Example sync command : python cloudcrate.py sync"
		print "For list of all commands : python cloudcrate.py  "
		print "=================================================================================="

if task == 'sync' :


	from boto.s3.connection import S3Connection
	from boto.s3.key import Key
	import json
	import time
	from time import mktime
	from datetime import datetime
	from subprocess import call
	import os
	import subprocess


	print "Establish connection to AWS S3"

	conn = S3Connection('AKIAJHAZH5AVPWXOI4ZA', 'PG8BmISNsLWFN/8dZ8jBckmqU/Jq8nFJFVEORswL')
	bucket = conn.create_bucket('cloudcrate.hari')
	print "======================================"

	print "====== Syncing Current Directory ====="
	print "======================================"
	path = os.path.dirname(os.path.realpath('cloudcrate.py')) + '/'
	
	list_of_files = []
	creation_time_dict = {}



	for (path,dirs,l_of_f) in os.walk(path):
		for name in l_of_f:
			full_name = (os.path.join(path,name))
			#print "file fullname = ",  full_name
			list_of_files.append(full_name)
    	for name in dirs:
        	full_name = (os.path.join(path,name))
        	print "dir fullname =" ,full_name
        	#list_of_files.extend[full_name]
        	list_of_files.append(full_name)

	print "==========================================="
	print "====== The creation time of the files ====="
	print "==========================================="
	
	for files in list_of_files:
		command_to_run = str("mdls -name kMDItemFSCreationDate") + " " + files
		process = subprocess.Popen(command_to_run.split(), stdout = subprocess.PIPE)
		output = process.communicate()[0]
		creation_time_dict[files] = str(output)[24:28]

	print creation_time_dict
	
	json.dump(creation_time_dict, open("creation_time.txt",'w'))
		
	#print "======================================"
	#print "===== SOME LIST ======================"
	#print "======================================"

	#print list_of_files

	print "======================================"
	print "===== LIST OF FILES IN DIRECTORY======"
	print "======================================"

	print "the list object returned above is " , type(list_of_files)

	try:
		print "in try block - this would handle a resyn operation"
		print os.path.exists("last_modified.txt")
		last_modified_dict = json.load(open("last_modified.txt"))

		for files in list_of_files:
			#if not files.startswith('.'):
			#print 'Working on file ' ,files

			if (files not in last_modified_dict):
				last_modified_dict[files] = os.path.getmtime(files)
				#print "Missing file Added to dictionary is ", files
				print "uploading ..from try block if" , files
				k = Key(bucket)
				head, tail = os.path.split(files)
				k.key = tail
				#print "The key is " , k.key
				k.set_contents_from_filename(files)
				json.dump(last_modified_dict, open("last_modified.txt",'w'))

			elif (files in last_modified_dict) & (os.path.getmtime(files) > last_modified_dict[files]) :
				last_modified_dict[files] = os.path.getmtime(files)
				print "uploading ..from try block elif" , files
				k = Key(bucket)
				head, tail = os.path.split(files)
				k.key = tail
				print "The key is " , k.key
				k.set_contents_from_filename(files)
				json.dump(last_modified_dict, open("last_modified.txt",'w'))
				
			else :
				print "skipping file from try block else ",files

		bucket.set_acl('public-read')

	except IOError as e : 

		print e

		print "In IO exception block - There was no last_modified.txt file"
		last_modified_dict = defaultdict()
		for files in list_of_files:
			print "files = " , files
			#print "list of files = " , list_of_files
			last_modified_dict[files]= os.path.getmtime(files)
		print last_modified_dict
		json.dump(last_modified_dict, open("last_modified.txt",'w'))

		for files in list_of_files:
		   	#if not files.startswith('.'):
			print 'uploading file from IOError Exception' ,files
			k = Key(bucket)
			#k.key = files
			head, tail = os.path.split(files)
			k.key = tail
			print "The key is " , k.key
			k.set_contents_from_filename(files)

	bucket.set_acl('public-read')

	print "======================================================================="
	print "visit http://cloudcrate.hari.s3.amazonaws.com/list.html to take a look at the bucket & uploaded files"
	print "======================================================================="


if task == 'download' :	

	import json
	from boto.s3.connection import S3Connection
	from boto.s3.key import Key

	download_last_modified_dict = {}
	#conn = S3Connection('AKIAJ332D5S6IQ7WITSQ', 'G2WNp8xGxQPSxEcurBOTI32okS/izRmz2KPAJO24')
	conn = S3Connection('AKIAJHAZH5AVPWXOI4ZA', 'PG8BmISNsLWFN/8dZ8jBckmqU/Jq8nFJFVEORswL')
	bucket = conn.get_bucket('cloudcrate.hari')
	#os.mkdir('~/Desktop/downloaded/')

	file_types_list =[]
	creation_time_dict = {}
	creation_time_dict = json.load(open("creation_time.txt"))


	if not os.path.exists(os.path.expanduser('~/Desktop/s3_downloads')):
		print "===================================================="
		print "Looks like you havent downloaded the files even once"
		print "===================================================="
		os.mkdir(os.path.expanduser('~/Desktop/s3_downloads/'))
		print "Created a folder of name s3_downloads on your Desktop"
		print "===================================================="
		print set(creation_time_dict.values())
		print "===================================================="

		os.chdir(os.path.expanduser('~/Desktop/s3_downloads'))

		# for key in bucket.list():
		# 		download_last_modified_dict[key.name]= key.last_modified
		# 		#print key.name
				
		# 		#fileName, fileExtension = os.path.splitext(key.name)
		# 		#print "file extension ==", fileExtension ,"file Name==" , fileName
		# 		#print key.last_modified
		# 		#print fileExtension[1:]

		# 			try :
		# 				if not os.path.exists(fileExtension[1:]):

		# 			#print "inside loop that makes Directory based on fileEXT"
		# 					#os.makedirs(fileExtension[1:])
		# 					downloaded_file = key.get_contents_to_filename(key.name)
		# 					print "Downloaded file from the if code block" , key.name
		# 			except OSError as e:
		# 				continue
		# 				#os.chdir(fileExtension[1:])
		# 				downloaded_file = key.get_contents_to_filename(key.name)
		# 				print "Downloaded file from the if code block" , key.name
		

		for key in bucket.list():
				#print creation_time_dict[key.name]
				download_last_modified_dict[key.name]= key.last_modified
				downloaded_file = key.get_contents_to_filename(key.name)
				#print key.last_modified
				print "Downloaded file from fresh download code block " , key.name


				
		#print download_last_modified_dict
		json.dump(download_last_modified_dict, open("download_last_modified.txt",'w'))

	else:

		print "============================================================================================="
		print "the s3_downloads folder already exists , will now selectively download files into this folder"
		print "============================================================================================="

		os.chdir(os.path.expanduser('~/Desktop/s3_downloads'))
		download_last_modified_dict = json.load(open("download_last_modified.txt"))
		print "loaded json from file into memory and it looks like below", download_last_modified_dict
		
		# for key in download_last_modified_dict:
		# 	print download_last_modified_dict[key]

		# print type(bucket.list())
		# for key in bucket.list():
		# 	#print type(key)
		# 	print key.name, key.last_modified , download_last_modified_dict[key.name]

		#try:
		for key in bucket.list():
			try:
				if key.last_modified > download_last_modified_dict[key.name]:
					#print "from S3 " ,key.last_modified ,"from file", download_last_modified_dict[key.name]
					print "Downloading file based on timestamp comparison",key.name
					download_last_modified_dict[key.name]= key.last_modified
					downloaded_file = key.get_contents_to_filename(key.name)
				else:
					#print "Skipping download of file",key.name , "last updated time that I just read from S3",key.last_modified
					print "Skipping download of file",key.name
				json.dump(download_last_modified_dict, open("download_last_modified.txt",'w'))
			except KeyError as e :
				#print e
				#print "KeyError" , key.name
				downloaded_file = key.get_contents_to_filename(key.name)
				print "Downloaded in the KeyError code block",key.name
				download_last_modified_dict[key.name]=key.last_modified
				#fileName, fileExtension = os.path.splitext(downloaded_file)
				json.dump(download_last_modified_dict, open("download_last_modified.txt",'w'))

	print set(creation_time_dict.values())

	print "End of Download"		