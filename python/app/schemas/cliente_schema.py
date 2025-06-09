from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.cliente import Cliente

class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_relationships = True
        load_instance = True

cliente_schema = ClienteSchema()
clienti_schema = ClienteSchema(many=True)