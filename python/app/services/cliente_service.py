from app.models import Cliente
from app.schemas.cliente_write_schema import cliente_write_schema

class ClienteService:
    def __init__(self, db_session=None):
        self.db = db_session

    def get_all_clienti(self, page=1, per_page=10):
        """Retrieve all clients."""
        return Cliente.query.paginate(page=page, per_page=per_page, error_out=False)


    def get_cliente_by_id(self, cliente_id):
        """Retrieve a client by its ID."""
        return Cliente.query.get(cliente_id)

    
    def create_cliente(self, data):
        """Create a new client."""
        try:
            validated_data = cliente_write_schema.load(data)

            cliente = Cliente(**validated_data)

            self.db.session.add(cliente)
            self.db.session.commit()

            return cliente
        except Exception as e:
            self.db.session.rollback()
            raise e

    
    def update_cliente(self, cliente_id, data):
        """Update an existing client."""
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            raise ValueError("Client not found")

        validated_data = cliente_write_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(cliente, key, value)

        self.db.session.commit()
        return cliente

    
    def delete_cliente(self, cliente_id):
        """Delete a client."""
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            raise ValueError("Client not found")

        self.db.session.delete(cliente)
        self.db.session.commit()
        return {"message": "Cliente deleted successfully"}