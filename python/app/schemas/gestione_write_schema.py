from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.gestione import Gestione

class GestioneWriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Gestione
        load_instance = False

gestione_write_schema = GestioneWriteSchema()