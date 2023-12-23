from manageflight import app,db
from manageflight.models import  User
import hashlib

def add_user(name,username,password, **kwargs):
    if password is not None:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username.strip(), password=password, email=kwargs.get('email'))
    db.session.add(user)
    db.session.commit()
def check_login(username,password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),User.password.__eq__(password)).first()
def get_user_by_id(user_id):
    return User.query.get(user_id)
