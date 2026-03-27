# ─────────────────────────────────────────────────────────────
# app.py — Application Entry Point
# Author : Atharva
# Attendify v1.1 | B.Tech Software Engineering Lab | CSE-A Sem IV
# ─────────────────────────────────────────────────────────────

import os, datetime
from flask import Flask
from routes import register_blueprints
from routes.utils import get_db


def create_app():
    app = Flask(__name__)
    app.secret_key = 'attendify-secret-key-2026-se-lab'
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)

    # Register all feature blueprints
    register_blueprints(app)

    # Inject current datetime into every template
    @app.context_processor
    def inject_now():
        return {'now': datetime.datetime.now().strftime('%d %b %Y, %H:%M')}

    return app


def init_db(app):
    """Create tables from schema.sql if DB does not exist."""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'attendify.db')
    os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)
    if not os.path.exists(db_path):
        with app.app_context():
            db = get_db()
            schema = open(os.path.join(os.path.dirname(__file__), 'schema.sql')).read()
            db.executescript(schema)
            db.commit()
            db.close()


app = create_app()

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True, port=5000)
