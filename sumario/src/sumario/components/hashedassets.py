# -*- coding: utf-8 -*-

import hashlib
import os
import os.path

from importlib.resources import as_file, files
from functools import partial

import yaml


def _get_settings(app, namespace, *names):
    return [app.config["{}_{}".format(namespace, name)] for name in names]


def _is_empty(seq):
    return False if seq else True


def _concatpaths(path, *rest):
    if _is_empty(rest):
        return os.path.normpath(path)
    return _concatpaths("{}{}{}".format(path, os.sep, rest[0]), *rest[1:])


def _trimsubpath(subpath, fullpath):
    return fullpath[len(os.path.commonpath([subpath, fullpath])) :]


def _walkdir(src_dir):
    for fullpath_dir, subdirs, filenames in os.walk(src_dir):
        for filename in filenames:
            asset_fullpath = _concatpaths(fullpath_dir, filename)
            asset_partpath = _trimsubpath(src_dir, asset_fullpath)
            yield asset_fullpath, asset_partpath


def _hash(data):
    return hashlib.sha256(data).hexdigest()[:15]


def _make_hashed_name(name, data):
    root, extn = os.path.splitext(name)
    return "{}.{}{}".format(root, _hash(data), extn)


def _get_resource(path, name):
    importable = files(path).joinpath(name)
    with as_file(importable) as resource:
        return resource


def hash_assets(app):
    """Create hashed assets and catalog.

    Args:
      app - The current Flask app instance.

    """
    data = {}
    src_dir, out_dir, url_prefix, catalog_name, resource_path = _get_settings(
        app, "HASHEDASSETS", "SRC_DIR", "OUT_DIR", "URL_PREFIX", "CATALOG_NAME", "RESOURCE_PATH"
    )
    for asset_fullpath, asset_partpath in _walkdir(src_dir):
        with open(asset_fullpath, "rb") as fd:
            asset = fd.read()
        hashed_asset_partpath = _make_hashed_name(asset_partpath, asset)
        hashed_asset_fullpath = _concatpaths(out_dir, hashed_asset_partpath)
        os.makedirs(os.path.dirname(hashed_asset_fullpath), exist_ok=True)
        with open(hashed_asset_fullpath, "wb") as fd:
            fd.write(asset)
        data[asset_partpath] = {"url": _concatpaths(url_prefix, hashed_asset_partpath)}
    with open(_get_resource(resource_path, catalog_name), "w") as fd:
        yaml.dump(data, fd)


class HashedAssetNotFoundError(LookupError):
    pass


def hashed_url_for(data):
    def _hashed_url_for(asset_name):
        if asset_name not in data:
            raise HashedAssetNotFoundError("{} not found in hashed assets catalog".format(asset_name))
        return data[asset_name]["url"]

    return dict(hashed_url_for=_hashed_url_for)


class HashedAssets(object):
    def init_app(self, app):
        catalog_name, resource_path = _get_settings(app, "HASHEDASSETS", "CATALOG_NAME", "RESOURCE_PATH")
        with open(_get_resource(resource_path, catalog_name), "r") as fd:
            data = yaml.safe_load(fd)
        app.context_processor(partial(hashed_url_for, data))


hashed_assets = HashedAssets()
