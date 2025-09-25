def format_date(date_obj, format='%Y%m%d'):
    return date_obj.strftime(format)

def format_stock_code(code):
    if code.startswith('6'):
        return 'SH' + code
    elif code.startswith(('0', '3')):
        return 'SZ' + code
    return code
