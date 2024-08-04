from flask import Flask
from .models import db
from .routes import bp as password_manager_bp
from .middleware import login_required_middleware

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garikipati.db'
    app.config['SECRET_KEY'] = 'VvoogMKIlsEsZ2eHlmXY9Cna_ClMkHiCjJAdfpCTTc0='
    #login_required_middleware(app)
    db.init_app(app)
    app.register_blueprint(password_manager_bp)
    return app




if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
