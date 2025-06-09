from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.fattura import Fattura

class FatturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fattura
        include_relationships = True
        load_instance = True

fattura_schema = FatturaSchema()
fatture_schema = FatturaSchema(many=True)