import os
import re

from bafser import create_file_response
from flask import Blueprint, abort

blueprint = Blueprint("img", __name__)
reg = re.compile("[0-9a-zA-Z_]+\\.([0-9a-zA-Z]+)")


@blueprint.route("/api/img/<fname>")
def img(fname: str):
    m = reg.match(fname)
    if not m:
        abort(404)

    path = os.path.join("imgs", fname)
    return create_file_response(path, f"image/{m.group(1)}", fname)
