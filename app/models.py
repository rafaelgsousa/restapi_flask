from mongoengine import (BooleanField, Document, EmailField, ImageField,
                         IntField, StringField)


class User(Document):
    name = StringField(max_length=100, required=True)
    nickname = StringField(max_length=100, required=True, unique=True)
    age = IntField(min_value=18)
    email = EmailField()
    self_image = ImageField()
    is_active = BooleanField(default=True)
    cpf = StringField(max_length=14, required=True, unique=True)

    def clean(self):
        # Validate CPF
        if not self.validate_cpf(self.cpf):
            return {"message": "CPF is invalid!"}, 400

    @staticmethod
    def validate_cpf(cpf):
        if not cpf:
            return False
        
        import re

        # Correct mask for CPF
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            return False

        # Grab only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Does it have 11 digits?
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validate first digit after -
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validate second digit after -
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
