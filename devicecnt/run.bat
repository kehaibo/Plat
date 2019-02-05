@echo off 
d:
cd \development\Plat-1\Plat\devicecnt\
dir .
echo 'runserver'
set/p ip=inter ip:
set/p port=inter port:	
python manage.py runserver  %ip%:%port%
echo 'python manage.py runserver'  %ip%:%port%
pause