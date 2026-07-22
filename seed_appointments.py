from app import app
from database import db
from models import Appointment


with app.app_context():

    if Appointment.query.count() == 0:

        appointments = [
            Appointment(
                date="23/07/2026",
                time="14:00",
                patient="Ana Silva",
                cpf="123.456.789-00",
                doctor="Dr. João",
                specialty="Cardiologia",
                insurance="Unimed",
                status="Confirmado"
            ),
            Appointment(
                date="24/07/2026",
                time="09:30",
                patient="Pedro Lima",
                cpf="987.654.321-00",
                doctor="Dra. Maria",
                specialty="Dermatologia",
                insurance="Amil",
                status="Pendente"
            ),
            Appointment(
                date="25/07/2026",
                time="11:00",
                patient="Carla Souza",
                cpf="456.789.123-00",
                doctor="Dr. Carlos",
                specialty="Ortopedia",
                insurance="Particular",
                status="Cancelado"
            )
        ]

        db.session.add_all(appointments)
        db.session.commit()

        print("Agendamentos cadastrados com sucesso.")

    else:
        print("Os agendamentos já foram cadastrados.")