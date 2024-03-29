# -*- coding: utf-8 -*-
"""Model unit tests."""
from datetime import datetime

import pytest

from arrowmanager.models import Application, Build


# def test_created_at_defaults_to_datetime(self):
#     """Test creation date."""
#     group = Group(groupname='foo', email='foo@bar.com')
#     group.save()
#     assert bool(group.created_at)
#     assert isinstance(group.created_at, dt.datetime)
#
# def test_password_is_nullable(self):
#     """Test null password."""
#     group = Group(groupname='foo', email='foo@bar.com')
#     group.save()
#     assert group.password is None
#
# def test_factory(self, db):
#     """Test group factory."""
#     group = GroupFactory(password='myprecious')
#     db.session.commit()
#     assert bool(group.groupname)
#     assert bool(group.email)
#     assert bool(group.created_at)
#     assert group.is_admin is False
#     assert group.active is True
#     assert group.check_password('myprecious')
#
# def test_check_password(self):
#     """Check password."""
#     group = Group.create(groupname='foo', email='foo@bar.com',
#                        password='foobarbaz123')
#     assert group.check_password('foobarbaz123') is True
#     assert group.check_password('barfoobaz') is False
#
# def test_full_name(self):
#     """Group full name."""
#     group = GroupFactory(first_name='Foo', last_name='Bar')
#     assert group.full_name == 'Foo Bar'
#
# def test_roles(self):
#     """Add a role to a group."""
#     role = Role(name='admin')
#     role.save()
#     group = GroupFactory()
#     group.roles.append(role)
#     group.save()
#     assert role in group.roles


@pytest.mark.usefixtures('db')
class TestApplication:
    """Group tests."""

    def test_get_by_id(self):
        application = Application(tenant='default',
                                  name='Foo',
                                  repo='https://foo.git')
        application.save()

        retrieved = Application.get_by_id(application.id)
        assert retrieved == application


@pytest.mark.usefixtures('db')
class TestBuild:
    """Group tests."""

    def test_get_by_id(self, application):
        build = Build(application=application,
                      image="eu.gcr.io/gridarrow/twexcel",
                      git_rev='646df370f851479d7423da324ec0b09116335584',
                      buildtime=datetime.now())
        build.save()

        retrieved = Build.get_by_id(build.id)
        assert retrieved == build
