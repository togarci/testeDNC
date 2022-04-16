from src import app, db
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

from src.model import Usuario, Ponto
from src.conttroller.API import UserConttroller, PontoConttroller

Migrate(app, db)

app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(UserConttroller.bp)
app.register_blueprint(PontoConttroller.bp)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
