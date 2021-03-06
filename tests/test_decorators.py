from unittest.mock import patch

from django.test import override_settings

from promise import Promise, is_thenable

from graphql_social_auth import decorators, exceptions

from .decorators import social_auth_mock
from .testcases import TestCase


class DecoratorsTests(TestCase):

    def test_psa_missing_backend(self):

        @decorators.social_auth
        def wrapped(cls, root, info, provider, *args):
            """Social Auth decorated function"""

        with self.assertRaises(exceptions.GraphQLSocialAuthError):
            wrapped(self, None, self.info(), 'unknown', 'token')

    @social_auth_mock
    @override_settings(SOCIAL_AUTH_PIPELINE=[])
    def test_psa_invalid_token(self, *args):

        @decorators.social_auth
        def wrapped(cls, root, info, provider, *args):
            """Social Auth decorated function"""

        with self.assertRaises(exceptions.InvalidTokenError):
            wrapped(self, None, self.info(), 'google-oauth2', 'token')

    @social_auth_mock
    @patch('social_core.backends.oauth.BaseOAuth2.do_auth')
    def test_psa_do_auth_error(self, *args):

        @decorators.social_auth
        def wrapped(cls, root, info, provider, *args):
            """Social Auth decorated function"""

        with self.assertRaises(exceptions.DoAuthError):
            wrapped(self, None, self.info(), 'google-oauth2', 'token')

    @social_auth_mock
    def test_social_auth_thenable(self, *args):

        @decorators.social_auth
        def wrapped(cls, root, info, provider, *args):
            return Promise()

        result = wrapped(TestCase, None, self.info(), 'google-oauth2', 'token')

        self.assertTrue(is_thenable(result))
