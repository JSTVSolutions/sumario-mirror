# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as _

from flask_wtf import FlaskForm

from wtforms.fields import BooleanField, EmailField, FormField, StringField, SubmitField
from wtforms.form import Form
from wtforms.validators import DataRequired, Email


class ReadOnlyWidgetProxy(object):
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, attr):
        return getattr(self.widget, attr)

    def __call__(self, *args, **kwargs):
        kwargs["readonly"] = True
        return self.widget(*args, **kwargs)


class NewRelayForm(FlaskForm):
    name = StringField(_("Name"), validators=[DataRequired()], render_kw={"class": "input is-fullwidth"})
    send_to = EmailField(
        _("Send to"), validators=[DataRequired(), Email()], render_kw={"class": "input is-fullwidth"}
    )
    success_url = StringField(
        _("Success URL"), validators=[DataRequired()], render_kw={"class": "input is-fullwidth"}
    )
    toggle_success_url = BooleanField(
        _("Use default success url"), render_kw={"class": "checkbox toggle-success-url-checkbox"}
    )
    new_relay = SubmitField(_("Create new relay"), render_kw={"class": "button is-fullwidth is-primary"})


class ListRelayForm(FlaskForm):
    name = StringField(
        _("Name"),
        validators=[DataRequired()],
        render_kw={"class": "input is-fullwidth list-relay-form-name", "readonly": True},
    )
    send_to = EmailField(
        _("Send to"),
        validators=[DataRequired(), Email()],
        render_kw={"class": "input is-fullwidth list-relay-form-send-to", "readonly": True},
    )
    success_url = StringField(
        _("Success URL"),
        validators=[DataRequired()],
        render_kw={"class": "input is-fullwidth", "readonly": True},
    )


class EditButtons(Form):
    update_relay = SubmitField(_("Update"), render_kw={"class": "button is-fullwidth is-primary"})
    delete_relay = SubmitField(_("Delete"), render_kw={"class": "button is-fullwidth"})


class EditRelayForm(FlaskForm):
    name = StringField(_("Name"), validators=[DataRequired()], render_kw={"class": "input is-fullwidth"})
    send_to = EmailField(
        _("Send to"),
        validators=[DataRequired(), Email()],
        render_kw={"class": "input is-fullwidth edit-relay-form-send-to"},
    )
    success_url = StringField(
        _("Success URL"), validators=[DataRequired()], render_kw={"class": "input is-fullwidth"}
    )
    toggle_success_url = BooleanField(
        _("Use default success url"), render_kw={"class": "checkbox toggle-success-url-checkbox"}
    )

    edit_buttons = FormField(EditButtons)
