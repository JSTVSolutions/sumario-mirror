# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from flask_user import login_required

help_blueprint = Blueprint("help", __name__)


@help_blueprint.route("/", methods=["GET"])
@login_required
def help():
    return render_template("sumario/help.html")
