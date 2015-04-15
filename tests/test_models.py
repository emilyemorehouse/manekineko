# -*- coding: utf-8 -*-

from fbone.user import User

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):

        assert User.query.count() == 2


# testing delete, check id url after and assert 404