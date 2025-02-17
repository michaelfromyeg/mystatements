import datetime
from collections import defaultdict
import os

def parse_filename(filename):
    parts = filename.split('_')
    account_type = '_'.join(parts[:3])
    date_parts = parts[3:]
    start_date_str = '_'.join(date_parts[:2])
    end_date_str = '_'.join(date_parts[2:]).split('.')[0]

    start_date = datetime.datetime.strptime(start_date_str, '%b_%d')
    end_date = datetime.datetime.strptime(end_date_str, '%d_%Y')

    # Set the year for start_date based on end_date
    start_date = start_date.replace(year=end_date.year)

    # Handle year rollover
    if start_date > end_date:
        start_date = start_date.replace(year=end_date.year - 1)

    return account_type, start_date, end_date

def find_missing_days(filenames):
    statements = defaultdict(list)
    for filename in filenames:
        account_type, start_date, end_date = parse_filename(filename)
        statements[account_type].append((start_date, end_date))

    missing_days = defaultdict(list)
    for account_type, dates in statements.items():
        dates.sort(key=lambda x: x[0])
        for i in range(1, len(dates)):
            prev_end = dates[i-1][1]
            curr_start = dates[i][0]
            if (curr_start - prev_end).days > 1:
                missing_days[account_type].append((prev_end + datetime.timedelta(days=1), curr_start - datetime.timedelta(days=1)))

    return missing_days

def get_pdf_files_from_folder(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.pdf') and "TFSA" not in f]

# Specify the folder path
folder_path = '/mnt/c/Users/mdema/Documents/td'  # Replace this with the actual path to your folder

# Get the list of PDF files from the folder
filenames = get_pdf_files_from_folder(folder_path)

# Find missing days
missing = find_missing_days(filenames)

# Print the results
for account_type, gaps in missing.items():
    print(f"Missing days for {account_type}:")
    for start, end in gaps:
        print(f"  From {start.strftime('%B %d, %Y')} to {end.strftime('%B %d, %Y')}")