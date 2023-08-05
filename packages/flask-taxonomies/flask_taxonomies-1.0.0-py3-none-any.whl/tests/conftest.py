# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from flask_taxonomies.app import create_app
from flask_taxonomies.extensions import db as _db
from flask_taxonomies.models import Taxonomy


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def root_taxonomy(db):
    """Create root taxonomy element."""
    root = Taxonomy(
        slug="root", title='{"en": "Root"}', description="Taxonomy root term"
    )
    db.session.add(root)
    db.session.commit()
    return root
