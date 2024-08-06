#!/usr/bin/env python3
""" authentication """
from flask import request
from typing import List, TypeVar


class Auth():
    """ authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require authentication '''
        if not path or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None
