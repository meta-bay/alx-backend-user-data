#!/usr/bin/env python3
""" flask app module """
from flask import Flask, jsonify, request, abort, redirect
import requests
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def message():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """ register user 'POST /users' """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify(
            {"email": email, "message": "user created"}
        )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ respond tho the 'POST /sessions route """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """ respond to the DELETE /sessions route """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """ respond to the GET /profile route """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ respond to the POST /reset_password route """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def update_password():
    """ respond to the PUT /reset_password route """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
