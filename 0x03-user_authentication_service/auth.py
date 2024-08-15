#!/usr/bin/env python3
""" auth module """
import bcrypt


def _hash_password(password: str) -> str:
    """ hashed with bcrypt.hashpw """
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_passwd
