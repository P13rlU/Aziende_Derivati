from app.models import Prodotto
from app.schemas.prodotto_write_schema import prodotto_write_schema

class ProdottoService:
    
    def __init__(self, db_session=None):
        self.db = db_session
    
    
    def get_all_prodotti(self, page=1, per_page=10):
        """Retrieve all products."""
        return Prodotto.query.paginate(page=page, per_page=per_page, error_out=False)

    
    def get_prodotto_by_id(self, prodotto_nome):
        """Retrieve a product by its ID."""
        return Prodotto.query.get(prodotto_nome)

    
    def create_prodotto(self, data):
        """Create a new product."""
        try:
            validated_data = prodotto_write_schema.load(data)

            prodotto = Prodotto(**validated_data)

            self.db.session.add(prodotto)
            self.db.session.commit()

            return prodotto
        except Exception as e:
            self.db.session.rollback()
            raise e

    
    def update_prodotto(self, prodotto_nome, data):
        """Update an existing product."""
        prodotto = Prodotto.query.get(prodotto_nome)
        if not prodotto:
            raise ValueError("Product not found")

        validated_data = prodotto_write_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(prodotto, key, value)

        self.db.session.commit()
        return prodotto

    
    def delete_prodotto(self, prodotto_nome):
        """Delete a product."""
        prodotto = Prodotto.query.get(prodotto_nome)
        if not prodotto:
            raise ValueError("Product not found")

        self.db.session.delete(prodotto)
        self.db.session.commit()
        return {"message": "Product deleted successfully"}