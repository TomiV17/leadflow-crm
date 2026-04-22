from flask import Flask
from app.database import init_db
from app.routes import leads_bp

def create_app():
    app = Flask(__name__)

    # Inicializar base de datos
    init_db()

    # Registrar rutas
    app.register_blueprint(leads_bp, url_prefix="/leads")

    return app
