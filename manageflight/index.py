from flask import render_template, request, redirect, url_for
from manageflight import app, login
import utils
from flask_login import login_user, logout_user,login_required
from manageflight.admin import *
@app.route("/")
def index():
    return render_template("index.html")
@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)
@app.route('/register',methods=['get','post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        try:
            if password.strip().__eq__(confirm.strip()):


                utils.add_user(name=name, username=username, password=password, email=email)
                return redirect(url_for('index'))
            else:
                err_msg = 'mat khau khong dung'
        except Exception as ex:
            err_msg = 'He thong dang co loi: ' + str(ex)
    return render_template('register.html',err_msg=err_msg)
@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if (user):
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_msg = 'Username hoac password khong dung'
    return render_template("login.html", err_msg=err_msg)
@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = utils.check_login(username=username,password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')
if __name__ =='__main__':
    app.run(debug=True)