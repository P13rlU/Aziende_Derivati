from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from app.extensions import db


class Fattura(db.Model):
    __tablename__ = 'A_FATTURA'

    id_fattura = db.Column(db.String(25), primary_key=True)
    id_venditore = db.Column(db.String(25), db.ForeignKey('A_DIPENDENTE.id_dipendente'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('A_CLIENTE.id_cliente'), nullable=False)
    data_vendita = db.Column(db.Date, nullable=False)
    totale = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("totale > 0", name="check_totale"),
    )

    venditore = relationship("Dipendente", back_populates="fatture")
    cliente = relationship("Cliente", back_populates="fatture")
    dettagli = relationship("Dettaglio", back_populates="fattura")
