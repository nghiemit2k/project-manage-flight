from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.secret_key = '@#djjdjdjd$%^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/manageflight?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
admin = Admin(app=app, name='ADMIN',template_mode='bootstrap4')