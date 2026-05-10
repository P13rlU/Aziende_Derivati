from flask import Blueprint, jsonify
from app.services.vendita_service import VenditaService
from app.extensions import db
import logging

logger = logging.getLogger(__name__)

vendite_bp = Blueprint('vendite_bp', __name__, url_prefix='/vendite')

vendita_service = VenditaService(db)

@vendite_bp.route('/categorie', methods=['GET'])
def get_vendite_per_categoria():
    """
    Endpoint to retrieve total sales per category.
    """

    logger.info("GET /vendite/categorie - Request to get total sales per category")

    try:
        vendite = vendita_service.vendite_per_categoria()
        if not vendite:
            logger.warning("GET /vendite/categorie - No sales found")
            return {"error": "No sales found"}, 404

        logger.info(f"GET /vendite/categorie - Found {len(vendite)} categories with sales")
        return jsonify(vendite), 200

    except Exception as e:
        logger.error(f"GET /vendite/categorie - Error: {str(e)}")
        return {"error": "Internal server error"}, 500