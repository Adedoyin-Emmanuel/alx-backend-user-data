#!/usr/bin/env python3
"""
Write a function called filter_datum
that returns the log message obfuscated:
"""
import csv
import logging
import os
import re
from typing import List
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format record """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    return re.sub(r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)",
                  lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), message)


def get_logger() -> logging.Logger:
    """ return a logger object """
    lg = logging.getLogger("user_data")
    lg.setLevel(logging.INFO)
    lg.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    lg.addHandler(sh)
    return lg


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ connect to MySQL database """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "root"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "localhost"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    )


def main():
    """
    The main function
    """
    con = get_db()
    users = con.cursor()
    users.execute("SELECT CONCAT('name=', name, ';ssn=', ssn, ';ip=', ip, \
        ';user_agent', user_agent, ';') AS message FROM users;")
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger()

    for user in users:
        logger.log(logging.INFO, user[0])


if __name__ == "__main__":
    main()
