# Agenda Médica

Aplicação desenvolvida em Flask para gerenciamento de agendamentos médicos.

## Tecnologias

- Python 3.13
- Flask
- SQLite
- SQLAlchemy
- Tabulator
- Pytest
- Docker

---

## Como executar

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Criar banco

```bash
python seed.py
python seed_appointments.py
```

### Executar

```bash
python app.py
```

Acesse:

```
http://127.0.0.1:5000
```

---

## Testes

```bash
python -m pytest -v
```

---

## Estrutura

```
agenda-medica
│
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── Dockerfile
├── README.md
├── seed.py
├── seed_appointments.py
├── tests
├── templates
└── static
```