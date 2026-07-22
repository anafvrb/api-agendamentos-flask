from app import app
from database import db
from models import User

with app.app_context():

    user = User(
        email="admin@test.com",
        password="123456"
    )

    db.session.add(user)
    db.session.commit()

    print("Usuário criado com sucesso!")