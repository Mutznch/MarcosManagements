@echo off
:start
cls

python -m pip install flask
python -m pip install flask-login
python -m pip install flask-sqlalchemy
python -m pip install flask-bootstrap
python -m pip install werkzeug
python -m pip install virtualenv
python -m pip install pymysql
python -m pip install paho-mqtt

pause
exit
