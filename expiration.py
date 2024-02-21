from datetime import date
from dateutil.relativedelta import relativedelta


now = date.today()
three_days_later = now + relativedelta(days=3)
one_month_later = now + relativedelta(months=1)

# print(f"3일 후\ndate({three_days_later.year}, {three_days_later.month}, {three_days_later.day})")
# print(f"한달 후\ndate({one_month_later.year}, {one_month_later.month}, {one_month_later.day})")

# 만료 일정 (위의 출력 후 결정)
# expiration_date = date(2024, 2, 17)
expiration_date = ""