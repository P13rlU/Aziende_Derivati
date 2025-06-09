from sqlalchemy import cast, Date

from app.models import Fattura
from app.schemas.fattura_write_schema import fattura_write_schema
from datetime import datetime

class FatturaService:

    def __init__(self, db_session=None):
        self.db = db_session
    
    def get_all_fatture(self, page=1, per_page=10):
        """Retrieve all invoices."""
        return Fattura.query.paginate(page=page, per_page=per_page, error_out=False)

    
    def get_fattura_by_id(self, fattura_id):
        """Retrieve an invoice by its ID."""
        return Fattura.query.get(fattura_id)

    
    def create_fattura(self, data):
        """Create a new invoice."""
        try:
            validated_data = fattura_write_schema.load(data)

            fattura = Fattura(**validated_data)

            self.db.session.add(fattura)
            self.db.session.commit()

            return fattura
        except Exception as e:
            self.db.session.rollback()
            raise e

    
    def update_fattura(self, fattura_id, data):
        """Update an existing invoice."""
        fattura = Fattura.query.get(fattura_id)
        if not fattura:
            raise ValueError("Invoice not found")

        validated_data = fattura_write_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(fattura, key, value)

        self.db.session.commit()
        return fattura

    
    def delete_fattura(self, fattura_id):
        """Delete an invoice."""
        fattura = Fattura.query.get(fattura_id)
        if not fattura:
            raise ValueError("Invoice not found")

        self.db.session.delete(fattura)
        self.db.session.commit()
        return {"message": "Invoice deleted successfully"}

    def search_fatture(self, id_cliente=None, id_venditore=None, data_vendita=None, page=1, per_page=10):
        """
        Cerca fatture per id_cliente, id_venditore p data_vendita.
        Puó usare piú filtri contemporaneamente.
        """

        query = Fattura.query

        if id_cliente:
            query=query.filter(Fattura.id_cliente==id_cliente)

        if id_venditore:
            query=query.filter(Fattura.id_venditore==id_venditore)

        if data_vendita:
            try:
                parsed_date = datetime.strptime(data_vendita, "%Y-%m-%d").date()
                query = query.filter(cast(Fattura.data_vendita, Date) == parsed_date)
            except ValueError as e:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        return query.paginate(page=page, per_page=per_page, error_out=False)