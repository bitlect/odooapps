from datetime import datetime
from dateutil import relativedelta


def months_between(start_date, end_date):
    date1 = datetime.strptime(str(start_date), '%Y-%m-%d  %H:%M:%S')
    date2 = datetime.strptime(str(end_date), '%Y-%m-%d  %H:%M:%S')
    return (date2.year - date1.year) * 12 + date2.month - date1.month
