import datetime
import simplejson as json 

def generate_order_num(pk):
    current_data = datetime.datetime.now().strftime("%Y%m%d%H%M")
    order_number = current_data + str(pk)
    return order_number


def order_total_by_vendor(order,vendor_id):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor_id))
    subtotal = 0
    tax = 0
    tax_dict = {}
    
    for vendor_id, vendor_data in total_data.items():
        for price, tax_data in vendor_data.items():
            subtotal += float(price)
            tax_data = tax_data.replace("'", '"')
            tax_data = json.loads(tax_data)
            tax_dict.update(tax_data)

            for currency, tax_info in tax_data.items():
                for tax_rate, tax_amount in tax_info.items():
                    tax += float(tax_amount)

        grand_total = float(subtotal) + float(tax)
        return {
            "grand_total": grand_total,
            "subtotal": subtotal,
            "tax": tax,
            "tax_dict": tax_dict,
        }