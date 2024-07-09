#!/usr/bin/env python3
""" A module containing an authentication class
that inherits from Auth"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User
from flask import request

UserType = TypeVar('UserType', bound=User)


class BasicAuth(Auth):
    """An authentication class that inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of the
        Authorization header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """returns the user email and password
        from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> UserType:
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> UserType:
        """Retrieves the User instance for a request"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if base64_auth_header is None:
            return None

        decode_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decode_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decode_auth_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
