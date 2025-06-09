from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from app.extensions import db

class Dipendente(db.Model):
    __tablename__ = 'A_DIPENDENTE'

    id_dipendente = db.Column(db.String(25), primary_key=True)
    nome = db.Column(db.String(50), nullable=True)
    cognome = db.Column(db.String(50), nullable=True)
    stipendio = db.Column(db.Numeric(10, 2), default=0)
    settore = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=True)

    __table_args__ = (
        CheckConstraint("settore IN ('produzione', 'vendita', 'direzione', 'Controllo Qualità')", name="check_settore"),
        CheckConstraint("categoria IN ('latte', 'carne', 'grano')", name="check_categoria"),
    )

    fatture = relationship("Fattura", back_populates="venditore")
