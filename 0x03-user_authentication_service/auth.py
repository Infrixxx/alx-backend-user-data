#!/usr/bin/env python3
"""A module containing password hashing for users"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a new UUID string"""
    string = uuid.uuid4()
    return str(string)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password=password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                try:
                    hashed_bytes = user.hashed_password.encode('utf-8')
                except AttributeError:
                    hashed_bytes = user.hashed_password
                if bcrypt.checkpw(
                    password.encode("utf-8"),
                    hashed_bytes,
                ):
                    return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """creates a session for a user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self, session_id: Optional[str]) -> Optional[User]:
        """Returns the corresponding user using session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: Optional[int]) -> None:
        """Updates the corresponding user session ID to None"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """generates a token used to reset the password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password as verified by the reset token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
