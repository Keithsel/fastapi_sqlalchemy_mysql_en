#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern: str, text: str) -> bool:
    """
    Regex match anywhere in the string

    :param pattern: Regular expression pattern
    :param text: Text to match
    :return:
    """
    if not pattern or not text:
        return False

    result = re.search(pattern, text)
    return result is not None


def match_string(pattern: str, text: str) -> bool:
    """
    Regex match from the beginning of the string

    :param pattern: Regular expression pattern
    :param text: Text to match
    :return:
    """
    if not pattern or not text:
        return False

    result = re.match(pattern, text)
    return result is not None


def is_phone(text: str) -> bool:
    """
    Check if the string is a valid phone number format

    :param text: Phone number to check
    :return:
    """
    if not text:
        return False

    phone_pattern = r'^1[3-9]\d{9}$'
    return match_string(phone_pattern, text)
