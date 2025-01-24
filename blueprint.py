from CTFd.utils.decorators import admins_only
from flask import Blueprint, render_template, request

from . import auth
from .db_utils import DBUtils

oauth_bp = Blueprint("oauth2", __name__, template_folder="templates")


def load_bp(plugin_route):
    @oauth_bp.route(plugin_route, methods=["GET"])
    @admins_only
    def get_config():
        config = DBUtils.get_config()
        return render_template("oauth2/config.html", config=config)

    @oauth_bp.route(plugin_route, methods=["POST"])
    @admins_only
    def update_config():
        config = request.form.to_dict()
        del config["nonce"]

        DBUtils.save_config(config.items())
        return render_template("oauth2/config.html", config=DBUtils.get_config())

    @oauth_bp.route("/oauth2/login", methods=["GET"])
    def oauth2_login():
        return auth.oauth2_login()

    @oauth_bp.route("/oauth2/callback", methods=["GET"])
    def oauth2_callback():
        return auth.oauth2_callback()

    return oauth_bp
