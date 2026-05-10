from app.models import Dettaglio
from app.schemas.dettaglio_write_schema import dettaglio_write_schema

class DettaglioService:
    def __init__(self, db_session=None):
        self.db = db_session

    
    def get_all_dettagli(self, page=1, per_page=10):
        """Retrieve all detail records."""
        return Dettaglio.query.paginate(page=page, per_page=per_page, error_out=False)

    
    def get_dettaglio_by_id(self, id_fattura, prodotto):
        """Retrieve a detail record by invoice ID and product ID."""
        return self.db.session.get(Dettaglio, (id_fattura, prodotto))

    
    def create_dettaglio(self, data):
        """Create a new detail record."""
        validated_data = dettaglio_write_schema.load(data)
        dettaglio = Dettaglio(**validated_data)
        self.db.session.add(dettaglio)
        self.db.session.commit()
        return dettaglio

    
    def update_dettaglio(self, id_fattura, prodotto, data):
        """Update an existing detail record."""
        dettaglio = self.db.session.get(Dettaglio, (id_fattura, prodotto))
        if not dettaglio:
            raise ValueError("Dettaglio not found")

        validated_data = dettaglio_write_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(dettaglio, key, value)

        self.db.session.commit()
        return dettaglio

    
    def delete_dettaglio(self, id_fattura, prodotto):
        """Delete a detail record."""
        dettaglio = self.db.session.get(Dettaglio, (id_fattura, prodotto))
        if not dettaglio:
            raise ValueError("Dettaglio not found")

        self.db.session.delete(dettaglio)
        self.db.session.commit()