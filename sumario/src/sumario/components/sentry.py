# -*- coding: utf-8; mode: python -*-

import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration


class Sentry(object):
    def init_app(self, app):
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            environment=app.config["SENTRY_ENVIRONMENT"],
            integrations=[
                FlaskIntegration(),
            ],
        )


sentry = Sentry()
