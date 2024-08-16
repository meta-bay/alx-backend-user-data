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
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        else:
            raise ValueError(f'User {email} already exists')

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

    def get_user_from_session_id(self, session_id: str) -> User:
        """ find the user by the session id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            return None
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy session """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ generate reset password reset token """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                setattr(user, "reset_token", reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_passwd = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_passwd,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError
