from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.dipendente import Dipendente

class DipendenteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dipendente
        include_relationships = True
        load_instance = True

dipendente_schema = DipendenteSchema()
dipendenti_schema = DipendenteSchema(many=True)