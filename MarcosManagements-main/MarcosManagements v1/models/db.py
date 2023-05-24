from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#instance = "sqlite:///marcosmanagements"
instance = "mysql+pymysql://marcosmanagements:123@localhost:3306/marcosmanagements"