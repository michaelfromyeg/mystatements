import datetime

def generate_month_list(start_date, end_date):
    months = []
    current_date = start_date
    while current_date <= end_date:
        months.append(current_date.strftime("%b_%Y"))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    return months

start_date = datetime.date(2019, 1, 1)
end_date = datetime.date(2024, 12, 31)

all_months = generate_month_list(start_date, end_date)

filenames = [
    # List of all filenames provided
    # (Omitted for brevity, but in practice would include all filenames)
]

missing_months = []

for month in all_months:
    if not any(month in filename for filename in filenames):
        missing_months.append(month)

print("Missing months:", missing_months)