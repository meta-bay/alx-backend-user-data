#!/usr/bin/env python3
""" authentication """
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """ authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return True if the path requires authentication"""
        if path:
            if path.endswith('/'):
                alt_path = path[:-1]
            else:
                alt_path = path + '/'

            if excluded_paths and excluded_paths != []:
                if path in excluded_paths or alt_path in excluded_paths:
                    return False

                for ex_path in excluded_paths:
                    if ex_path.endswith('*'):
                        base_ex_path = ex_path[:-1]
                        if (path.startswith(base_ex_path) or
                                alt_path.startswith(base_ex_path)):
                            return False
                    else:
                        if path == ex_path or alt_path == ex_path:
                            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        auth_value = request.headers.get('Authorization')
        return auth_value

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
