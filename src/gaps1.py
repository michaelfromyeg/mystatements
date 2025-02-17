import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict
from statistics import mode, StatisticsError

def parse_filename(filename: str) -> Tuple[str, str, datetime, datetime]:
    patterns = [
        r'(\w+)_(?:STUDENT_)?(\w+)_ACCOUNT_.*_(\w+_\d+)-(\w+_\d+)_(\d{4})\.pdf',
        r'MULTI-HOLDING_(\w+)_.*_(\w+_\d+)_(\d{4})\.pdf'
    ]

    for pattern in patterns:
        match = re.match(pattern, filename)
        if match:
            groups = match.groups()
            if len(groups) == 5:  # Chequing or Savings
                bank, account_type, start_date, end_date, year = groups
                start_date = datetime.strptime(f"{start_date}_{year}", "%b_%d_%Y")
                end_date = datetime.strptime(f"{end_date}_{year}", "%b_%d_%Y")
                if end_date < start_date:  # Year-end statement
                    end_date = end_date.replace(year=end_date.year + 1)
            else:  # TFSA
                account_type, end_date, year = groups
                bank = "MULTI-HOLDING"
                end_date = datetime.strptime(f"{end_date}_{year}", "%b_%d_%Y")
                start_date = end_date.replace(day=1)  # Assume start of the month

            return bank, account_type, start_date, end_date

    raise ValueError(f"Unable to parse filename: {filename}")

def analyze_statements(folder_path: str) -> Dict[str, List[Tuple[datetime, datetime]]]:
    statements = defaultdict(list)

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            bank, account_type, start_date, end_date = parse_filename(filename)
            key = f"{bank}_{account_type}"
            statements[key].append((start_date, end_date))

    return statements

def infer_expected_gap(dates: List[Tuple[datetime, datetime]]) -> timedelta:
    sorted_dates = sorted(dates, key=lambda x: x[0])
    gaps = [(sorted_dates[i+1][0] - sorted_dates[i][1]).days for i in range(len(sorted_dates)-1)]
    try:
        most_common_gap = mode(gaps)
    except StatisticsError:
        # If there's no unique mode, use the minimum gap
        most_common_gap = min(gaps)
    return timedelta(days=most_common_gap)

def check_for_gaps(statements: Dict[str, List[Tuple[datetime, datetime]]]) -> Dict[str, List[Tuple[datetime, datetime]]]:
    gaps = {}

    for account, dates in statements.items():
        expected_gap = infer_expected_gap(dates)
        sorted_dates = sorted(dates, key=lambda x: x[0])
        account_gaps = []

        for i in range(1, len(sorted_dates)):
            prev_end = sorted_dates[i-1][1]
            current_start = sorted_dates[i][0]

            if current_start - prev_end > expected_gap + timedelta(days=1):
                account_gaps.append((prev_end + timedelta(days=1), current_start - timedelta(days=1)))

        if account_gaps:
            gaps[account] = account_gaps

    return gaps

def main(folder_path: str):
    statements = analyze_statements(folder_path)
    gaps = check_for_gaps(statements)

    for account, dates in statements.items():
        sorted_dates = sorted(dates, key=lambda x: x[0])
        start_date = sorted_dates[0][0]
        end_date = max(date[1] for date in sorted_dates)

        print(f"\nAccount: {account}")
        print(f"Date range: {start_date.date()} to {end_date.date()}")
        expected_gap = infer_expected_gap(dates)
        print(f"Inferred statement frequency: {expected_gap.days} days")

        if account in gaps:
            print("Gaps found:")
            for gap_start, gap_end in gaps[account]:
                if gap_start >= start_date and gap_end <= end_date:
                    print(f"  {gap_start.date()} to {gap_end.date()}")
        else:
            print("No gaps found.")

if __name__ == "__main__":
    folder_path = "/mnt/c/Users/mdema/Documents/td"  # Assumes the script is run in the same directory as the files
    main(folder_path)