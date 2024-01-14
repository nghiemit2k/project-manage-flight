from flask import render_template, request, redirect, url_for, session, jsonify

import manageflight.dao
from manageflight import app, login, dao, admin
import utils
from flask_login import login_user, logout_user, login_required


@app.route("/")
def index():
    if session.get('ticket'):
        del session["ticket"]
    return render_template("index.html")


@login.user_loader
def user_load(user_id):
    return manageflight.dao.get_user_by_id(user_id=user_id)


@app.route('/register', methods=['get', 'post'])
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
                if not dao.add_user(name=name, username=username, password=password, email=email):
                    err_msg = "Tạo tài khoản thất bại"
                else:
                    return redirect(url_for('index'))
            else:
                err_msg = "Mật khẩu không chính xác"
        except Exception as ex:
            err_msg = 'Hệ thống đang xảy ra lỗi' + str(ex)
    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password) or dao.check_staff_login(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)
        else:
            err_msg = 'Username hoặc password không chính xác'
    return render_template("login.html", err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.check_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/bookTicket")
def book_ticket():
    return render_template("bookTicket.html", flight=dao.get_flight(),
                           ticket_class=dao.get_ticket_class(), ticket=utils.show_ticket_info(session.get('ticket')))


@app.route('/api/book_ticket', methods=["post"])
def show_ticket_information():
    data = request.json

    ticket = session.get('ticket')

    if ticket is None:
        ticket = {}

    ticket["ticket_class_name"] = data.get("ticket_class_name")
    ticket["flight_name"] = data.get("flight_name")
    ticket["quantity"] = data.get("quantity")

    ticket_class = dao.get_ticket_class(name=ticket["ticket_class_name"])
    ticket["quantity_seat"] = ticket_class[0].quantity_seat if ticket_class else 0

    foundTicket = dao.get_ticket(ticket["flight_name"], ticket["ticket_class_name"])
    ticket["price"] = foundTicket.base_price if foundTicket else 0
    ticket["discount"] = foundTicket.discount if foundTicket else 0

    session['ticket'] = ticket
    return utils.show_ticket_info(ticket)


@app.route("/api/pay", methods=["post"])
def payment():
    price = request.json.get("price")
    ticket = session.get("ticket")
    try:
        dao.add_receipt(ticket_class_name=ticket["ticket_class_name"],
                        flight_name=ticket["flight_name"], price=price,
                        quantity=ticket["quantity"])
    except Exception as ex:
        return jsonify({'status': 500, "err_msg": str(ex)})
    else:
        del session["ticket"]
        return jsonify({'status': 200})


@app.route('/sellTicket')
def sell_ticket():
    return render_template('sellTicket.html',
                           flight=dao.get_flight(), ticket_class=dao.get_ticket_class(),
                           ticket=utils.show_ticket_info(session.get("sellTicket")))


@app.route('/api/sell_ticket', methods=["post"])
def show_sell_ticket_info():
    data = request.json

    ticket = session.get('sellTicket')

    if ticket is None:
        ticket = {}

    ticket["ticket_class_name"] = data.get("ticket_class_name")
    ticket["flight_name"] = data.get("flight_name")

    ticket["quantity"] = 1
    ticket["quantity_seat"] = 0

    foundTicket = dao.get_ticket(ticket["flight_name"], ticket["ticket_class_name"])
    ticket["price"] = foundTicket.base_price if foundTicket else 0
    ticket["discount"] = foundTicket.discount if foundTicket else 0

    session['sellTicket'] = ticket
    return utils.show_ticket_info(ticket)


@app.route("/api/print_ticket", methods=["post"])
def print_ticket():
    price = request.json.get("price")
    ticket = session.get("sellTicket")
    try:
        dao.sell_ticket(ticket_class_name=ticket["ticket_class_name"],
                        flight_name=ticket["flight_name"], price=price,
                        quantity=1)
    except Exception as ex:
        return jsonify({'status': 500, "err_msg": str(ex)})
    else:
        del session["sellTicket"]
        return jsonify({'status': 200})


@app.context_processor
def common_response():
    return {

    }


if __name__ == '__main__':
    app.run(debug=True)
