from datetime import date
from dateutil.relativedelta import relativedelta


now = date.today()
one_month_later = now + relativedelta(months=1)

# print(f"한달 후\ndate({one_month_later.year}, {one_month_later.month}, {one_month_later.day})")

# 만료 일정 (위의 출력 후 결정)
# expiration_date = date(2024, 12, 17)