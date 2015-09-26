# -*- coding: utf-8 -*-

from flask import url_for

from ..helpers import check_is_equal, login, with_tst_request_context, with_tst_client, with_tst_user


@with_tst_request_context
@with_tst_client
def test_help_login_required(*args, **kwargs):
    test_client = kwargs["test_client"]

    response = test_client.get(url_for("help.help"))
    check_is_equal(response.status_code, 302)

    location = response.headers["Location"]
    assert location.startswith("http://localhost:8443/user/register?"), location


@with_tst_request_context
@with_tst_client
@with_tst_user
def test_help_help_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]

    login(test_client, test_user)

    response = test_client.get(url_for("help.help"))
    check_is_equal(response.status_code, 200)
