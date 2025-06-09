from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.prodotto import Prodotto

class ProdottoWriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prodotto
        load_instance = False

prodotto_write_schema = ProdottoWriteSchema()