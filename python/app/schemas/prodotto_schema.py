from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.prodotto import Prodotto

class ProdottoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prodotto
        include_relationships = True
        load_instance = True

prodotto_schema = ProdottoSchema()
prodotti_schema = ProdottoSchema(many=True)