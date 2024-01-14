def show_ticket_info(ticket):
    flight_name, ticket_class_name, quantity, price, discount, quantity_seat = "", "", 1, 0, 0, 0
    if ticket:
        flight_name = ticket["flight_name"]
        ticket_class_name = ticket["ticket_class_name"]
        quantity = ticket["quantity"]
        price = ticket["price"]
        discount = ticket["discount"]
        quantity_seat = ticket["quantity_seat"]

    return {
        "flight_name": flight_name,
        "ticket_class_name": ticket_class_name,
        "quantity": quantity,
        "price": price,
        "discount": discount,
        "quantity_seat": quantity_seat
    }

