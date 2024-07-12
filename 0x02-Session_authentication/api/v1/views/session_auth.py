#!/usr/bin/env python3
"""A new flask view that handles all routes for session authenticato"""
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort
import os
from typing import Tuple


@app_views.route(
        '/auth_session/login',
        methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    POST /api/v1/auth_session/login

    Return
    - retrieves email and password
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
