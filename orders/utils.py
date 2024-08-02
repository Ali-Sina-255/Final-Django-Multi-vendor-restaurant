import datetime


def generate_order_num(pk):
    current_data = datetime.datetime.now().strftime("%Y%m%d%H%M")
    order_number = current_data + str(pk)
    return order_number
