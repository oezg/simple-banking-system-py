MAIN_MENU = """
1. Create an account
2. Log into account
0. Exit
"""

ACCOUNT_MENU = """
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""

CARD_CREATED = """
Your card has been created
Your card number:
{number}
Your card PIN:
{pin}
"""

INSTITUTE = "400000"

DB_FILENAME = 'card.s3db'

DB_CREATE_TABLE = """
    CREATE TABLE card (
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
    );
"""

DB_SELECT_NUMBER = "SELECT card.number FROM card;"

DB_INSERT_ACCOUNT = "INSERT INTO card (number, pin) VALUES ({number}, {pin});"

DB_SELECT_PIN = "SELECT pin FROM card WHERE number = {number};"

DB_SELECT_BALANCE = "SELECT balance FROM card WHERE number = {number};"

DB_DELETE_ACCOUNT = "DELETE FROM card WHERE number = {number};"

DB_UPDATE_BALANCE = "UPDATE card SET balance = balance + {amount} WHERE number = {number};"

LOG_OUT = "You have successfully logged out!"

ACCOUNT_CLOSED = "The account has been closed!"

LOG_IN_FAIL = "Wrong card number or PIN!"

LOG_IN_SUCCESS = "You have successfully logged in!"

DEPOSIT = "Income was added!"

SAME_ACCOUNT = "You can't transfer money to the same account!"

CHECK_SUM_ERROR = "Probably you made a mistake in the card number. Please try again!"
