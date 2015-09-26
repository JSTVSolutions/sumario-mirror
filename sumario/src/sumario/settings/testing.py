# -*- coding: utf-8 -*-

from .common import *


DEBUG = True
TESTING = True

SENTRY_ENVIRONMENT = "testing"

SERVER_NAME = "localhost:8443"

USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ["plaintext"]

WTF_CSRF_ENABLED = False
