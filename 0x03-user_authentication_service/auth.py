#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ hashed with bcrypt.hashpw """
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_passwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ user Registeration """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user
