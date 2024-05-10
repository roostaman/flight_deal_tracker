from datetime import datetime, timedelta

now = datetime.now().date()
date_from = now.strftime("%d/%m/%Y")

days_later = now + timedelta(days=30*6)
date_to = days_later.strftime("%d/%m/%Y")
