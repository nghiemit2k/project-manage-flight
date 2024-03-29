from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = '@#djjdjdjd$%^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/manageflight?charset=utf8mb4' % quote(
    "Admin@123")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
