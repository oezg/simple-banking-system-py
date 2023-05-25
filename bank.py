import random
import sqlite3
import sys

import resources
import luhn


class Bank:
    def __init__(self, db_connection):
        self.conn: sqlite3.Connection = db_connection

    def main_menu(self):
        print(resources.MAIN_MENU)
        user_input = get_user_input('0', '1', '2')
        match user_input:
            case '0':
                self.exit_bank()
            case '1':
                self.create_account()
                self.main_menu()
            case '2':
                self.log_in()

    def exit_bank(self):
        print('Bye!')
        self.conn.close()
        sys.exit(0)

    def log_in(self):
        number = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        if self.authenticate(number, pin):
            print(resources.LOG_IN_SUCCESS)
            self.account_menu(number)
        else:
            print(resources.LOG_IN_FAIL)
            self.main_menu()

    def account_menu(self, card_number):
        print(resources.ACCOUNT_MENU)
        user_input = get_user_input('0', '1', '2', '3', '4', '5')
        match user_input:
            case '0':
                self.exit_bank()
            case '1':
                self.show_balance(card_number)
                self.account_menu(card_number)
            case '2':
                self.deposit(card_number)
                self.account_menu(card_number)
            case '3':
                self.transfer(card_number)
                self.account_menu(card_number)
            case '4':
                self.close_account(card_number)
                self.main_menu()
            case '5':
                print(resources.LOG_OUT)
                self.main_menu()

    def authenticate(self, number, pin):
        result = self.conn.cursor().execute(resources.DB_SELECT_PIN.format(number=number)).fetchone()
        return result and pin == result[0]

    def insert_into_database(self, card_number: str, card_pin: str):
        cur = self.conn.cursor()
        cur.execute(resources.DB_INSERT_ACCOUNT.format(number=card_number, pin=card_pin))
        self.conn.commit()

    def create_account(self):
        existing_card_numbers = self.get_existing_card_numbers()
        new_card_number = luhn.get_new_card_number(existing_card_numbers)
        card_pin = create_pin()
        self.insert_into_database(new_card_number, card_pin)
        print(resources.CARD_CREATED.format(number=new_card_number, pin=card_pin))

    def get_existing_card_numbers(self):
        return {row[0] for row in self.conn.cursor().execute(resources.DB_SELECT_NUMBER).fetchall()}

    def get_balance(self, card_number):
        return self.conn.cursor().execute(resources.DB_SELECT_BALANCE.format(number=card_number)).fetchone()[0]

    def show_balance(self, card_number):
        balance = self.get_balance(card_number)
        print(f"Balance: {balance}")

    def deposit(self, card_number: str):
        amount = max(0, int(input('Enter income:\n')))
        self.update_balance(amount, card_number)
        print(resources.DEPOSIT)

    def update_balance(self, amount: int, card_number: str):
        self.conn.cursor().execute(resources.DB_UPDATE_BALANCE.format(amount=amount, number=card_number))
        self.conn.commit()

    def transfer(self, origin_card_number):
        print('Transfer')
        target_card_number = input('Enter card number:\n')
        if origin_card_number == target_card_number:
            print(resources.SAME_ACCOUNT)
        elif target_card_number in self.get_existing_card_numbers():
            transfer_amount = int(input('Enter how much money you want to transfer:\n'))
            if transfer_amount > self.get_balance(origin_card_number):
                print('Not enough money!')
            else:
                self.update_balance(-transfer_amount, origin_card_number)
                self.update_balance(transfer_amount, target_card_number)
                print('Success!')
        elif luhn.match_check_sum(target_card_number):
            print('Such a card does not exist.')
        else:
            print(resources.CHECK_SUM_ERROR)
        self.account_menu(origin_card_number)

    def close_account(self, card_number):
        self.conn.cursor().execute(resources.DB_DELETE_ACCOUNT.format(number=card_number))
        self.conn.commit()
        print(resources.ACCOUNT_CLOSED)


def create_pin(digits: int = 4):
    return str(random.randint(10 ** (digits - 1), 10 ** digits - 1))


def get_user_input(*args):
    while (user := input()) not in args:
        print('Enter', ' or '.join(args))
    return user
