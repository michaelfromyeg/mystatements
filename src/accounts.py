"""
Process account data for CSV files exported from TD.

NOTE: currently, you can only export transaction data for 18 months at a time, so you'll have to manually "stitch" together data
to get a complete history. Eventually I'll get aruond to writing a migrator tool.

"""

import sys
from pprint import pprint
from typing import List, Dict
from datetime import datetime
import csv
from transaction import Transaction, TransactionKind

DEBUG = True

ACCOUNTS_DIRECTORY = "data/accounts"


def main(kind: str) -> None:
    """
    Process account data.

    Raw CSV comes in the form:
    date[0],transaction description[1],withdrawls[2],deposits[3],balance[4]

    Process into transaction objects.
    """
    # Setup transactions list
    transactions: List[Transaction] = []

    # Open file from accounts directory, of kind
    with open(f"{ACCOUNTS_DIRECTORY}/{kind}.csv", newline="") as f:

        # Read in CSV data
        d = csv.reader(f)

        # Loop through row data
        for row in d:

            # Get kind, description
            kind: TransactionKind = TransactionKind.NULL
            description: str = row[1].strip()

            # Get amount: if row[2] is a non-empty string, it's a withdrawl;
            # if row[3] is a non-empty string, it's a deposit
            amount: int = 0
            if row[2]:
                amount = int(float(row[2]) * 100)
                kind = TransactionKind.WITHDRAWL
            elif row[3]:
                amount = int(float(row[3]) * 100)
                kind = TransactionKind.DEPOSIT

            # Get date (in form MM/DD/YYYY) and balance for printing
            date: datetime.date = datetime.strptime(row[0].strip(), "%m/%d/%Y")
            balance: str = row[4]

            if DEBUG:
                print(
                    f"kind: {kind}\tdescription: {description}\n\tamount: {amount}\tdate: {date}\tbalance: {balance}"
                )

            t: Transaction = Transaction(kind, description, amount, date)
            transactions.append(t)

    process_transactions(transactions)


def process_transactions(transactions: List[Transaction]) -> None:
    """
    Print sum of all transaction and withdrawl data.
    """
    # Initialize accumulator
    amt: int = 0

    # Loop through transactions; sum based on kind
    for t in transactions:
        if t.kind == TransactionKind.DEPOSIT:
            amt += t.amount
        elif t.kind == TransactionKind.WITHDRAWL:
            amt -= t.amount
        else:
            raise Exception(
                f"Invalid transaction kind given in process_transactions: ${t.kind}"
            )

    # Print accumulator
    print(f"Sum of all deposits and withdrawls is ${amt / 100}")


# Driver code: run main with argv[1]
if __name__ == "__main__":
    if len(sys.argv) != 2 or not (
        sys.argv[1] == "savings" or sys.argv[1] == "chequing"
    ):
        print("usage: python accounts.py [savings|chequing]")
    else:
        main(sys.argv[1])
        print("Done!")
