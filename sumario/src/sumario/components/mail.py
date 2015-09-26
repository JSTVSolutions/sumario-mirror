# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as _

from flask_mail import Mail, Message


mail = Mail()


__init__ = Message.__init__


def _init(*args, **kwargs):
    kwargs["extra_headers"] = {"X-PM-Message-Stream": "outbound"}
    return __init__(*args, **kwargs)


Message.__init__ = _init


def send_message(to, body, html=None):
    options = {"body": body, "html": html, "recipients": [to], "sender": "submissions@sumar.io"}
    return mail.send(Message(_("Form submission from Sumario"), **options))
