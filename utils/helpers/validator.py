from datetime import datetime

from utils.helpers.loger import log


class Verify:
    @staticmethod
    def equals(expected, actual, message_on_fail):
        try:
            assert expected == actual, message_on_fail
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error(f"{err_type}: {message_on_fail}\n\texpected: {expected}\n\tactual: {actual}")
            raise err

    @staticmethod
    def not_equals(expected, actual, message_on_fail):
        try:
            assert expected != actual, message_on_fail
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error(f"{err_type}: {message_on_fail}\n\texpected: {expected}\n\tactual: {actual}")
            raise err

    @staticmethod
    def true(condition, message_on_fail):
        try:
            assert condition, message_on_fail
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error(f"{err_type}: {message_on_fail}")
            raise err

    @staticmethod
    def false(condition, message_on_fail):
        try:
            assert not condition, message_on_fail
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error(f"{err_type}: {message_on_fail}")
            raise err

    @staticmethod
    def contains(expected, actual, message_on_fail):
        try:
            assert expected in actual, message_on_fail
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error(f"{err_type}: {message_on_fail}\n\texpected: {expected}\n\tactual: {actual}")
            raise err

    @staticmethod
    def not_contains(expected, actual, message_on_fail):
        try:
            assert expected not in actual, message_on_fail
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error(f"{err_type}: {message_on_fail}\n\texpected: {expected}\n\tactual: {actual}")
            raise err

    @staticmethod
    def dict_contains_key(key, dict_, message_on_fail):
        """
        :param key: expected key
        :param dict_: dict obj
        :param message_on_fail: message printed on fail
        :return: True if key exists in dict_
        """
        try:
            assert key in dict_.keys()
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error("%s: %s", err_type, message_on_fail)
            log.debug(f"Dict '{dict_}' does not contain key '{key}'")
            raise err

    @staticmethod
    def dict_contains_all_keys(dict_, keys: list[str], message_on_fail):
        """
        :param dict_: dict obj
        :param keys: expected key list
        :param message_on_fail: message printed on fail
        :return: True if key exists in dict_
        """
        try:
            assert sorted(dict_.keys()) == sorted(keys)
        except AssertionError as err:
            err_type = err.__class__.__name__
            log.error("%s: %s", err_type, message_on_fail)
            log.debug(f"Dict '{dict_}' does not contain all keys '{keys}'")
            raise err

    @staticmethod
    def date_in_format(date_str, date_format, message_on_fail):
        """
        Verify that given date has specific given date format
        :param date_str: date as string
        :param date_format: date format as string
        :param message_on_fail: message to raise exception with
        """
        try:
            datetime.strptime(date_str, date_format)
        except ValueError as err:
            err_type = err.__class__.__name__
            log.error("%s: %s", err_type, message_on_fail)
            log.debug("Date value '%s' does not conform to format '%s'", date_str, date_format)
            raise err
