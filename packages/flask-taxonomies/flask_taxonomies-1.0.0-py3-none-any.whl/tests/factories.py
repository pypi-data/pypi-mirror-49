# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory.alchemy import SQLAlchemyModelFactory

from flask_taxonomies.database import db


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session
