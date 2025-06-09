from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship

from app.extensions import db

class Prodotto(db.Model):
    __tablename__ = 'A_PRODOTTO'

    nome = db.Column(db.String(100), primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    costo_di_produzione = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("costo_di_produzione > 0", name="check_costo_di_produzione"),
        CheckConstraint("categoria IN ('latte', 'carne', 'grano')", name="check_categoria_a_prodotto"),
    )

    dettagli = relationship("Dettaglio", back_populates="prodotto_ref")