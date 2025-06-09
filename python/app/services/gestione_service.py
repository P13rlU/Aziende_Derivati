from app.models import Gestione
from datetime import datetime
from app.schemas.gestione_write_schema import gestione_write_schema

class GestioneService:

    def __init__(self, db_session=None):
        self.db = db_session

    def get_all_gestioni(self, page=1, per_page=10):
        """Retrieve all management records"""
        return Gestione.query.paginate(page=page, per_page=per_page, error_out=False)

    def get_gestioni_by_id(self, id_dipendente, data_assegnazione):
        """Retrieve management records by employee ID and assignment date"""
        try:
            data_obj = datetime.strptime(data_assegnazione, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        return self.db.session.get(Gestione, (id_dipendente, data_obj))

    def create_gestione(self, data):
        """Create a new management record"""
        try:
            validated_data = gestione_write_schema.load(data)
            gestione = Gestione(**validated_data)
            self.db.session.add(gestione)
            self.db.session.commit()
            return gestione
        except Exception as e:
            self.db.session.rollback()
            raise e

    def update_gestione(self, id_dipendente, data_assegnazione, data):
        """Update an existing Gestione record."""
        try:
            data_obj = datetime.strptime(data_assegnazione, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        gestione = self.db.session.get(Gestione, (id_dipendente, data_obj))
        if not gestione:
            raise ValueError("Gestione not found")

        validated_data = gestione_write_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(gestione, key, value)

        self.db.session.commit()
        return gestione

    def delete_gestione(self, id_dipendente, data_assegnazione):
        """Delete a Gestione record."""
        try:
            data_obj = datetime.strptime(data_assegnazione, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        gestione = self.db.session.get(Gestione, (id_dipendente, data_obj))
        if not gestione:
            raise ValueError("Gestione not found")

        self.db.session.delete(gestione)
        self.db.session.commit()
        return {"message": "Gestione deleted successfully"}
