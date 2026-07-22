from flask import Flask, render_template, request, redirect, jsonify
from database import db
from models import User, Appointment
import os
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///agenda.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "123456"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template(
            "login.html",
            error="Preencha o e-mail e a senha."
        )

    try:
        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="E-mail ou senha inválidos."
        )

    except SQLAlchemyError:
        db.session.rollback()

        app.logger.exception(
            "Erro ao consultar usuário no banco de dados."
        )

        return render_template(
            "login.html",
            error="Não foi possível acessar o sistema. Tente novamente."
        ), 503

    except Exception:
        app.logger.exception(
            "Erro inesperado durante o login."
        )

        return render_template(
            "login.html",
            error="Não foi possível realizar o login. Tente novamente."
        ), 500
    
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/appointments")
def appointments():
    try:
        appointments_list = Appointment.query.all()

        dados = []

        for appointment in appointments_list:
            dados.append({
                "id": appointment.id,
                "date": appointment.date,
                "time": appointment.time,
                "patient": appointment.patient,
                "cpf": appointment.cpf,
                "doctor": appointment.doctor,
                "specialty": appointment.specialty,
                "insurance": appointment.insurance,
                "status": appointment.status
            })

        return jsonify(dados), 200

    except SQLAlchemyError:
        db.session.rollback()

        app.logger.exception(
            "Erro de conexão ou consulta ao banco de dados."
        )

        return jsonify({
            "error": "Não foi possível acessar o banco de dados."
        }), 503

    except Exception:
        app.logger.exception(
            "Erro inesperado ao carregar os agendamentos."
        )

        return jsonify({
            "error": "A API está temporariamente indisponível."
        }), 500
    
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "0") == "1"
    )