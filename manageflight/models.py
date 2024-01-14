import hashlib

from manageflight import db
# from enum import Enum as UserEnum
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, func, engine, MetaData
from sqlalchemy.orm import relationship, backref, mapped_column
from datetime import datetime
from enum import Enum as UserEnum
from manageflight import app
from flask_login import UserMixin
from flask_admin import Admin, AdminIndexView, expose


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    STAFF = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class ReceiptModel(db.Model):
    __abstract__ = True
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


class Flight(BaseModel):
    __tablename__ = 'flight'
    name = Column(String(50), nullable=False)
    pilot = Column(String(50), nullable=False)
    time_departure = Column(DateTime)
    time_flight = Column(DateTime)
    created_date = Column(DateTime, default=datetime.now())
    airport = relationship('Airport', secondary='flight_airport', lazy='subquery',
                           backref=backref('flight', lazy=True))
    tickets = relationship('Ticket', backref='flight', lazy=True)

    def __str__(self):
        return self.name

class Airport(BaseModel):
    __tablename__ = 'airport'
    departure_airport = Column(String(50))
    arrival_airport = Column(String(50))
    intermediate_airport = Column(String(50))
    stop_time = Column(Integer)
    created_date = Column(DateTime, default=datetime.now())


class ModelUser(UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name


class User(BaseModel, ModelUser):
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipt = relationship('Receipt', backref='user', lazy=True)


class Staff(BaseModel, ModelUser):
    user_role = Column(Enum(UserRole), default=UserRole.STAFF)
    receipt = relationship('ReceiptSell', backref='staff', lazy=True)
    calenders = relationship('FlightCalender', backref='staff', lazy=True)
    # sell_tickets = relationship('SellTicket', backref='staff',lazy=True)


class Ticket(BaseModel):
    __tablename__ = 'ticket'
    base_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    ticket_class_id = Column(Integer, ForeignKey('ticket_class.id'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    # sells = relationship('SellTicket',backref='ticket',lazy=True)
    # books = relationship('BookTicket',backref='ticket',lazy=True)
    receipt_details = relationship('ReceiptDetail', backref='ticket', lazy=True)
    receipt_details_sell = relationship('ReceiptDetailSell', backref='ticket', lazy=True)

    def __str__(self):
        return self.id


flight_airport = db.Table('flight_airport',
                          Column('flight_id', Integer, ForeignKey('flight.id'), primary_key=True),
                          Column('airport_id', Integer, ForeignKey('airport.id'), primary_key=True))


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(ReceiptModel):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False, primary_key=True)


class ReceiptSell(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    details = relationship('ReceiptDetailSell', backref='ReceiptSell', lazy=True)


class ReceiptDetailSell(ReceiptModel):
    t_sell_id = Column(Integer, ForeignKey(ReceiptSell.id), nullable=False, primary_key=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False, primary_key=True)


# class SellTicket(db.Model):
#     staff_id=Column( Integer, ForeignKey('staff.id'), primary_key=True),
#     ticket_id=Column(Integer, ForeignKey('ticket.id'), primary_key=True),
#     created_date = Column(DateTime, default=datetime.now())
#     quantity = Column(Integer, default=0)
#     unit_price = Column(Float, default=0)


class TicketClass(BaseModel):
    __tablename__ = 'ticket_class'
    name = Column(String(50), nullable=False)
    tickets = relationship('Ticket', backref='ticket_class', lazy=True)
    seat_type = Column(Integer, nullable=False)
    quantity_seat = Column(Integer, nullable=False)
    note = Column(String(50), nullable=True)

    def __str__(self):
        return self.name


class FlightCalender(BaseModel):
    __tablename__ = 'flight_calender'
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    note = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        u1 = User(name='User2', username='user2', password=hashlib.md5("123456".encode('utf-8')).hexdigest())
        t1 = Airport(departure_airport='tphcm', arrival_airport='ha noi', intermediate_airport='hue', stop_time=30)
        t2 = Airport(departure_airport='ha noi', arrival_airport='tphcm', intermediate_airport='hai phong',
                     stop_time=30)
        t13 = User(name='User1', username='user', password=hashlib.md5("123456".encode('utf-8')).hexdigest())
        t14 = User(name='Admin', username='admin', password=hashlib.md5("123456".encode('utf-8')).hexdigest(), user_role=UserRole.ADMIN)
        t3 = TicketClass(name='E class', seat_type=2, quantity_seat=1)
        t4 = TicketClass(name='M class', seat_type=2, quantity_seat=2)
        t5 = Flight(name='tphcm-hn', pilot='abc0', time_departure=datetime(2023, 12, 24),
                    time_flight=datetime(2023, 12, 24))
        t6 = Flight(name='hn-tphcm', pilot='abc0', time_departure=datetime(2023, 12, 24),
                    time_flight=datetime(2023, 12, 24))
        t7 = Ticket(base_price=30000, discount=0, start_date=None, end_date=None, ticket_class_id=1, flight_id=1)
        t8 = Ticket(base_price=500000, discount=100000, start_date=datetime(2023, 12, 23),
                    end_date=datetime(2023, 12, 25), ticket_class_id=1, flight_id=2)
        t12 = Ticket(base_price=50000, discount=0, start_date=None, end_date=None, ticket_class_id=2, flight_id=1)
        t11 = Ticket(base_price=700000, discount=100000, start_date=datetime(2023, 12, 23),
                    end_date=datetime(2023, 12, 25), ticket_class_id=2, flight_id=2)
        t9 = Receipt(user_id=2)
        t10 = ReceiptDetail(receipt_id=1, ticket_id=1, quantity=2, unit_price=300000)
        # db.session.add(u1)
        # db.session.add(t1)
        # db.session.add(t2)
        # db.session.add(t3)
        # db.session.add(t4)
        # db.session.add(t5)
        # db.session.add(t6)
        # db.session.add(t7)
        # db.session.add(t8)
        # db.session.add(t9)
        # db.session.add(t10)
        # db.session.add(t11)
        # db.session.add(t12)
        # db.session.add(t13)
        # db.session.add(t14)
        db.session.commit()
