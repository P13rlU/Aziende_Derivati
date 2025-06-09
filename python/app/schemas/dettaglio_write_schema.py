from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.dettaglio import Dettaglio

class DettaglioWriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dettaglio
        load_instance = False

dettaglio_write_schema = DettaglioWriteSchema()