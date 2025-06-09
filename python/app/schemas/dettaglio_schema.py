from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.dettaglio import Dettaglio

class DettaglioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dettaglio
        include_relationships = True
        load_instance = True

dettaglio_schema = DettaglioSchema()
dettagli_schema = DettaglioSchema(many=True)