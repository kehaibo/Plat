#-*- coding:utf-8 -*-
import os

loglocal = str()

if os.name =='nt':
	logfilepath = os.path.abspath('.')
	loglocal =logfilepath+'\log\log.txt'
else:
	logfilepath = os.path.abspath('.')
	loglocal =logfilepath+'/log/log.txt'







