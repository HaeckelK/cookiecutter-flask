# -*- coding: utf-8 -*-
"""Database unit tests."""
import datetime as dt

import pytest

from {{cookiecutter.app_name}}.database import PkModel, Column, db
from flask_login import UserMixin


class TestUser(UserMixin, PkModel):
    """Example model class."""

    __tablename__ = "testusers"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username, email):
        super().__init__(username=username, email=email)


@pytest.mark.usefixtures("db")
class TestCRUDMixin:
    """CRUDMixin tests."""

    def test_create(self):
        """Test CRUD create."""
        user = TestUser.create(username="foo", email="foo@bar.com")
        assert TestUser.get_by_id(user.id).username == "foo"

    def test_delete_with_commit(self):
        """Test CRUD delete with commit."""
        user = TestUser("foo", "foo@bar.com")
        user.save()
        assert TestUser.get_by_id(user.id) is not None
        user.delete(commit=True)
        assert TestUser.get_by_id(user.id) is None

    def test_delete_without_commit(self):
        """Test CRUD delete without commit."""
        user = TestUser("foo", "foo@bar.com")
        user.save()
        user.delete(commit=False)
        assert TestUser.get_by_id(user.id) is not None

    @pytest.mark.parametrize("commit,expected", [(True, "bar"), (False, "foo")])
    def test_update(self, commit, expected, db):
        """Test CRUD update with and without commit."""
        user = TestUser(username="foo", email="foo@bar.com")
        user.save()
        user.update(commit=commit, username="bar")
        retrieved = db.session.execute("""select * from testusers""").fetchone()
        assert retrieved.username == expected


@pytest.mark.usefixtures("db")
class TestPkModel:
    """PkModel tests."""

    def test_get_by_id_wrong_type(self):
        assert TestUser.get_by_id("twelve") is None
