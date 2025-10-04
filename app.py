from app import app
from db import db
from login import lm
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key='segredo'
lm.init_app(app)
db.init_app(app)
lm.login_view='login'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
