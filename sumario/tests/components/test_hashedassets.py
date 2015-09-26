# -*- coding: utf-8 -*-

import os.path
import uuid

from importlib.resources import as_file, files

from flask import render_template
from flask.testing import FlaskCliRunner

import pytest

from sumario.components import hashed_assets
from sumario.components.hashedassets import HashedAssetNotFoundError

from ..helpers import with_tst_request_context


def _get_resource(path, name):
    importable = files(path).joinpath(name)
    with as_file(importable) as resource:
        return resource


@pytest.mark.xfail(raises=HashedAssetNotFoundError)
@with_tst_request_context
def test_hashed_asset_not_found_error(*args, **kwargs):
    test_app = kwargs["test_app"]

    hashed_assets.init_app(test_app)

    assert render_template("tests/sumario/hashedassets/hashed-asset-not-found.html")


@with_tst_request_context
def test_hash_assets_command(*args, **kwargs):
    test_app = kwargs["test_app"]

    catalog_name = str(uuid.uuid4()).split("-")[0] + ".yml"
    test_app.config["HASHEDASSETS_CATALOG_NAME"] = catalog_name

    resource_path = "sumario.tests.components"
    test_app.config["HASHEDASSETS_RESOURCE_PATH"] = resource_path

    resource = _get_resource(resource_path, catalog_name)
    assert os.path.exists(resource) is False

    rc = FlaskCliRunner(test_app).invoke(args=["hash-assets"])
    assert rc.exit_code == 0

    assert os.path.exists(resource) is True
