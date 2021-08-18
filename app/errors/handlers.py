from flask import render_template, request, redirect, url_for
from app import db
from app.errors import bp

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@bp.app_errorhandler(401)
def unauthorized_access_error(error):
    if wants_json_response():
        return {'error': 'unauthorized access'}, 401
    return redirect(url_for('auth.login')), 401

@bp.app_errorhandler(400)
def bad_request_error(error):
    if wants_json_response():
        return {'error': 'bad request'}, 400
    return render_template('errors/400.html', title='400'), 400

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return {'error': 'endpoint not found'}, 404
    return render_template('errors/404.html', title='404'), 404

@bp.app_errorhandler(405)
def method_not_allowed_error(error):
    if wants_json_response():
        return {'error': 'method not allowed'}, 405
    return render_template('errors/405.html', title='405'), 405

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return {'error': 'internal server error'}, 500
    return render_template('errors/500.html', title='500'), 500
