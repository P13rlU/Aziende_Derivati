# from flasgger import swag_from
from flask import Blueprint, request, jsonify

from app.schemas.dipendente_schema import dipendente_schema, dipendenti_schema
from app.services.dipendente_service import DipendenteService
from app.extensions import db
import logging

from app.utils.helpers import get_pagination_params, format_paginated_result

logger = logging.getLogger(__name__)

dipendenti_bp = Blueprint('dipendenti_bp', __name__, url_prefix='/dipendenti')

dipendente_service = DipendenteService(db)

@dipendenti_bp.route('/', methods=['GET'])
# @swag_from('../docs/dipendente/get_all.yaml')
def get_all_dipendenti():
    """
    Endpoint to retrieve all dipendenti.
    """

    logger.info("GET /dipendenti - Request to get all dipendenti")

    page, per_page = get_pagination_params()

    dipendenti = dipendente_service.get_all_dipendenti(page, per_page)
    if not dipendenti:
        logger.warning("GET /dipendenti - No dipendenti found")

        return {"error": "No dipendenti found"}, 404

    logger.info(f"GET /dipendenti - Found dipendenti")

    return jsonify(format_paginated_result(dipendenti, dipendenti_schema)), 200


@dipendenti_bp.route('/<string:id_dipendente>', methods=['GET'])
# @swag_from('../docs/dipendente/get_by_id.yaml')
def get_dipendente(id_dipendente):
    """
    Endpoint to retrieve a specific dipendente by ID.
    """

    logger.info(f"GET /dipendenti/{id_dipendente} - Request to get dipendente with ID {id_dipendente}")

    dipendente = dipendente_service.get_dipendente_by_id(id_dipendente)
    if not dipendente:
        logger.warning(f"GET /dipendenti/{id_dipendente} - Dipendente with ID {id_dipendente} not found")

        return {"error": "Dipendente not found"}, 404

    logger.info(f"GET /dipendenti/{id_dipendente} - Dipendente found: {dipendente.nome} {dipendente.cognome}")

    return dipendente_schema.dump(dipendente), 200


@dipendenti_bp.route('/', methods=['POST'])  # create
# @swag_from('../docs/dipendente/create.yaml')
def create_dipendente():
    """
    Endpoint to create a new dipendente.
    """

    logger.info("POST /dipendenti - Request to create a new dipendente")

    data = request.get_json()

    if not data:
        logger.error("POST /dipendenti - No input data provided")

        return jsonify({"error": "No input data provided"}), 400

    try:
        dipendente = dipendente_service.create_dipendente(data)

        logger.info(f"POST /dipendenti - Dipendente created with ID {dipendente.id_dipendente}")

        return dipendente_schema.dump(dipendente), 201
    except Exception as e:

        logger.error(f"POST /dipendenti - Error creating dipendente: {str(e)}")

        return jsonify({"error": "Errore nela creazione del dipendente", "details": str(e)}), 500


@dipendenti_bp.route('/<string:id_dipendente>', methods=['PUT'])  # update
# @swag_from('../docs/dipendente/update.yaml')
def update_dipendente(id_dipendente):
    """
    Endpoint to update an existing dipendente.
    """

    logger.info(f"PUT /dipendenti/{id_dipendente} - Request to update dipendente with ID {id_dipendente}")

    data = request.get_json()

    if not data:
        logger.error("PUT /dipendenti - No input data provided")

        return jsonify({"error": "No input data provided"}), 400

    try:
        dipendente = dipendente_service.update_dipendente(id_dipendente, data)

        logger.info(f"PUT /dipendenti/{id_dipendente} - Dipendente updated with ID {dipendente.id_dipendente}")

        return jsonify(dipendente_schema.dump(dipendente)), 200
    except Exception as e:

        logger.error(f"PUT /dipendenti/{id_dipendente} - Error updating dipendente: {str(e)}")

        return jsonify({"error": "Errore nella modifica del dipendente", "details": str(e)}), 500


@dipendenti_bp.route('/<string:id_dipendente>', methods=['DELETE'])  # delete
# @swag_from('../docs/dipendente/delete.yaml')
def delete_dipendente(id_dipendente):
    """
    Endpoint to delete a dipendente.
    """

    logger.info(f"DELETE /dipendenti/{id_dipendente} - Request to delete dipendente with ID {id_dipendente}")

    try:
        response = dipendente_service.delete_dipendente(id_dipendente)

        logger.info(f"DELETE /dipendenti/{id_dipendente} - Dipendente deleted successfully")

        return jsonify(response), 200
    except Exception as e:

        logger.error(f"DELETE /dipendenti/{id_dipendente} - Error deleting dipendente: {str(e)}")

        return jsonify({"error": "Errore nella cancellazione del dipendente", "details": str(e)}), 500


@dipendenti_bp.route('/top_venditore', methods=['GET'])
def get_top_venditore():
    """
    Endpoint to retrieve the top venditore based on total sales.
    """

    logger.info("GET /dipendenti/top_venditore - Request to get top venditore")

    t_venditore = dipendente_service.top_venditore()
    if not t_venditore:
        logger.warning("GET /dipendenti/top_venditore - No venditore found")

        return jsonify({"message": "Nessun venditore trovato"}), 404

    logger.info("GET /dipendenti/top_venditore - Top venditore found")

    return jsonify(t_venditore), 200
