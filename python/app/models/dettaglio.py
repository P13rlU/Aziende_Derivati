from sqlalchemy.orm import relationship
from app.extensions import db

class Dettaglio(db.Model):
    __tablename__ = 'A_DETTAGLIO'

    id_fattura = db.Column(db.String(25), db.ForeignKey('A_FATTURA.id_fattura'), primary_key=True)
    prodotto = db.Column(db.String(100), db.ForeignKey('A_PRODOTTO.nome'), primary_key=True)
    quantita = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Numeric(10, 2), nullable=False)

    fattura = relationship("Fattura", back_populates="dettagli")
    prodotto_ref = relationship("Prodotto", back_populates="dettagli")
