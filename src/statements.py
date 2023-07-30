# Read in PDFs and convert to required data format

import os
import sys
from pprint import pprint
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime
from tika import parser
from transaction import Transaction, TransactionKind
import plotly.graph_objects as go
import numpy as np

DEBUG = False

STATEMENTS_DIRECTORY = "data/statements"

NEW_CHEQUING_PREAMBLE = "TD_CHEQUING"
NEW_SAVINGS_PREAMBLE = "TD_SAVINGS"

TOTALS = []
DIFFS = []


def main(kind: str) -> None:
    """
    Process all statement data and produce list of transaction history.
    """

    # Create map for known transaction descriptions
    data: Dict = get_dict(kind)

    # Skip PDFs we're not interested in processing
    other_kind: str = "savings" if kind == "chequing" else "chequing"
    print(f"NOTE: Skipping {other_kind} accounts!")

    files = os.listdir(STATEMENTS_DIRECTORY)
    formatted_files = [x for x in files if kind.upper() in x]
    formatted_files.sort(key=lambda f: get_filename_date(f, kind))

    # Loop through files
    for filename in formatted_files:

        # Initialize accumulator
        transactions: List[Transaction] = []

        print(f"Looking at {filename}...")

        # Read in PDF data and remove unnecessary characters, blank lines
        raw = parser.from_file(f"{STATEMENTS_DIRECTORY}/{filename}")
        text = "".join(
            [
                s
                for s in raw["content"].strip().splitlines(True)
                if s.strip("\r\n").strip()
            ]
        )
        dump = open("./dump.txt", "w+")
        dump.write(text)

        # Get lines (each line is a transaction or None)
        lines = text.split("\n")

        # Process each line
        for line in lines:
            t = process_line(line, data, kind, filename)
            if t:
                transactions.append(t)

        # Print summary data
        process_transactions(filename, transactions)

        # Graph transactions
        graph(transactions)


def get_filename_date(filename: str, kind: str) -> datetime.date:
    """
    Sort files by the date included in the files
    """
    preamble: str = (
        NEW_CHEQUING_PREAMBLE if kind == "chequing" else NEW_SAVINGS_PREAMBLE
    )

    # Get the dates part of the string: after hte preamble, remove '.pdf', skip the leading '_'
    dates = filename.split(preamble)[1].replace(".pdf", "")[1:]

    # Split from_date, to_date
    from_date_str, to_date_str = dates.split("_")
    from_date: datetime.date = datetime.strptime(from_date_str.strip(), "%Y-%m-%d")
    # to_date: datetime.date = datetime.strptime(to_date_str.strip(), "%Y-%m-%d")

    return from_date


def get_dict(kind: str) -> Dict:
    """
    Load in 'knowledge bank' (pun intended) of savings or chequing data.
    """
    data: Dict = None

    # Load in required JSON data
    with open(f"data/{kind}.json") as f:
        data = json.load(f)

    return data


def process_line(
    line: str, data: Dict, kind: str, filename: str
) -> Optional[Transaction]:
    """
    Process each line of a statement.
    """
    if DEBUG:
        pprint(line)
        pprint(filename)

    # Initialize locals
    t_new: Transaction = None

    # Get values that we can process
    values = line.split(" ")

    # Check the entry against all of the keys
    # TODO: rewrite as hashmap and save as dump; detect changes to json file
    for key in data.keys():
        # Skip if it's the header; otherwise instantiate the new transaction's fields
        if "DESCRIPTION" in line:
            return
        if key in line:
            t_orig = data[key]
            t_kind = kind_helper(t_orig["kind"])
            t_description = "TODO"
            t_date = date_helper(values[int(t_orig["date"])], kind, filename)
            t_amount = amount_helper(values[int(t_orig["amount"])])
            print(f"\tkey: {key}\tkind: {t_kind}\tamt: {t_amount}")
            t_new = Transaction(t_kind, t_description, t_amount, t_date)
            return t_new
    return None


def kind_helper(raw: str) -> TransactionKind:
    """
    Infer a transaction kind from a given string.
    """
    if raw == "START":
        return TransactionKind.START
    elif raw == "TRANSFER":
        return TransactionKind.TRANSFER
    elif raw == "CREDIT":
        return TransactionKind.CREDIT
    elif raw == "FEES":
        return TransactionKind.FEES
    elif raw == "DEPOSIT":
        return TransactionKind.DEPOSIT
    elif raw == "WITHDRAWL":
        return TransactionKind.WITHDRAWL


def date_helper(raw: str, kind: str, filename: str) -> datetime:
    """
    Get new date from a filename.
    """
    return datetime.strptime(raw, "%b%d").replace(
        year=int(
            filename[
                len(f"TD_{kind.capitalize()}_") : len(f"TD_{kind.capitalize()}_") + 4
            ]
        )
    )


def amount_helper(raw: str) -> int:
    """
    Get cents amount from a string containing a float.
    """
    # Remove commas
    raw = raw.replace(",", "")

    # Add leading 0
    if raw[0] == ".":
        raw = "0" + raw

    # String (in dollars) to float (in dollars) to int (in cents)
    f = float(raw)
    t = int(f * 100)
    return t


def process_transactions(filename: str, transactions: List[Transaction]) -> None:
    """
    Process and print transaction summary information.
    """
    # Initialize accumulators
    amt = 0
    start = 0

    # Loop through transactions and process
    for t in transactions:
        d_amt, d_start = process_transaction(t)
        amt += d_amt
        if d_start:
            start = d_start

    # Append to globals for summary statistics
    TOTALS.append(amt / 100)
    DIFFS.append((amt - start) / 100)

    print(
        f"{filename} Summary\n\
            \t- Start: ${start/100}\n\
            \t- Finish: ${amt/100}\n\
            \t- Difference: ${(amt-start)/100}\n\
        "
    )


def process_transaction(t: Transaction) -> Tuple[int, int]:
    """
    Get [amount, start] from a transaction based on its kind and amount.
    """
    if t.kind == TransactionKind.START:
        return [t.amount, t.amount]
    elif t.kind == TransactionKind.DEPOSIT:
        return [t.amount, None]
    elif t.kind == TransactionKind.CREDIT:
        return [t.amount, None]
    elif t.kind == TransactionKind.WITHDRAWL:
        return [-t.amount, None]
    elif t.kind == TransactionKind.TRANSFER:
        return [-t.amount, None]
    elif t.kind == TransactionKind.FEES:
        return [-t.amount, None]
    else:
        raise Exception("Invalid transaction kind given.")


def graph(transactions: List[Transaction]) -> None:
    N = 100
    # x = np.random.rand(N)
    # y = np.random.rand(N)
    colors = np.random.rand(N)
    sz = np.random.rand(N) * 30

    x = [t.date for t in transactions]
    y = [t.amount for t in transactions]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=go.scatter.Marker(
                size=sz, color=colors, opacity=0.6, colorscale="Viridis"
            ),
        )
    )

    fig.show()
    fig.write_image("images/fig1.png")


# Driver code: run main with argv[1]
if __name__ == "__main__":
    if len(sys.argv) != 2 or not (
        sys.argv[1] == "savings" or sys.argv[1] == "chequing"
    ):
        print("usage: python statements.py [savings|chequing]")
    else:
        main(sys.argv[1])
        print("=== SUMMARY STATISTICS ===")
        print(
            f"Your maximum value was ${max(TOTALS)} and your minimum value was ${min(TOTALS)}."
        )
        print(
            f"Your maximum gain was ${max(DIFFS)} and your maximum loss (or min gain) was ${min(DIFFS)}."
        )
        print("Done!")
