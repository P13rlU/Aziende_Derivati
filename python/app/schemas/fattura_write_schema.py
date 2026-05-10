from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.fattura import Fattura

class FatturaWriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fattura
        load_instance = False
        include_fk = True

fattura_write_schema = FatturaWriteSchema()