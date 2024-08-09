#!/usr/bin/env python3
""" session auth view """
from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ auth session login """
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not passwd or passwd == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(passwd):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    user = users[0]
    session_id = auth.create_session(user.id)
    SESSION_NAME = os.getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """ DELETE /api/v1/auth_session/logout """
    from api.v1.app import auth
    deleted = auth.destroy_session(request)
    if not deleted:
        abort(404)
    return jsonify({}), 200
