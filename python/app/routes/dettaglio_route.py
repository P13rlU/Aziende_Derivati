from flask import Blueprint, request, jsonify
from app.schemas.dettaglio_schema import dettagli_schema, dettaglio_schema
from app.services.dettaglio_service import DettaglioService
from app.extensions import db
import logging

from app.utils.helpers import get_pagination_params, format_paginated_result

logger = logging.getLogger(__name__)

dettagli_bp = Blueprint('dettagli_bp', __name__, url_prefix='/dettagli')

dettaglio_service = DettaglioService(db)

@dettagli_bp.route('/', methods=['GET'])
def get_all_dettagli():
    """
    Ottiene tutti i dettagli delle gestioni.
    """

    logger.info("GET /dettagli - Richiesta per ottenere tutti i dettagli")

    page, per_page = get_pagination_params()

    dettagli = dettaglio_service.get_all_dettagli(page,per_page)
    if not dettagli:
        logger.warning("GET /dettagli - Nessun dettaglio trovato")

        return {"error": "Nessun dettaglio trovato"}, 404

    logger.info(f"GET /dettagli - Trovati dettagli")

    return jsonify(format_paginated_result(dettagli, dettagli_schema)), 200


@dettagli_bp.route('/<string:id_fattura>/<string:prodotto>', methods=['GET'])
def get_dettaglio(id_fattura, prodotto):
    """
    Ottiene un dettaglio specifico.
    """

    logger.info(f"GET /dettagli/{id_fattura}/{prodotto} - Richiesta per ottenere il dettaglio")

    dettaglio = dettaglio_service.get_dettaglio_by_id(id_fattura, prodotto)
    if not dettaglio:
        logger.warning(f"GET /dettagli/{id_fattura}/{prodotto} - Dettaglio non trovato")

        return {"error": "Dettaglio non trovato"}, 404

    logger.info(f"GET /dettagli/{id_fattura}/{prodotto} - Dettaglio trovato")

    return dettaglio_schema.dump(dettaglio), 200


@dettagli_bp.route('/', methods=['POST'])
def create_dettaglio():
    """
    Crea un nuovo dettaglio.
    """

    logger.info("POST /dettagli - Richiesta per creare un nuovo dettaglio")

    data = request.get_json()
    if not data:
        logger.error("POST /dettagli - Dati mancanti nella richiesta")

        return jsonify({"error": "Dati mancanti"}), 400

    try:
        dettaglio = dettaglio_service.create_dettaglio(data)

        logger.info("POST /dettagli - Dettaglio creato con successo")

        return dettaglio_schema.dump(dettaglio), 201
    except Exception as e:

        logger.error(f"POST /dettagli - Errore nella creazione del dettaglio: {str(e)}")

        return jsonify({"error": "Errore nella creazione", "details": str(e)}), 500


@dettagli_bp.route('/<string:id_fattura>/<string:prodotto>', methods=['PUT'])
def update_dettaglio(id_fattura, prodotto):
    """
    Aggiorna un dettaglio esistente.
    """

    logger.info(f"PUT /dettagli/{id_fattura}/{prodotto} - Richiesta per aggiornare il dettaglio")

    data = request.get_json()
    if not data:
        logger.error("PUT /dettagli - Dati mancanti nella richiesta")

        return jsonify({"error": "Dati mancanti"}), 400

    try:
        dettaglio = dettaglio_service.update_dettaglio(id_fattura, prodotto, data)

        logger.info(f"PUT /dettagli/{id_fattura}/{prodotto} - Dettaglio aggiornato con successo")

        return dettaglio_schema.dump(dettaglio), 200
    except ValueError as e:

        logger.error(f"PUT /dettagli/{id_fattura}/{prodotto} - Errore durante l'aggiornamento: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"PUT /dettagli/{id_fattura}/{prodotto} - Errore durante l'aggiornamento: {str(e)}")

        return jsonify({"error": "Errore durante aggiornamento", "details": str(e)}), 500


@dettagli_bp.route('/<string:id_fattura>/<string:prodotto>', methods=['DELETE'])
def delete_dettaglio(id_fattura, prodotto):
    """
    Elimina un dettaglio.
    """

    logger.info(f"DELETE /dettagli/{id_fattura}/{prodotto} - Richiesta per eliminare il dettaglio")

    try:
        dettaglio_service.delete_dettaglio(id_fattura, prodotto)

        logger.info(f"DELETE /dettagli/{id_fattura}/{prodotto} - Dettaglio eliminato con successo")

        return jsonify({"message": "Dettaglio eliminato con successo"}), 204
    except ValueError as e:

        logger.error(f"DELETE /dettagli/{id_fattura}/{prodotto} - Errore durante l'eliminazione: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"DELETE /dettagli/{id_fattura}/{prodotto} - Errore durante l'eliminazione: {str(e)}")

        return jsonify({"error": "Errore durante eliminazione", "details": str(e)}), 500
