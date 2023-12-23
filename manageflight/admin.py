from manageflight import  db,app,utils,admin
from flask_admin.contrib.sqla import ModelView
from manageflight.models import Flight,FlightCalender,TicketClass,Ticket,Receipt
from flask import redirect
class MyModelView(ModelView):
    column_display_pk = True
    column_exclude_list = ()


admin.add_view(ModelView(Flight,db.session))
admin.add_view(ModelView(FlightCalender, db.session))
admin.add_view(ModelView(TicketClass, db.session))
admin.add_view(MyModelView(Ticket, db.session))
admin.add_view(ModelView(Receipt, db.session))