import datetime
from flask import jsonify


def get_current_time():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def success_response(message='', data=None):
    response = {'status': 'success', 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response)


def error_response(message='', status_code=400):
    response = {'status': 'error', 'message': message}
    return jsonify(response), status_code


def grade_to_quality_points(grade):
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.0
    elif grade == 'C':
        return 2.0
    elif grade == 'D':
        return 1.0
    else:
        return 0.0
