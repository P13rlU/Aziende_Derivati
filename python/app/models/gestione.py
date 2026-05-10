from sqlalchemy.orm import relationship
from app.extensions import db

class Gestione(db.Model):
    __tablename__ = 'A_GESTIONE'

    id_dipendente = db.Column(db.String(25), db.ForeignKey('A_DIPENDENTE.id_dipendente', ondelete="SET NULL"), primary_key=True)
    data_assegnazione = db.Column(db.Date, primary_key=True)
    settore = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(20), nullable=True)

    dipendente = relationship("Dipendente")