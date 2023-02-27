"""
Provides fake test data for tests
"""
import random
import string
from datetime import datetime, timedelta
from faker import Faker


class __Fake:

    def __init__(self):
        self.fake = Faker()

    def __str__(self):
        return "Create fake testing data such as company, address, email, zipcode, state, city, etc..."

    def _random_number(self, length=1):
        """
        Generate a random number with 1 digit (default length =1)
        or a random number with given number of digits.
        :param length: maximum number of digits
        :returns: random number with given number of digits
        """
        if length == 1:
            return self.fake.random_digit_not_null()
        res = ""
        for i in range(0, length):
            number = self.fake.random_digit_not_null()
            res += str(number)
        return int(res)

    def number(self, length=2):
        return self._random_number(length)

    def password(self):
        return self.fake.password() + "P@ssw0rd"

    def phone(self):
        return "+" + str(self.fake.random_number(15))

    def property_id(self):
        return self.fake.word() + str(self.fake.random_number(15))

    def property_name(self, length=7):
        return " ".join(self.fake.word() for _ in range(0, length)).capitalize() + " !" + str(self.number(length=3))

    def address(self):
        return self.fake.address().replace("\n", " ")

    def city(self):
        return self.fake.city()

    def email(self, unique=True):
        if unique:
            return "aqa_test_{}_{}{}".format(self.fake.word(), self.fake.word(), "@fake.net")
        return "aqa_test_grifan@gmail.com"

    def word(self):
        return self.fake.word()

    def words_combination(self, count=3):
        return " ".join([self.fake.word() for _ in range(count)])

    @staticmethod
    def letters_numbers(length):
        """
        Generates random string containing only letters and/or number symbols
        :param length: length of string
        """
        sources = string.ascii_letters + string.digits
        return "".join([random.choice(sources) for _ in range(0, length)])

    @staticmethod
    def get_formatted_date(dt_format, delta_in_minutes=0):
        dt = datetime.now() + timedelta(minutes=delta_in_minutes)
        return dt.strftime(dt_format)


fake = __Fake()
