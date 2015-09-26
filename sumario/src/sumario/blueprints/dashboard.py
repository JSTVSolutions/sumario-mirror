# -*- coding: utf-8 -*-

from flask import Blueprint, flash, redirect, request, render_template, url_for

from flask_babel import lazy_gettext as _

from flask_user import current_user, login_required

from ..components import db
from ..forms import EditRelayForm, ListRelayForm, NewRelayForm, ReadOnlyWidgetProxy
from ..models import Relay

dashboard_blueprint = Blueprint("dashboard", __name__)


def _get_dashboard_template(relays):
    return "sumario/dashboard-{}.html".format("n" if len(relays) else "0")


def _list_relay_form_model(relay):
    return ListRelayForm(formdata=None, obj=relay, prefix="list-relay"), relay


@dashboard_blueprint.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    new_relay_form = NewRelayForm(prefix="new-relay", formdata=request.form)
    if new_relay_form.validate_on_submit():
        new_relay = Relay()
        new_relay.name = new_relay_form.name.data
        new_relay.send_to = new_relay_form.send_to.data
        new_relay.success_url = new_relay_form.success_url.data
        new_relay.user_uuid = current_user.uuid
        db.session.add(new_relay)
        db.session.commit()
        flash(_("Cool! The relay has been created and is ready to use."), "warning")

    if not new_relay_form.errors:
        new_relay_form.send_to.data = current_user.email
        new_relay_form.name.data = None
        new_relay_form.success_url.data = None
        new_relay_form.toggle_success_url.data = False

    default_success_url = url_for("submission.success")

    relays = current_user.relays.filter_by(deleted=False).order_by(Relay.created_at.desc()).all()

    list_relay_forms_models = [_list_relay_form_model(relay) for relay in relays]

    extra_context = {
        "default_success_url": default_success_url,
        "new_relay_form": new_relay_form,
        "relays": relays,
        "list_relay_forms_models": list_relay_forms_models,
    }

    return render_template(_get_dashboard_template(relays), **extra_context)


@dashboard_blueprint.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid):
    relay = db.session.get(Relay, uuid)

    edit_relay_form = EditRelayForm(prefix="edit-relay", formdata=request.form, obj=relay)

    if edit_relay_form.edit_buttons.delete_relay.data:
        relay.deleted = True
        db.session.add(relay)
        db.session.commit()
        flash(
            '<div class="is-grouped"><p>{}<strong><a href="{}">{}</a></strong></p></div>'.format(
                _("The relay has been deleted. Was this a mistake? Fear not!"),
                url_for("dashboard.undelete", uuid=relay.uuid),
                _("Click to undelete"),
            ),
            "warning",
        )
        return redirect(url_for("dashboard.dashboard"))

    if edit_relay_form.edit_buttons.update_relay.data:
        if edit_relay_form.validate_on_submit():
            relay.send_to = edit_relay_form.send_to.data
            relay.name = edit_relay_form.name.data
            relay.success_url = edit_relay_form.success_url.data
            db.session.add(relay)
            db.session.commit()
            flash(_("Cool! The relay has been updated. The changes are in full effect."), "warning")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash(_("Oops! Please correct the errors below and then re-submit."), "warning")

    default_success_url = url_for("submission.success")

    if edit_relay_form.success_url.data == default_success_url:
        edit_relay_form.success_url.widget = ReadOnlyWidgetProxy(edit_relay_form.success_url.widget)
        edit_relay_form.toggle_success_url.data = True

    extra_context = {"default_success_url": default_success_url, "edit_relay_form": edit_relay_form}

    return render_template("sumario/dashboard-edit.html", **extra_context)


@dashboard_blueprint.route("/<uuid>/undelete", methods=["GET"])
@login_required
def undelete(uuid):
    relay = db.session.get(Relay, uuid)
    relay.deleted = False
    db.session.add(relay)
    db.session.commit()
    flash(_("Cool! The relay has been undeleted and is ready to use."), "warning")
    return redirect(url_for("dashboard.dashboard"))
