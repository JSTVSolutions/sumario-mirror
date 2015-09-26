# -*- coding: utf-8 -*-

import os


SECRET_KEY = os.environ["SECRET_KEY"]

LANGUAGES = {"en": "English", "es": "Español"}

BABEL_TRANSLATION_DIRECTORIES = "translations"

HASHEDASSETS_CATALOG_NAME = "hashedassets.yml"
HASHEDASSETS_RESOURCE_PATH = "sumario.static"
HASHEDASSETS_SRC_DIR = "src/sumario/static/build"
HASHEDASSETS_OUT_DIR = "src/sumario/static/public"
HASHEDASSETS_URL_PREFIX = "/static/"

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ["POSTGRES_USERNAME"],
    os.environ["POSTGRES_PASSWORD"],
    os.environ["POSTGRES_HOSTNAME"],
    os.environ["POSTGRES_TCP_PORT"],
    os.environ["SUMARIO_ENVIRONMENT"],
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
SENTRY_USER_ATTRS = ["email"]

MAIL_DEFAULT_SENDER = "sumario@sumar.io"
MAIL_PASSWORD = os.environ.get("POSTMARK_TOKEN", "")
MAIL_PORT = 587
MAIL_SERVER = "smtp.postmarkapp.com"
MAIL_USERNAME = os.environ.get("POSTMARK_TOKEN", "")
MAIL_USE_SSL = False
MAIL_USE_TLS = True

USER_AFTER_CHANGE_PASSWORD_ENDPOINT = "user.login"  # nosec
USER_AFTER_CHANGE_USERNAME_ENDPOINT = "user.login"
USER_AFTER_CONFIRM_ENDPOINT = "user.login"
USER_AFTER_FORGOT_PASSWORD_ENDPOINT = "user.login"  # nosec
USER_AFTER_LOGIN_ENDPOINT = "dashboard.dashboard"
USER_AFTER_LOGOUT_ENDPOINT = "homepage.homepage"
USER_AFTER_REGISTER_ENDPOINT = "user.login"
USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT = "user.login"
USER_AFTER_RESET_PASSWORD_ENDPOINT = "user.login"  # nosec
USER_APP_NAME = "Sumario"
USER_AUTO_LOGIN = False
USER_AUTO_LOGIN_AFTER_CONFIRM = False
USER_ENABLE_CHANGE_USERNAME = False
USER_ENABLE_CONFIRM_EMAIL = True
USER_ENABLE_USERNAME = False
USER_PROFILE_URL = "/user-profile-disabled"  # Causes 404. TODO: Find a better way to disable this.
USER_REQUIRE_RETYPE_PASSWORD = False
USER_UNAUTHENTICATED_ENDPOINT = "user.register"

STRIPE_PUBKEY = os.environ.get("STRIPE_PUBKEY", "")
STRIPE_SECRET = os.environ.get("STRIPE_SECRET", "")
