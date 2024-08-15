#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """ hashed with bcrypt.hashpw """
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_passwd


def _generate_uuid() -> str:
    """ generates uuid """
    new_uuid = uuid.uuid4()
    return str(new_uuid)


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

    def valid_login(self, email: str, password: str) -> bool:
        """ credentials validation """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password
                ):
                    return True
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Get session ID """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                new_uuid = _generate_uuid()
                setattr(user, 'session_id', new_uuid)
                self._db._session.commit()
                return new_uuid
        except NoResultFound:
            pass
        return None
