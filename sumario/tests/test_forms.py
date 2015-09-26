# -*- coding: utf-8 -*-

from sumario.forms import NewRelayForm

from .helpers import with_tst_request_context


@with_tst_request_context
def test_new_relay_form(*args, **kwargs):
    new_relay_data = {"send_to": "tvaughan@foobar.mil", "name": "Test Relay", "success_url": "/"}
    new_relay_form = NewRelayForm()
    new_relay_form.process(**new_relay_data)
    assert new_relay_form.validate()
