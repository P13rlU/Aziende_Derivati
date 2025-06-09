from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.gestione import Gestione

class GestioneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Gestione
        include_relationships = True
        load_instance = True

gestione_schema = GestioneSchema()
gestioni_schema = GestioneSchema(many=True)