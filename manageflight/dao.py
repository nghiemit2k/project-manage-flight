import hashlib
from flask_login import current_user
from sqlalchemy import func
from manageflight import db
from manageflight.models import Flight, TicketClass, Ticket, Receipt, ReceiptDetail, User, ReceiptSell, \
    ReceiptDetailSell, Staff


def get_flight(id=None, name=None):
    flight = db.session.query(Flight)

    if id is not None:
        flight = flight.filter(Flight.id.__eq__(id))

    return flight.all()


def get_ticket_class(id=None, name=None):
    ticketClass = db.session.query(TicketClass)

    if id is not None:
        ticketClass = ticketClass.filter(TicketClass.id.__eq__(id))

    if name is not None:
        ticketClass = ticketClass.filter(TicketClass.name.__eq__(name))

    return ticketClass.all()


def get_ticket(flight_name=None, ticket_class_name=None):
    flight_id, ticket_class_id = 0, 0
    if flight_name and Flight.query.filter(Flight.name.__eq__(flight_name)).first():
        flight_id = Flight.query.filter(Flight.name.__eq__(flight_name)).first().id

    if ticket_class_name and TicketClass.query.filter(TicketClass.name.__eq__(ticket_class_name)).first():
        ticket_class_id = TicketClass.query.filter(TicketClass.name.__eq__(ticket_class_name)).first().id

    return Ticket.query.filter(Ticket.flight_id.__eq__(flight_id), Ticket.ticket_class_id.__eq__(ticket_class_id)).first()


def count_customer_profit(month=1):
    return (db.session.query(func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))
            .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))
            .filter(func.extract("month", Receipt.created_date).__eq__(month))).first()


def count_staff_profit(month=1):
    return (db.session.query(func.sum(ReceiptDetailSell.quantity * ReceiptDetailSell.unit_price))
            .join(ReceiptSell, ReceiptSell.id.__eq__(ReceiptDetailSell.t_sell_id))
            .filter(func.extract("month", ReceiptSell.created_date).__eq__(month))).first()


def revenue_mon_stats(month=1, year=2024):
    query = (db.session.query(Flight.name,
                              func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price),
                              func.count(Flight.name),
                              func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price)
                              / (count_customer_profit(month)[0]) * 100)
                              .join(Ticket, Ticket.flight_id.__eq__(Flight.id))
                              .join(ReceiptDetail, ReceiptDetail.ticket_id.__eq__(Ticket.id))
                              .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))
                              .filter(func.extract('month', Receipt.created_date).__eq__(month),
                                      func.extract('year', Receipt.created_date).__eq__(year))
                              .group_by(Flight.name))
    return query.all()


def add_receipt(flight_name, ticket_class_name, quantity, price):
    r = Receipt(user=current_user)
    db.session.add(r)
    flight_id = get_flight(name=flight_name)[0].id
    ticket_class_id = get_ticket_class(name=ticket_class_name)[0].id
    foundTicket = Ticket.query.filter(Ticket.flight_id.__eq__(flight_id),
                                          Ticket.ticket_class_id.__eq__(ticket_class_id)).first()
    if foundTicket:
        d = ReceiptDetail(receipt=r, ticket=foundTicket, quantity=quantity, unit_price=price)
        db.session.add(d)

    db.session.commit()


def add_user(name, username, password, **kwargs):
    if password is not None:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    if User.query.filter(username=username).first():
        return False
    else:
        user = User(name=name.strip(), username=username.strip(), password=password, email=kwargs.get('email'))
        db.session.add(user)
        db.session.commit()
        return True


def sell_ticket(flight_name, ticket_class_name, quantity, price):
    rs = ReceiptSell(staff_id=current_user.id)
    db.session.add(rs)
    flight_id = get_flight(name=flight_name)[0].id
    ticket_class_id = get_ticket_class(name=ticket_class_name)[0].id
    foundTicket = Ticket.query.filter(Ticket.flight_id.__eq__(flight_id),
                                      Ticket.ticket_class_id.__eq__(ticket_class_id)).first()
    if foundTicket:
        d = ReceiptDetailSell(ReceiptSell=rs, ticket=foundTicket, quantity=quantity, unit_price=price)
        db.session.add(d)

    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()


def check_staff_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return Staff.query.filter(Staff.username.__eq__(username.strip()), Staff.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)
