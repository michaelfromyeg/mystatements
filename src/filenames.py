# Normalize filenames in the STATEMENTS_DIRECTORY folder

import os
from typing import Tuple

DEBUG = False

STATEMENTS_DIRECTORY = "data/statements"

# File informaton; should live in constants
OLD_CHEQUING_PREAMBLE = "TD_STUDENT_CHEQUING_ACCOUNT_"
OLD_SAVINGS_PREAMBLE = "TD_HIGH_INTEREST_SAVINGS_ACCOUNT_"
NEW_CHEQUING_PREAMBLE = "TD_CHEQUING"
NEW_SAVINGS_PREAMBLE = "TD_SAVINGS"
EXT = "pdf"


def rename() -> None:
    """
    Rename all files in the STATEMENTS_DIRECTORY
    """
    if DEBUG:
        print(f"NUMBER OF STATEMENTS: {len(os.listdir(STATEMENTS_DIRECTORY))}")
    for filename in os.listdir(STATEMENTS_DIRECTORY):
        if (
            filename[0 : len(NEW_CHEQUING_PREAMBLE)] == NEW_CHEQUING_PREAMBLE
            or filename[0 : len(NEW_SAVINGS_PREAMBLE)] == NEW_SAVINGS_PREAMBLE
        ):
            continue
        dst = get_name(filename)
        src = f"{STATEMENTS_DIRECTORY}/{filename}"
        dst = f"{STATEMENTS_DIRECTORY}/{dst}"
        if DEBUG:
            print(dst)
        else:
            os.rename(src, dst)
    return None


def get_name(old_name: str) -> str:
    """
    Generate new filename
    """
    is_chequing = get_is_chequing(old_name)

    ending = old_name.split(
        OLD_CHEQUING_PREAMBLE if is_chequing else OLD_SAVINGS_PREAMBLE
    )[1]

    # Convert from, to dates to numbers (instead of strings)
    from_date, to_date = ending.split("-")
    from_mo, from_day = date_to_numbers(from_date, True)
    to_mo, to_day = date_to_numbers(to_date, False)

    year = get_year(ending)

    return f"{NEW_CHEQUING_PREAMBLE if is_chequing else NEW_SAVINGS_PREAMBLE}_{year}-{from_mo}-{from_day}_{year}-{to_mo}-{to_day}.{EXT}"


def get_is_chequing(old_name: str) -> bool:
    """
    Determine whether an old file name is from an old chequing account or not.
    """
    return (
        len(old_name) >= len(OLD_CHEQUING_PREAMBLE)
        and old_name[0 : len(OLD_CHEQUING_PREAMBLE)] == OLD_CHEQUING_PREAMBLE
    )


def date_to_numbers(old_date: str, is_from: bool) -> Tuple[str, str]:
    """
    Convert an old date to 'numbers', e.g., Jan_31 to [01, 31]
    """
    mo = month_to_num(old_date[0:3])
    day = old_date[4:6]
    if mo == "12" and day == "31" and is_from:
        return ("01", "01")
    return (mo, day)


def get_year(ending: str) -> str:
    """
    Get the year from the ending string
    """
    return ending[-8:-4]


def month_to_num(mo: str) -> str:
    """
    Convert string months to 'numbers'
    """
    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    return months.get(mo, Exception("Invalid month"))


# Driver code: rename all files in statements directory
if __name__ == "__main__":
    rename()
