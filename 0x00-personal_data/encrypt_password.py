#!/usr/bin/env python3
"""
    encryption password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Expects one string argument name password and returns
       a salted, hashed password, which is a byte string.

    Args:
        password (str): password

    Returns:
        bytes: encryption password
    """
    if password:
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check password

    Args:
        hashed_password (bytes): hash
        password (str): password

    Returns:
        bool: true or false
    """
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)