import random
import resources


def generate_card_number(account_id, institute_id=resources.INSTITUTE):
    check_sum = get_check_sum(institute_id + account_id)
    return institute_id + account_id + check_sum


def get_check_sum(number):
    digits = []
    for i, num in enumerate(number):
        temp = int(num)
        if i % 2 == 0:
            temp *= 2
            if temp > 9:
                temp -= 9
        digits.append(temp)
    check_sum = (10 - (sum(digits) % 10)) % 10
    return str(check_sum)


def match_check_sum(card_number: str) -> bool:
    assert len(card_number) > 0
    return card_number[-1] == get_check_sum(card_number[:-1])


def get_new_card_number(existing_numbers: set[str]) -> str:
    account_id = str(random.randint(10 ** 8, 10 ** 9 - 1))
    card_number = generate_card_number(account_id)
    if card_number in existing_numbers:
        get_new_card_number(existing_numbers)
    return card_number
