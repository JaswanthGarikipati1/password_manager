# app/middleware.py
from flask import request, redirect, url_for, session
import logging

def login_required_middleware(app):
    @app.before_request
    def check_login():
        logging.info(f'Request to endpoint: {request.endpoint}, Session: {session}')

        if request.endpoint and request.endpoint.startswith('password_manager.') and 'admin_authenticated' not in session:
            logging.warning(f'Redirecting to login. Endpoint: {request.endpoint}, Session: {session}')
            return redirect(url_for('password_manager.admin_login'))
