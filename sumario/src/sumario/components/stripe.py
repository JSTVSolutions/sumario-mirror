# -*- coding: utf-8 -*-

import stripe as _stripe


class Stripe(object):
    def init_app(self, app):
        _stripe.api_key = app.config["STRIPE_SECRET"]
        self.pubkey = app.config["STRIPE_PUBKEY"]

    def __getattr__(self, attr):
        return getattr(_stripe, attr)


stripe = Stripe()
