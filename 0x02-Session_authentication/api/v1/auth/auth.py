#!/usr/bin/env python3
"""Authentication Module"""
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the given path requires authentication.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for pattern in excluded_paths:
            if not pattern.endswith('/'):
                pattern = pattern + '*'
            if fnmatch.fnmatch(path, pattern):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """returns a cookie value from a request"""
        if request is None:
            return None
        session = None
        session_name = getenv('SESSION_NAME')
        if session_name is None:
            return None
        session = session_name
        cookie = request.cookies.get(session)
        return cookie
