#!/usr/bin/env python3
""" filtered_logger """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    pattern = r'({})=[^{}]+'.format(
        '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(
        pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)
