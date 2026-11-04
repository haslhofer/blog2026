import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from flask import redirect

from app import ALLOWED_LOGIN_EMAIL, app, microsoft


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.original_config = {
            key: app.config[key]
            for key in (
                "MICROSOFT_CLIENT_ID",
                "MICROSOFT_CLIENT_SECRET",
                "MICROSOFT_REDIRECT_URI",
                "SECRET_KEY",
                "AUTH_SECRET_KEY_CONFIGURED",
                "SESSION_COOKIE_SECURE",
                "TESTING",
            )
        }
        app.config.update(
            MICROSOFT_CLIENT_ID="test-client-id",
            MICROSOFT_CLIENT_SECRET="test-client-secret",
            MICROSOFT_REDIRECT_URI="https://example.test/auth/callback",
            SECRET_KEY="test-session-secret",
            AUTH_SECRET_KEY_CONFIGURED=True,
            SESSION_COOKIE_SECURE=False,
            TESTING=True,
        )
        self.client = app.test_client()

    def tearDown(self):
        app.config.update(self.original_config)

    def test_protected_page_redirects_to_login_with_return_path(self):
        response = self.client.get("/us-options")

        self.assertEqual(response.status_code, 302)
        location = urlsplit(response.location)
        self.assertEqual(location.path, "/login")
        self.assertEqual(parse_qs(location.query)["next"], ["/us-options"])

    def test_every_nonpublic_page_requires_login_by_default(self):
        public_endpoints = {
            "index",
            "auth_login",
            "auth_callback",
            "city_comparison_login",
            "logout",
            "static",
        }
        protected_paths = {
            rule.rule
            for rule in app.url_map.iter_rules()
            if "GET" in rule.methods
            and rule.endpoint not in public_endpoints
            and "<" not in rule.rule
        }

        self.assertGreater(len(protected_paths), 0)
        for path in protected_paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(urlsplit(response.location).path, "/login")

    def test_homepage_hides_protected_page_links_until_signed_in(self):
        response = self.client.get("/")

        self.assertIn(b"Sign in", response.data)
        self.assertIn(b"Sign in to browse the blog pages.", response.data)
        self.assertNotIn(b"class=\"page-card\"", response.data)
        self.assertNotIn(b"Pages", response.data)
        self.assertNotIn(b"US Options to Move To", response.data)
        self.assertNotIn(b"Where Should We Live?", response.data)

        with self.client.session_transaction() as browser_session:
            browser_session["authenticated_email"] = ALLOWED_LOGIN_EMAIL

        response = self.client.get("/")

        self.assertIn(b"Sign out", response.data)
        self.assertIn(b"class=\"page-card\"", response.data)
        self.assertIn(b"Steppr Architecture", response.data)
        self.assertIn(b"US Options to Move To", response.data)
        self.assertIn(b"Where Should We Live?", response.data)

    def test_login_starts_microsoft_authorization_and_remembers_safe_path(self):
        with patch.object(
            microsoft,
            "authorize_redirect",
            return_value=redirect("https://login.microsoftonline.com/"),
        ) as authorize_redirect:
            response = self.client.get("/login?next=%2Fus-options")

        self.assertEqual(response.status_code, 302)
        authorize_redirect.assert_called_once_with(
            "https://example.test/auth/callback", prompt="select_account"
        )
        with self.client.session_transaction() as browser_session:
            self.assertEqual(browser_session["post_login_redirect"], "/us-options")

    def test_login_discards_external_return_urls(self):
        with patch.object(
            microsoft,
            "authorize_redirect",
            return_value=redirect("https://login.microsoftonline.com/"),
        ):
            self.client.get("/login?next=https%3A%2F%2Fevil.example")

        with self.client.session_transaction() as browser_session:
            self.assertEqual(browser_session["post_login_redirect"], "/")

    def test_allowed_microsoft_account_can_access_protected_page(self):
        with self.client.session_transaction() as browser_session:
            browser_session["post_login_redirect"] = "/us-options"

        with patch.object(
            microsoft,
            "authorize_access_token",
            return_value={"userinfo": {"email": ALLOWED_LOGIN_EMAIL.upper()}},
        ):
            response = self.client.get("/auth/callback")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response.location).path, "/us-options")
        self.assertEqual(self.client.get("/us-options").status_code, 200)

    def test_other_microsoft_account_is_denied(self):
        with patch.object(
            microsoft,
            "authorize_access_token",
            return_value={"userinfo": {"email": "someone@example.com"}},
        ):
            response = self.client.get("/auth/callback")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"haslhofer@outlook.com", response.data)
        self.assertEqual(self.client.get("/us-options").status_code, 302)

    def test_login_shows_configuration_error_when_required_settings_are_missing(self):
        app.config.update(AUTH_SECRET_KEY_CONFIGURED=False)

        response = self.client.get("/login")

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"not configured", response.data)

    def test_logout_clears_the_authenticated_session(self):
        with self.client.session_transaction() as browser_session:
            browser_session["authenticated_email"] = ALLOWED_LOGIN_EMAIL

        response = self.client.get("/logout")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get("/us-options").status_code, 302)


if __name__ == "__main__":
    unittest.main()
