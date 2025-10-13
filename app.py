from app import app
from db import db
from login import lm
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='config.env')

# Configurações do Flask
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB-URL')
app.config['SECRET_KEY'] = os.getenv('SECRET-KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
db.init_app(app)
lm.init_app(app)
lm.login_view = 'login'

# 🔹 Importa modelos e rotas **depois** de inicializar db
import models
import routes

# 🔹 Cria tabelas no contexto do app (funciona com Gunicorn)
def create_tables():
    with app.app_context():
        db.create_all()

# Chama a função para garantir que as tabelas existam
create_tables()

# Apenas para desenvolvimento local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.getenv('DEBUG') == "True"
    app.run(host="0.0.0.0", port=port, debug=debug)