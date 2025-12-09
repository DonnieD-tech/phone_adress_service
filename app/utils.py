import re

PHONE_PATTERN = r"^\+7[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$"

PHONE_EXAMPLES = [
    '+79399562637',
    '+7(939)9562637'
]

PHONE_DESC = 'Номер телефона в формате +7XXXXXXXXXX или +7(XXX)XXXXXXX'

ADDRESS_EXAMPLES = [
    'ул. Ткачева, 17',
    'Барбарисовая, 29, кв.17'
]

ADDRESS_DESC = 'Полный адрес'


def phone_normalization(phone: str) -> str:
    phone = phone.strip()

    if phone.startswith('+'):
        char_plus = '+'
    else:
        char_plus = ''

    digits = re.sub(
        r'\D',
        '', phone
    )

    normalized = char_plus + digits
    return normalized