# -*- coding: utf-8 -*-

from ..helpers import check_is_equal, url_for, login, with_tst_request_context, with_tst_client, with_tst_user


@with_tst_request_context
@with_tst_client
def test_account_login_required(*args, **kwargs):
    test_client = kwargs["test_client"]

    response = test_client.get(url_for("account.account"))
    check_is_equal(response.status_code, 302)

    location = response.headers["Location"]
    assert location.startswith("http://localhost:8443/user/register?"), location


@with_tst_request_context
@with_tst_client
@with_tst_user
def test_account_login_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]

    login(test_client, test_user)

    response = test_client.get(url_for("account.account"))
    check_is_equal(response.status_code, 200)


@with_tst_request_context
@with_tst_client
@with_tst_user
def test_account_credit_purchase_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]

    login(test_client, test_user)

    response = test_client.post(url_for("account.account"), data=dict(stripeToken="tok_amex"))
    check_is_equal(response.status_code, 200)
