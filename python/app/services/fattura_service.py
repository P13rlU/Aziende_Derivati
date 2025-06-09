from sqlalchemy import cast, Date

from app.models import Fattura, Prodotto, Dettaglio
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

    def fatture_per_dettaglio_categoria(self):
        """
        Restituisce il totale delle fatture per categoria.
        Return:
            Dict[str, any]: {categoria, totale_fatture}
        """
        query = self.db.text("""
                             WITH CategorieFattura AS
                                      (SELECT f.id_fattura,
                                              COUNT(DISTINCT p.categoria) AS numero_categorie
                                       FROM a_fattura f
                                                JOIN a_dettaglio d ON f.id_fattura = d.id_fattura
                                                JOIN a_prodotto p ON d.prodotto = p.nome
                                       GROUP BY f.id_fattura)
                             SELECT f.id_fattura,
                                    f.data_vendita,
                                    f.totale,
                                    c.numero_categorie
                             FROM a_fattura f
                                      JOIN CategorieFattura c ON f.id_fattura = c.id_fattura
                             WHERE c.numero_categorie > 1
                             ORDER BY c.numero_categorie DESC
                             """)
        result = self.db.session.execute(query).mappings().all()
        return [dict(row) for row in result]

    def categorie_fatture(self):
        """
        Retrieve all product categories with invoice counts.

        Returns:
            List[Dict]: List of categories with count of invoices
        """
        result = (self.db.session.query(
            Prodotto.categoria,
            self.db.func.count(self.db.distinct(Fattura.id_fattura)).label('count'))
                  .join(Dettaglio, Dettaglio.prodotto == Prodotto.nome)
                  .join(Fattura, Fattura.id_fattura == Dettaglio.id_fattura)
                  .group_by(Prodotto.categoria)
                  .all())

        return [{"categoria": row[0], "count": row[1]} for row in result]

    def fatture_by_categoria(self, categoria, page=1, per_page=10):
        """
        Retrieve invoices by product category.

        Args:
            categoria (str): Product category to filter by
            page (int): Page number
            per_page (int): Items per page

        Returns:
            Pagination: Paginated result of invoices
        """
        return (Fattura.query
                .join(Dettaglio, Fattura.id_fattura == Dettaglio.id_fattura)
                .join(Prodotto, Dettaglio.prodotto == Prodotto.nome)
                .filter(Prodotto.categoria == categoria)
                .paginate(page=page, per_page=per_page, error_out=False))