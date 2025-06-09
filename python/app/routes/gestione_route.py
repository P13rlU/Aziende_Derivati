from flask import Blueprint, request, jsonify
from app.schemas.gestione_schema import gestioni_schema, gestione_schema
from app.services.gestione_service import GestioneService
from app.extensions import db
import logging

from app.utils.helpers import get_pagination_params, format_paginated_result

logger = logging.getLogger(__name__)

gestioni_bp = Blueprint('gestioni_bp', __name__, url_prefix='/gestioni')

gestione_service = GestioneService(db)

@gestioni_bp.route('/', methods=['GET'])
def get_all_gestioni():
    """
    Ottiene tutte le assegnazioni di gestione.
    """

    logger.info("GET /gestioni - Richiesta per ottenere tutte le gestioni")

    page, per_page = get_pagination_params()

    gestioni = gestione_service.get_all_gestioni(page, per_page)
    if not gestioni:
        logger.warning("GET /gestioni - Nessuna gestione trovata")

        return {"error": "Nessuna gestione trovata"}, 404

    logger.info(f"GET /gestioni - Trovate gestioni")

    return jsonify(format_paginated_result(gestioni, gestioni_schema)), 200


@gestioni_bp.route('/<string:id_dipendente>/<string:data_assegnazione>', methods=['GET'])
def get_gestione(id_dipendente, data_assegnazione):
    """
    Ottiene una gestione specifica.
    """

    logger.info(f"GET /gestioni/{id_dipendente}/{data_assegnazione} - Richiesta per ottenere la gestione")

    gestione = gestione_service.get_gestioni_by_id(id_dipendente, data_assegnazione)
    if not gestione:
        logger.warning(f"GET /gestioni/{id_dipendente}/{data_assegnazione} - Gestione non trovata")

        return {"error": "Gestione non trovata"}, 404

    logger.info(f"GET /gestioni/{id_dipendente}/{data_assegnazione} - Gestione trovata")

    return gestione_schema.dump(gestione), 200


@gestioni_bp.route('/', methods=['POST'])
def create_gestione():
    """
    Crea una nuova gestione.
    """

    logger.info("POST /gestioni - Richiesta per creare una nuova gestione")

    data = request.get_json()
    if not data:
        logger.error("POST /gestioni - Nessun dato di input fornito")

        return jsonify({"error": "Dati mancanti"}), 400

    try:
        gestione = gestione_service.create_gestione(data)

        logger.info(
            f"POST /gestioni - Gestione creata con ID {gestione.id_dipendente} e data {gestione.data_assegnazione}")

        return gestione_schema.dump(gestione), 201
    except Exception as e:

        logger.error(f"POST /gestioni - Errore nella creazione della gestione: {str(e)}")

        return jsonify({"error": "Errore nella creazione", "details": str(e)}), 500


@gestioni_bp.route('/<string:id_dipendente>/<string:data_assegnazione>', methods=['PUT'])
def update_gestione(id_dipendente, data_assegnazione):
    """
    Aggiorna una gestione esistente.
    """

    logger.info(f"PUT /gestioni/{id_dipendente}/{data_assegnazione} - Richiesta per aggiornare la gestione")

    data = request.get_json()
    if not data:
        logger.error("PUT /gestioni - Nessun dato di input fornito")

        return jsonify({"error": "Dati mancanti"}), 400

    try:
        gestione = gestione_service.update_gestione(id_dipendente, data_assegnazione, data)

        logger.info(f"PUT /gestioni/{id_dipendente}/{data_assegnazione} - Gestione aggiornata con successo")

        return gestione_schema.dump(gestione), 200
    except ValueError as e:

        logger.error(f"PUT /gestioni/{id_dipendente}/{data_assegnazione} - Errore durante l'aggiornamento: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"PUT /gestioni/{id_dipendente}/{data_assegnazione} - Errore durante l'aggiornamento: {str(e)}")

        return jsonify({"error": "Errore durante aggiornamento", "details": str(e)}), 500


@gestioni_bp.route('/<string:id_dipendente>/<string:data_assegnazione>', methods=['DELETE'])
def delete_gestione(id_dipendente, data_assegnazione):
    """
    Elimina una gestione.
    """

    logger.info(f"DELETE /gestioni/{id_dipendente}/{data_assegnazione} - Richiesta per eliminare la gestione")

    try:
        result = gestione_service.delete_gestione(id_dipendente, data_assegnazione)

        logger.info(f"DELETE /gestioni/{id_dipendente}/{data_assegnazione} - Gestione eliminata con successo")

        return jsonify(result), 200
    except ValueError as e:

        logger.error(f"DELETE /gestioni/{id_dipendente}/{data_assegnazione} - Errore durante l'eliminazione: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"DELETE /gestioni/{id_dipendente}/{data_assegnazione} - Errore durante l'eliminazione: {str(e)}")

        return jsonify({"error": "Errore durante eliminazione", "details": str(e)}), 500
