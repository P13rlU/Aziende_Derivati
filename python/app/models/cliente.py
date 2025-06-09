from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from app.extensions import db

class Cliente(db.Model):
    __tablename__ = 'A_CLIENTE'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    citta = db.Column(db.String(50), nullable=False)
    codice_fiscale = db.Column(db.String(50), nullable=True)

    fatture = relationship("Fattura", back_populates="cliente")
