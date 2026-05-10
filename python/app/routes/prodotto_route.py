from flask import Blueprint, request, jsonify
from app.schemas.prodotto_schema import prodotti_schema, prodotto_schema
from app.services.prodotto_service import ProdottoService
from app.extensions import db
import logging

from app.utils.helpers import get_pagination_params, format_paginated_result

prodotti_bp = Blueprint('prodotti_bp', __name__, url_prefix='/prodotti')

prodotti_service = ProdottoService(db)

@prodotti_bp.route('/', methods=['GET'])
def get_all_prodotti():
    """
    Endpoint to retrieve all products.
    """

    logging.info("GET /prodotti - Request to get all products")

    page, per_page = get_pagination_params()

    prodotti = prodotti_service.get_all_prodotti(page, per_page)
    if not prodotti:
        logging.warning("GET /prodotti - No products found")

        return {"error": "No products found"}, 404

    logging.info(f"GET /prodotti - Found products")

    return jsonify(format_paginated_result(prodotti, prodotti_schema)), 200


@prodotti_bp.route('/<string:nome>', methods=['GET'])
def get_prodotto(nome):
    """
    Endpoint to retrieve a specific product by ID.
    """

    logging.info(f"GET /prodotti/{nome} - Request to get product with ID {nome}")

    prodotto = prodotti_service.get_prodotto_by_id(nome)
    if not prodotto:
        logging.warning(f"GET /prodotti/{nome} - Product with ID {nome} not found")

        return {"error": "Product not found"}, 404

    logging.info(f"GET /prodotti/{nome} - Product found: {prodotto.nome}")

    return prodotto_schema.dump(prodotto), 200


@prodotti_bp.route('/', methods=['POST'])
def create_prodotto():
    """
    Endpoint to create a new product.
    """

    logging.info("POST /prodotti - Request to create a new product")

    data = request.get_json()

    if not data:
        logging.error("POST /prodotti - No input data provided")

        return jsonify({"error": "No input data provided"}), 400

    try:
        prodotto = prodotti_service.create_prodotto(data)

        logging.info(f"POST /prodotti - Product created with ID {prodotto.nome}")

        return prodotto_schema.dump(prodotto), 201
    except Exception as e:

        logging.error(f"POST /prodotti - Error creating product: {str(e)}")

        return jsonify({"error": "Error creating product", "details": str(e)}), 500


@prodotti_bp.route('/<string:nome>', methods=['PUT'])
def update_prodotto(nome):
    """
    Endpoint to update an existing product.
    """

    logging.info(f"PUT /prodotti/{nome} - Request to update product with ID {nome}")

    data = request.get_json()

    if not data:
        logging.error("PUT /prodotti - No input data provided")

        return jsonify({"error": "No input data provided"}), 400

    try:
        prodotto = prodotti_service.update_prodotto(nome, data)

        logging.info(f"PUT /prodotti/{nome} - Product updated with ID {prodotto.nome}")

        return prodotto_schema.dump(prodotto), 200
    except ValueError as e:

        logging.warning(f"PUT /prodotti/{nome} - Product with ID {nome} not found: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logging.error(f"PUT /prodotti/{nome} - Error updating product: {str(e)}")

        return jsonify({"error": "Error updating product", "details": str(e)}), 500


@prodotti_bp.route('/<string:nome>', methods=['DELETE'])
def delete_prodotto(nome):
    """
    Endpoint to delete a product.
    """

    logging.info(f"DELETE /prodotti/{nome} - Request to delete product with ID {nome}")

    try:
        response = prodotti_service.delete_prodotto(nome)

        logging.info(f"DELETE /prodotti/{nome} - Product deleted successfully")

        return jsonify(response), 200
    except ValueError as e:

        logging.warning(f"DELETE /prodotti/{nome} - Product with ID {nome} not found: {str(e)}")

        return jsonify({"error": str(e)}), 404
    except Exception as e:

        logging.error(f"DELETE /prodotti/{nome} - Error deleting product: {str(e)}")

        return jsonify({"error": "Error deleting product", "details": str(e)}), 500
