from manageflight import db, app, utils, admin
from flask_admin.contrib.sqla import ModelView
from manageflight.models import Flight, FlightCalender, TicketClass, Ticket, Receipt, Airport, User
from flask import redirect


class FlightView(ModelView):
    column_list = ["id", "name", "pilot", "time_departure", "time_flight", "created_date"]


class FlightCalendarView(ModelView):
    column_list = ["id", "flight_name", "staff_name", "note", "created_date", "is_active"]

    column_formatters = {
        "flight_name": lambda v, c, m, p: m.flight.name,
        "staff_name": lambda v, c, m, p: m.staff.name,
    }


class TicketClassView(ModelView):
    column_list = ["id", "name", "seat_type", "quantity_seat", "note"]


class TicketView(ModelView):
    column_list = ["id", "base_price", "discount", "start_date", "end_date", "ticket_class_name", "flight_name"]

    column_formatters = {
        "flight_name": lambda v, c, m, p: m.flight.name,
        "ticket_class_name": lambda v, c, m, p: m.ticket_class.name
    }


class ReceiptView(ModelView):
    column_list = ["id", "created_date", "user_id"]


class AirportView(ModelView):
    column_list = ["id", "departure_airport", "arrival_airport", "intermediate_airport", "stop_time", "created_date"]


class UserView(ModelView):
    column_list = ["id", "name", "username", "password", "email", "active", "joined_date", "user_role"]


admin.add_view(FlightView(Flight, db.session))
admin.add_view(FlightCalendarView(FlightCalender, db.session))
admin.add_view(TicketClassView(TicketClass, db.session))
admin.add_view(TicketView(Ticket, db.session))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(UserView(User, db.session))
