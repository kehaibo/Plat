@echo off 
e:
cd \Python-L\Plat\devicecnt\
dir .
echo 'runserver'
set/p ip=inter ip:
set/p port=inter port:	
echo 'python manage.py runserver'  %ip%:%port%
python manage.py runserver  %ip%:%port%
pause