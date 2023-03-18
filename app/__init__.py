import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "student_management.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import students
    app.register_blueprint(students.bp)

    from . import courses
    app.register_blueprint(courses.bp)

    from . import grades
    app.register_blueprint(grades.bp)

    from . import course_students
    app.register_blueprint(course_students.bp)

    return app
