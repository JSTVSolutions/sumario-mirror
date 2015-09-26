# -*- coding: utf-8 -*-

from flask import Blueprint, flash, request, render_template

from flask_babel import lazy_gettext as _

from flask_user import current_user, login_required

from ..components import db, stripe
from ..models import CreditPurchase


account_blueprint = Blueprint("account", __name__)

# Amount is in cents USD.
options = [{"amount": 500, "credits": 1000, "currency": "USD"}]


def _charge(option, token):
    customer = stripe.Customer.create(email=current_user.email, source=token)

    credits_purchased = option["credits"]

    charge = stripe.Charge.create(
        amount=option["amount"],
        currency=option["currency"],
        customer=customer.id,
        description=_("{credits_purchased} Sumario Credits").format(credits_purchased=credits_purchased),
    )

    credit_pool = current_user.credit_pool
    db.session.add(credit_pool)

    new_credit_purchase = CreditPurchase()
    db.session.add(new_credit_purchase)

    # TODO: Prevent simultaneous updates. Lock reads.
    credit_pool.num_credits += credits_purchased

    new_credit_purchase.amount = charge.amount
    new_credit_purchase.credits_purchased = credits_purchased
    new_credit_purchase.currency = charge.currency
    new_credit_purchase.credit_pool_uuid = credit_pool.uuid
    new_credit_purchase.tx = charge.id
    new_credit_purchase.user_uuid = current_user.uuid

    db.session.commit()

    amount = "{:.2f}".format(option["amount"] / 100)

    flash(
        _("Cool! You bought an additional {credits} credits for ${amount} {currency}").format(
            credits=option["credits"], amount=amount, currency=option["currency"]
        ),
        "warning",
    )


@account_blueprint.route("/", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        _charge(options[0], request.form["stripeToken"])

    credit_purchases = current_user.credit_pool.credit_purchases.order_by(
        CreditPurchase.created_at.desc()
    ).all()

    extra_context = {"option": options[0], "credit_purchases": credit_purchases, "stripe": stripe}

    return render_template("sumario/account.html", **extra_context)
