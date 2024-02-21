from datetime import date
from dateutil.relativedelta import relativedelta


now = date.today()
three_days_later = now + relativedelta(days=3)

# print(f"3일 후\ndate({three_days_later.year}, {three_days_later.month}, {three_days_later.day})")

# 만료 일정 (위의 출력 후 결정)
expiration_date = date(2024, 12, 17)