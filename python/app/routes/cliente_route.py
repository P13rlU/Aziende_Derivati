# from flasgger import swag_from
from flask import Blueprint, request, jsonify
from app.schemas.cliente_schema import cliente_schema, clienti_schema
from app.services.cliente_service import ClienteService
from app.extensions import db
import logging

from app.utils.helpers import get_pagination_params, format_paginated_result

logger = logging.getLogger(__name__)

clienti_bp = Blueprint('clienti_bp', __name__, url_prefix='/clienti')

cliente_service = ClienteService(db)

@clienti_bp.route('/', methods=['GET'])
# @swag_from('../docs/cliente/get_all.yaml')
def get_all_clienti():
    """
    Endpoint to retrieve all clients.
    """

    logger.info("GET /clienti - Richiesta per ottenere tutti i clienti")

    # Retrieve all clients using the service
    page, per_page = get_pagination_params()

    clienti = cliente_service.get_all_clienti(page, per_page)
    if not clienti:
        logger.warning("GET /clienti - Nessun cliente trovato")

        return {"error": "No clients found"}, 404
    logger.info(f"GET /clienti - Trovati")
    # return clienti_schema.dump(clienti), 200
    return jsonify(format_paginated_result(clienti, clienti_schema)), 200


@clienti_bp.route('/<int:id_cliente>', methods=['GET'])
# @swag_from('../docs/cliente/get_by_id.yaml')
def get_cliente(id_cliente):
    """
    Endpoint to retrieve a specific client by ID.
    """

    logger.info(f"GET /clienti/{id_cliente} - Richiesta per ottenere il cliente con ID {id_cliente}")

    cliente = cliente_service.get_cliente_by_id(id_cliente)
    if not cliente:
        logger.warning(f"GET /clienti/{id_cliente} - Cliente con ID {id_cliente} non trovato")

        return {"error": "Client not found"}, 404

    logger.info(f"GET /clienti/{id_cliente} - Cliente trovato: {cliente.nome} {cliente.cognome}")

    return cliente_schema.dump(cliente), 200


@clienti_bp.route('/', methods=['POST'])
# @swag_from('../docs/cliente/create.yaml')
def create_cliente():
    """
    Endpoint to create a new client.
    """

    logger.info("POST /clienti - Richiesta per creare un nuovo cliente")

    data = request.get_json()

    if not data:
        logger.error("POST /clienti - Nessun dato di input fornito")

        return jsonify({"error": "No input data provided"}), 400

    try:
        cliente = cliente_service.create_cliente(data)

        logger.info(f"POST /clienti - Cliente creato con ID {cliente.id_cliente}")

        return cliente_schema.dump(cliente), 201
    except Exception as e:

        logger.error(f"POST /clienti - Errore durante la creazione del cliente: {str(e)}")

        return jsonify({"error": "Error creating client", "details": str(e)}), 500


@clienti_bp.route('/<int:id_cliente>', methods=['PUT'])
# @swag_from('../docs/cliente/update.yaml')
def update_cliente(id_cliente):
    """
    Endpoint to update an existing client.
    """

    logger.info(f"PUT /clienti/{id_cliente} - Richiesta per aggiornare il cliente con ID {id_cliente}")

    data = request.get_json()

    if not data:
        logger.error(f"PUT /clienti/{id_cliente} - Nessun dato di input fornito per l'aggiornamento")

        return jsonify({"error": "No input data provided"}), 400

    try:
        cliente = cliente_service.update_cliente(id_cliente, data)

        logger.info(f"PUT /clienti/{id_cliente} - Cliente aggiornato con ID {cliente.id_cliente}")

        return cliente_schema.dump(cliente), 200
    except ValueError as e:

        logger.error(f"PUT /clienti/{id_cliente} - Errore durante l'aggiornamento del cliente: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"PUT /clienti/{id_cliente} - Errore durante l'aggiornamento del cliente: {str(e)}")

        return jsonify({"error": "Error updating client", "details": str(e)}), 500


@clienti_bp.route('/<int:id_cliente>', methods=['DELETE'])
# @swag_from('../docs/cliente/delete.yaml')
def delete_cliente(id_cliente):
    """
    Endpoint to delete a client.
    """

    logger.info(f"DELETE /clienti/{id_cliente} - Richiesta per eliminare il cliente con ID {id_cliente}")

    try:
        response = cliente_service.delete_cliente(id_cliente)

        logger.info(f"DELETE /clienti/{id_cliente} - Cliente eliminato con successo")

        return jsonify(response), 200
    except ValueError as e:

        logger.error(f"DELETE /clienti/{id_cliente} - Errore durante l'eliminazione del cliente: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logger.error(f"DELETE /clienti/{id_cliente} - Errore durante l'eliminazione del cliente: {str(e)}")

        return jsonify({"error": "Error deleting client", "details": str(e)}), 500
