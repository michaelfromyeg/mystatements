"""
Data types for transaction information.
"""

import datetime
from enum import Enum
from dataclasses import dataclass


class TransactionKind(Enum):
    """
    An enum for transaction types
    """

    NULL = 1  # the default transaction kind; type is unclear or undefined
    START = 2
    DEPOSIT = 3
    TRANSFER = 4
    CREDIT = 5
    FEES = 6
    WITHDRAWL = 7


@dataclass(frozen=True)
class Transaction:
    """
    A class representing a generic transaction on a TD statement.

    To get an object's "ID", invoke __hash__ (since the object is frozen, this is okay).
    """

    kind: TransactionKind  # One-of: Start, Deposit, Transfer, Credit, Fees
    description: str  # A text description of the transfer
    amount: int  # Montary amount, in cents
    date: datetime.date  # The date of the transaction (MM-DD)


if __name__ == "__main__":
    print(
        "Oops... are you sure you meant to run this file?\n\
        There are only data types and helpers here!"
    )
    raise Exception
