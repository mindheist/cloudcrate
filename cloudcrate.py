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

	setup      ................ Run 'cloudcrate setup' first to setup AWS keys. 
                                      Example: python cloudcrate.py setup 
	sync       ................ Run Sync from the desired folder to sync to the cloud 
                                      Example: python cloudcrate.py sync 
	schedule   ................ Run schedule to cron sync and download every 90 mins
	download   ................ Run Download followed by destination folder name 
                                      Example: python cloudcrate.py download <destination_folder_name>
 
  """

import sys
import os
from datetime import datetime
import pip
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
		print "===================================================================="
		print "All required libraries have already been installed , procced to sync"
		print "===================================================================="

	except ImportError,e:
		print "============================================================="
		raw_input("Missing Libraries - Press Hit Enter to Install them")

		print "============================================================="
		print "Installing boto - python interface to Amazon S3"
		print "============================================================="
		os.system("tar -zxvf boto.0.tar.gz")
		os.chdir("boto-2.34.0")
		os.system("sudo python setup.py install ")
		print "============================================================="
		print "All required libraries have been installed , procced to sync "
		print "============================================================="



if task == 'sync' :


	from boto.s3.connection import S3Connection
	from boto.s3.key import Key
	import json
	import time
	from time import mktime
	from datetime import datetime


	conn = S3Connection('AKIAJ332D5S6IQ7WITSQ', 'G2WNp8xGxQPSxEcurBOTI32okS/izRmz2KPAJO24')
	bucket = conn.create_bucket('cloudcrate.hari')
	print "======================================"

	print "====== Syncing Current Directory ====="
	path = os.path.dirname(os.path.realpath('cloudcrate.py')) + '/'
	
	list_of_files = {}

	for (path,dirs,list_of_files) in os.walk(path):
		#print list_of_files
		break

	print "======================================"
	print "===== LIST OF FILES IN DIRECTORY======"
	print "======================================"

	print type(list_of_files)

	try:
		print "in try block - this would handle a resyn operation"
		print os.path.exists("last_modified.txt")
		last_modified_dict = json.load(open("last_modified.txt"))

		for files in list_of_files:
			if not files.startswith('.'):
				#print 'Working on file ' ,files

				if (files not in last_modified_dict):
					last_modified_dict[files] = os.path.getmtime(files)
					#print "Missing file Added to dictionary is ", files
					print "uploading ..from try block if" , files
					k = Key(bucket)
					k.key = files
					k.set_contents_from_filename(path+files)
					json.dump(last_modified_dict, open("last_modified.txt",'w'))

				elif (files in last_modified_dict) & (os.path.getmtime(files) > last_modified_dict[files]) :
					print "uploading ..from try block elif" , files
					k = Key(bucket)
					k.key = files
					k.set_contents_from_filename(path+files)
				
				else :
					print "skipping file from try block else ",files


		bucket.set_acl('public-read')


	except IOError: 

		print "in exception block"
		last_modified_dict = defaultdict()
		for files in list_of_files:
			last_modified_dict[files]= os.path.getmtime(files)
		print last_modified_dict
		json.dump(last_modified_dict, open("last_modified.txt",'w'))

		for files in list_of_files:
		   	if not files.startswith('.'):
				print 'uploading file from IOError Exception' ,files
				k = Key(bucket)
				k.key = files
				k.set_contents_from_filename(path+files)

	bucket.set_acl('public-read')

	print "======================================================================="
	print "visit http://cloudcrate.hari.s3.amazonaws.com/list.html to take a look at the bucket & uploaded files"
	print "======================================================================="


if task == 'download' :	

	import json
	from boto.s3.connection import S3Connection
	from boto.s3.key import Key

	download_last_modified_dict = {}
	conn = S3Connection('AKIAJ332D5S6IQ7WITSQ', 'G2WNp8xGxQPSxEcurBOTI32okS/izRmz2KPAJO24')
	bucket = conn.get_bucket('cloudcrate.hari')
	#os.mkdir('~/Desktop/downloaded/')

	if not os.path.exists(os.path.expanduser('~/Desktop/s3_downloads')):
		os.mkdir(os.path.expanduser('~/Desktop/s3_downloads/'))
	#path = '/tmp/s3_downloads/' + str(datetime.now())
	#os.mkdir(path)
	os.chdir(os.path.expanduser('~/Desktop/s3_downloads')) 
	#print "for this instance of download , the following folder has been created ",path
	print "==============================================================================="
	print "starting file download from S3 Bucket",bucket
	print "==============================================================================="
	
	for key in bucket.list():
	     try:
	     	download_last_modified_dict[key.name] = key.last_modified
	     	downloaded_file = key.get_contents_to_filename(key.name)
	     	print "Downloaded file",key.name 
	     	#list_of_downloaded_files.extend[key.name]
	     	#print "the creation time of this files is " , os.path.getctime(key.name)
	     except:
	      	print "FAILED"

	#print download_last_modified_dict
	json.dump(download_last_modified_dict, open("download_last_modified.txt",'w'))
	print "==============================================================================="
	print "all files have been downloaded to a folder of name s3_downloads on your desktop"
	print "==============================================================================="



#if task == 'schedule' :
	


# import os
# path = '/Users/Hari/modashboard'
# list_of_files = os.listdir(path)
# print path
# #print list_of_files
# # The above line was used only to debug , it prints a list containing all the files 
# print "======================================"
# print "===== LIST OF FILES IN DIRECTORY======"
# print "======================================"

# for files in list_of_files:
# 	print path+'/'+files
# 	scp path+'/'+files root@10.115.129.228:/cloudcrate/