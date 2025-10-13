from app import app
from db import db
from login import lm
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv(dotenv_path='config.env')

# Configurações do Flask
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB-URL')
app.config['SECRET_KEY'] = os.getenv('SECRET-KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
lm.init_app(app)
lm.login_view = 'login'
db.init_app(app)

# Importa modelos e rotas **depois** de inicializar o db
import models
import routes

# Cria tabelas sempre que o app é importado (funciona no Gunicorn)
with app.app_context():
    db.create_all()

# Apenas para desenvolvimento local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.getenv('DEBUG') == "True"  # converte string para boolean
    app.run(host="0.0.0.0", port=port, debug=debug)
