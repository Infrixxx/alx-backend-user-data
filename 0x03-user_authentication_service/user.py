#!/usr/bin/env python3
"""This module defines the User model for a SQLAlchemy database"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

Base = declarative_base()


class User(Base):
    """Represents a user in the database"""
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250), nullable=True)
    reset_token: Optional[str] = Column(String(250), nullable=True)
