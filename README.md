# python-demo-site
Simple Python web site: Flask, SQLAlchemy, SQLAlchemy.orm

First create MySql database named "python-demo-site"
    
Import MySql dump file located at ./databases/mysql.python-demo-site.sql

Change ./env file to meet your MySql database login parameters:

DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=*******
DB_NAME=python-demo-site

Run localhost server from Visual Code Terminal with:

python app.py

Open in browser: http://127.0.0.1:4949/
