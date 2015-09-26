# -*- coding: utf-8 -*-

import os

from flask_user.forms import RegisterForm
from flask_user.signals import user_registered

import pytest

from sqlalchemy.orm.exc import ObjectDeletedError

from sumario.app import run
from sumario.components import db
from sumario.models import (
    CreditPool,
    CreditPurchase,
    ImmutableError,
    Relay,
    User,
    create_db,
    delete_db,
)

from .helpers import check_is_equal, with_tst_request_context


def _create_user(test_app, email, *args, **kwargs):
    new_user = User()
    new_user.email = email
    new_user.password = "password"  # Do not hash password
    db.session.add(new_user)
    db.session.commit()

    user_registered.send(test_app, user=new_user)

    return new_user


@with_tst_request_context
def test_register_form_password_is_too_short(*args, **kwargs):
    register_data = {
        "email": "foobar@foobar.mil",
        # Password is any string less than 8 characters
        "password": "1234567",
    }
    register_form = RegisterForm()
    register_form.process(**register_data)
    assert register_form.validate() is False
    check_is_equal(register_form.errors, {"password": ["Password must have at least 8 characters"]})


@with_tst_request_context
def test_register_form_password_is_ok(*args, **kwargs):
    register_data = {
        "email": "foobar@foobar.mil",
        # Passwors is any string 8 or more characters
        "password": "12345678",
    }
    register_form = RegisterForm()
    register_form.process(**register_data)
    assert register_form.validate() is True
    check_is_equal(register_form.errors, {})


@pytest.mark.xfail(raises=ObjectDeletedError)
@with_tst_request_context
def test_user_model_is_ok(*args, **kwargs):
    test_app = kwargs["test_app"]
    email = "foobar@example.mil"
    new_user = _create_user(test_app, email)

    user = db.session.get(User, new_user.uuid)
    assert repr(user) == "<User {}>".format(email)
    assert "{}".format(user) == email
    assert user.email == email
    assert user.active is False

    db.session.delete(new_user)
    db.session.commit()

    assert db.session.get(User, new_user.uuid) is None


@pytest.mark.xfail(raises=ObjectDeletedError)
@with_tst_request_context
def test_credit_purchase_model_is_ok(*args, **kwargs):
    test_app = kwargs["test_app"]
    new_user = _create_user(test_app, "foobar@example.mil")

    credit_purchase = db.session.execute(
        db.select(CreditPurchase).filter_by(credit_pool_uuid=new_user.credit_pool.uuid)
    ).scalar_one()
    # credit_purchase = db.session.filter(CreditPurchase, CreditPool.uuid == new_user.credit_pool.uuid).one()
    assert repr(credit_purchase) == "<CreditPurchase {}>".format(credit_purchase.uuid)
    assert "{}".format(credit_purchase) == str(credit_purchase.uuid)
    assert credit_purchase.amount == 0
    assert credit_purchase.credits_purchased == 25
    assert credit_purchase.currency == "FREE!"

    db.session.delete(new_user)
    db.session.commit()

    assert db.session.get(CreditPurchase, credit_purchase.uuid) is None


@pytest.mark.xfail(raises=ObjectDeletedError)
@with_tst_request_context
def test_credit_purchase_model_is_immutable(*args, **kwargs):
    test_app = kwargs["test_app"]
    new_user = _create_user(test_app, "foobar@example.mil")

    credit_purchase = db.session.execute(
        db.select(CreditPurchase).filter_by(credit_pool_uuid=new_user.credit_pool.uuid)
    ).scalar_one()
    # credit_purchase = db.session.filter(CreditPurchase, CreditPool.uuid == new_user.credit_pool.uuid).one()
    credit_purchase.currency = "CLP"
    db.session.add(credit_purchase)

    with pytest.raises(ImmutableError):
        db.session.commit()
    db.session.rollback()

    db.session.delete(new_user)
    db.session.commit()

    assert db.session.get(CreditPurchase, credit_purchase.uuid) is None


@pytest.mark.xfail(raises=ObjectDeletedError)
@with_tst_request_context
def test_credit_pool_model_is_ok(*args, **kwargs):
    test_app = kwargs["test_app"]
    new_user = _create_user(test_app, "foobar@example.mil")

    credit_pool = db.session.get(CreditPool, new_user.credit_pool.uuid)
    assert repr(credit_pool) == "<CreditPool {}>".format(credit_pool.uuid)
    assert "{}".format(credit_pool) == str(credit_pool.uuid)
    assert credit_pool.num_credits == 25

    db.session.delete(new_user)
    db.session.commit()

    assert db.session.get(CreditPool, credit_pool.uuid) is None


@pytest.mark.xfail(raises=ObjectDeletedError)
@with_tst_request_context
def test_relay_model_is_ok(*args, **kwargs):
    test_app = kwargs["test_app"]
    new_user = _create_user(test_app, "foobar@example.mil")

    send_to = "tvaughan@example.mil"
    name = "Test Relay"
    success_url = "/success"
    new_relay = Relay()
    new_relay.name = name
    new_relay.send_to = send_to
    new_relay.success_url = success_url
    new_relay.user_uuid = new_user.uuid
    db.session.add(new_relay)
    db.session.commit()

    relay = db.session.get(Relay, new_relay.uuid)
    assert repr(relay) == "<Relay {}>".format(relay.uuid)
    assert "{}".format(relay) == str(relay.uuid)
    assert relay.name == name
    assert relay.send_to == send_to
    assert relay.success_url == success_url

    db.session.delete(new_user)
    db.session.commit()

    assert db.session.get(Relay, relay.uuid) is None


def test_create_db():
    app = run(os.environ["SUMARIO_ENVIRONMENT"])
    create_db(db, app)
    create_db(db, app)


def test_delete_db():
    app = run(os.environ["SUMARIO_ENVIRONMENT"])
    delete_db(db, app)
    delete_db(db, app)
