# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as BS

from sumario.components import db
from sumario.models import Relay

from ..helpers import (
    check_is_equal,
    url_for,
    login,
    with_tst_request_context,
    with_tst_client,
    with_tst_relay,
    with_tst_user,
)


def _get_value(elem):
    value = elem.string if elem.string else elem["value"]
    return value.strip()


@with_tst_request_context
@with_tst_client
def test_dashboard_login_required(*args, **kwargs):
    test_client = kwargs["test_client"]

    response = test_client.get(url_for("dashboard.dashboard"))
    check_is_equal(response.status_code, 302)

    location = response.headers["Location"]
    assert location.startswith("http://localhost:8443/user/register?"), location


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_login_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]

    login(test_client, test_user)

    response = test_client.get(url_for("dashboard.dashboard"))
    check_is_equal(response.status_code, 200)

    bs = BS(response.data, "html5lib")
    check_is_equal(bs.find(id="hi").string.strip(), "Hi, {}".format(test_user.email))

    for send_to_kind in ["list-relay-form-send-to"]:
        send_to_list = [_get_value(elem) for elem in bs.find_all(class_=send_to_kind)]
        check_is_equal(len(send_to_list), 1)
        check_is_equal(send_to_list[0], test_user.email)

    for send_to_kind in ["list-relay-form-name", "example-form-name"]:
        send_to_list = [_get_value(elem) for elem in bs.find_all(class_=send_to_kind)]
        check_is_equal(len(send_to_list), 1)
        check_is_equal(send_to_list[0], "Test Relay")


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_create_new_relay_has_errors(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    data = {
        "new-relay-new_relay": True,
        "new-relay-send_to": "invalid-email-address",
        "new-relay-success_url": test_relay.success_url,
    }

    response = test_client.post(url_for("dashboard.dashboard"), data=data)
    check_is_equal(response.status_code, 200)

    bs = BS(response.data, "html5lib")
    check_is_equal(bs.find(id="hi").string.strip(), "Hi, {}".format(test_user.email))

    for send_to_kind in ["list-relay-form-send-to"]:
        send_to_list = [_get_value(elem) for elem in bs.find_all(class_=send_to_kind)]
        check_is_equal(len(send_to_list), 1)
        check_is_equal(send_to_list[0], test_user.email)

    for send_to_kind in ["list-relay-form-name", "example-form-name"]:
        send_to_list = [_get_value(elem) for elem in bs.find_all(class_=send_to_kind)]
        check_is_equal(len(send_to_list), 1)
        check_is_equal(send_to_list[0], "Test Relay")


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_create_new_relay_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    name = "Test Relay"
    send_to = "tvaughan@foobar.mil"

    data = {
        "new-relay-new_relay": True,
        "new-relay-name": name,
        "new-relay-send_to": send_to,
        "new-relay-success_url": test_relay.success_url,
    }

    response = test_client.post(url_for("dashboard.dashboard"), data=data)
    check_is_equal(response.status_code, 200)

    bs = BS(response.data, "html5lib")
    check_is_equal(bs.find(id="hi").string.strip(), "Hi, {}".format(test_user.email))

    for send_to_kind in ["list-relay-form-send-to"]:
        send_to_list = [_get_value(elem) for elem in bs.find_all(class_=send_to_kind)]
        check_is_equal(len(send_to_list), 2)
        check_is_equal(send_to_list[0], send_to)
        check_is_equal(send_to_list[1], test_user.email)

    for send_to_kind in ["list-relay-form-name", "example-form-name"]:
        send_to_list = [_get_value(elem) for elem in bs.find_all(class_=send_to_kind)]
        check_is_equal(len(send_to_list), 2)
        check_is_equal(send_to_list[0], "Test Relay")


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_update_relay_invalid_send_to(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    send_to = "this is not a valid email address"
    success_url = url_for("submission.success")

    data = {
        "edit-relay-edit_buttons-update_relay": True,
        "edit-relay-send_to": send_to,
        "edit-relay-success_url": success_url,
    }

    response = test_client.post(url_for("dashboard.edit", uuid=test_relay.uuid), data=data)
    check_is_equal(response.status_code, 200)

    bs = BS(response.data, "html5lib")
    check_is_equal(bs.find(id="hi").string.strip(), "Hi, {}".format(test_user.email))

    send_to_list = [_get_value(elem) for elem in bs.find_all(class_="edit-relay-form-send-to")]
    check_is_equal(len(send_to_list), 1)
    check_is_equal(send_to_list[0], send_to)

    # Double-check that relay **HAS NOT BEEN** updated.
    relay = db.session.get(Relay, test_relay.uuid)
    check_is_equal(relay.send_to, test_user.email)
    check_is_equal(relay.success_url, test_relay.success_url)


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_update_relay_get_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    response = test_client.get(url_for("dashboard.edit", uuid=test_relay.uuid))
    check_is_equal(response.status_code, 200)


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_update_relay_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    send_to = "foobar@hotmail.mil"
    success_url = url_for("submission.success")

    data = {
        "edit-relay-edit_buttons-update_relay": True,
        "edit-relay-send_to": send_to,
        "edit-relay-success_url": success_url,
    }

    response = test_client.post(url_for("dashboard.edit", uuid=test_relay.uuid), data=data)
    check_is_equal(response.status_code, 302)
    check_is_equal(response.headers["Location"], url_for("dashboard.dashboard"))

    # Double-check that relay **HAS BEEN** updated.
    relay = db.session.get(Relay, test_relay.uuid)
    check_is_equal(relay.send_to, send_to)
    check_is_equal(relay.success_url, success_url)


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_delete_relay_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    data = {"edit-relay-edit_buttons-delete_relay": True}

    response = test_client.post(url_for("dashboard.edit", uuid=test_relay.uuid), data=data)
    check_is_equal(response.status_code, 302)
    check_is_equal(response.headers["Location"], url_for("dashboard.dashboard"))

    # Double-check that relay **HAS BEEN** deleted.
    check_is_equal(db.session.get(Relay, test_relay.uuid).deleted, True)


@with_tst_request_context
@with_tst_client
@with_tst_user
@with_tst_relay
def test_dashboard_undelete_relay_ok(*args, **kwargs):
    test_client = kwargs["test_client"]
    test_user = kwargs["test_user"]
    test_relay = kwargs["test_relay"]

    login(test_client, test_user)

    check_is_equal(test_relay.deleted, False)

    test_relay.deleted = True
    db.session.add(test_relay)
    db.session.commit()

    # Double-check that relay **HAS BEEN** deleted.
    check_is_equal(db.session.get(Relay, test_relay.uuid).deleted, True)

    response = test_client.get(url_for("dashboard.undelete", uuid=test_relay.uuid))
    check_is_equal(response.status_code, 302)
    check_is_equal(response.headers["Location"], url_for("dashboard.dashboard"))

    # Double-check that relay **HAS BEEN** undeleted.
    check_is_equal(db.session.get(Relay, test_relay.uuid).deleted, False)
