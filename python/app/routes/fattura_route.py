from flask import Blueprint, request, jsonify
from app.schemas.fattura_schema import fatture_schema, fattura_schema
from app.services.fattura_service import FatturaService
from app.extensions import db
import logging

from app.utils.helpers import get_pagination_params, format_paginated_result

logger = logging.getLogger(__name__)

fatture_bp = Blueprint('fatture_bp', __name__, url_prefix='/fatture')

fattura_service = FatturaService(db)

@fatture_bp.route('/', methods=['GET'])
def get_all_fatture():
    """
    Endpoint to retrieve all invoices.
    """

    logger.info("GET /fatture - Request to retrieve all invoices")

    page, per_page = get_pagination_params()

    fatture = fattura_service.get_all_fatture(page, per_page)
    if not fatture:
        logger.warning("GET /fatture - No invoices found")

        return {"error": "No invoices found"}, 404

    logger.info(f"GET /fatture - Found invoices")

    return jsonify(format_paginated_result(fatture, fatture_schema)), 200


@fatture_bp.route('/<string:id_fattura>', methods=['GET'])
def get_fattura(id_fattura):
    """
    Endpoint to retrieve a specific invoice by ID.
    """

    logger.info(f"GET /fatture/{id_fattura} - Request to retrieve invoice with ID {id_fattura}")

    fattura = fattura_service.get_fattura_by_id(id_fattura)
    if not fattura:
        logger.warning(f"GET /fatture/{id_fattura} - Invoice with ID {id_fattura} not found")

        return {"error": "Invoice not found"}, 404

    logger.info(f"GET /fatture/{id_fattura} - Invoice found: {fattura.id_fattura} dated {fattura.data_vendita}")

    return fattura_schema.dump(fattura), 200


@fatture_bp.route('/', methods=['POST'])
def create_fattura():
    """
    Endpoint to create a new invoice.
    """

    logger.info("POST /fatture - Request to create a new invoice")

    data = request.get_json()

    if not data:
        logger.error("POST /fatture - No input data provided")

        return jsonify({"error": "No input data provided"}), 400

    try:
        fattura = fattura_service.create_fattura(data)

        logger.info(f"POST /fatture - Invoice created")

        return fattura_schema.dump(fattura), 201
    except Exception as e:

        logger.error(f"POST /fatture - Error creating invoice: {str(e)}")

        return jsonify({"error": "Error creating invoice", "details": str(e)}), 500


@fatture_bp.route('/<string:id_fattura>', methods=['PUT'])
def update_fattura(id_fattura):
    """
    Endpoint to update an existing invoice.
    """

    logger.info(f"PUT /fatture/{id_fattura} - Request to update invoice with ID {id_fattura}")

    data = request.get_json()

    if not data:
        logger.error("PUT /fatture - No input data provided")

        return jsonify({"error": "No input data provided"}), 400

    try:
        fattura = fattura_service.update_fattura(id_fattura, data)

        logger.info(f"PUT /fatture/{id_fattura} - Invoice updated with ID {fattura.id_fattura}")

        return fattura_schema.dump(fattura), 200
    except ValueError as e:

        logger.error(f"PUT /fatture/{id_fattura} - Error updating invoice: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"PUT /fatture/{id_fattura} - Error updating invoice: {str(e)}")

        return jsonify({"error": "Error updating invoice", "details": str(e)}), 500


@fatture_bp.route('/<string:id_fattura>', methods=['DELETE'])
def delete_fattura(id_fattura):
    """
    Endpoint to delete an invoice.
    """

    logger.info(f"DELETE /fatture/{id_fattura} - Request to delete invoice with ID {id_fattura}")

    try:
        result = fattura_service.delete_fattura(id_fattura)

        logger.info(f"DELETE /fatture/{id_fattura} - Invoice deleted successfully")

        return jsonify(result), 200
    except ValueError as e:

        logger.error(f"DELETE /fatture/{id_fattura} - Error deleting invoice: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"DELETE /fatture/{id_fattura} - Error deleting invoice: {str(e)}")

        return jsonify({"error": "Error deleting invoice", "details": str(e)}), 500


@fatture_bp.route('/search', methods=['GET'])
def search_fatture():
    """
    Endpoint di ricerca fatture per cliente_id, venditore_id o data_vendita
    Esempio: /fatture/search?cliente_id=1&venditore_id=D1&data_vendita=2024-10-10
    """

    logger.info("GET /fatture/search - Request to search invoices by filters")

    id_cliente = request.args.get('id_cliente')
    id_venditore = request.args.get('id_venditore')
    data_vendita = request.args.get('data_vendita')

    page, per_page = get_pagination_params()

    try:
        risultato = fattura_service.search_fatture(
            id_cliente=id_cliente,
            id_venditore=id_venditore,
            data_vendita=data_vendita,
            page=page,
            per_page=per_page
        )

        if not risultato.items:
            logger.warning("GET /fatture/search - No invoices matched the filters")
            return jsonify({"error": "No invoices matched the filters"}), 404

        logger.info(f"GET /fatture/search - Found  invoices")
        return jsonify(format_paginated_result(risultato, fatture_schema)), 200

    except ValueError as ve:
        logger.error(f"GET /fatture/search - Invalid input: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"GET /fatture/search - Server error: {str(e)}")
        return jsonify({"error": "Error searching invoices", "details": str(e)}), 500
