from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.dipendente import Dipendente

class DipendenteWriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dipendente
        load_instance = False  # ❌ No caricamento istanza

dipendente_write_schema = DipendenteWriteSchema()