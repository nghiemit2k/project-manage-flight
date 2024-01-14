from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_login import current_user, logout_user

from manageflight import db, app, dao
from flask_admin.contrib.sqla import ModelView
from manageflight.models import Flight, FlightCalender, TicketClass, Ticket, Receipt, Airport, User, UserRole
from flask import redirect, session, request


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='ADMIN', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class TicketView(AuthenticatedAdmin):
    column_list = ["id", "base_price", "discount", "start_date", "end_date",
                   "ticket_class_id", "ticket_class_name", "flight_id", "flight_name"]

    column_formatters = {
        "flight_name": lambda v, c, m, p: m.flight.name,
        "ticket_class_name": lambda v, c, m, p: m.ticket_class.name
    }


class FlightView(AuthenticatedAdmin):
    column_list = ["id", "name", "pilot", "time_departure", "time_flight", "created_date"]


class FlightCalendarView(AuthenticatedAdmin):
    column_list = ["id", "flight_name", "staff_name", "note", "created_date", "is_active"]

    column_formatters = {
        "flight_name": lambda v, c, m, p: m.flight.name,
        "staff_name": lambda v, c, m, p: m.staff.name,
    }


class TicketClassView(AuthenticatedAdmin):
    column_list = ["id", "name", "seat_type", "quantity_seat", "note"]


class ReceiptView(AuthenticatedAdmin):
    column_list = ["id", "created_date", "user_id"]


class AirportView(AuthenticatedAdmin):
    column_list = ["id", "departure_airport", "arrival_airport", "intermediate_airport", "stop_time", "created_date"]


class UserView(AuthenticatedAdmin):
    column_list = ["id", "name", "username", "password", "email", "active", "joined_date", "user_role"]


class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        month = request.args.get("month")
        return self.render('admin/stats.html',
                           mon_stats=dao.revenue_mon_stats(month if month else 1),
                           month=month)


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(FlightView(Flight, db.session))
admin.add_view(FlightCalendarView(FlightCalender, db.session))
admin.add_view(TicketClassView(TicketClass, db.session))
admin.add_view(TicketView(Ticket, db.session))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))