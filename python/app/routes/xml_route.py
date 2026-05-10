from flask import Blueprint, Response, request
from app.extensions import db
import logging

from app.services.xml_service import XMLService

logger = logging.getLogger(__name__)

xml_bp = Blueprint('fattura_dettagli', __name__, url_prefix='/xml')

xml_service = XMLService(db)

@xml_bp.route('/cliente', methods=['GET'])
def xml_cliente():
    cf_cliente = request.args.get("cf_cliente")

    logger.info(f"Richiesta XML per cliente con codice fiscale: {cf_cliente}")

    if not cf_cliente:
        logger.error("Codice fiscale non fornito")
        return {"error": "Codice fiscale richiesto"}, 400

    try:
        cliente = xml_service.get_cliente_by_cf(cf_cliente)

        logger.info(f"Cliente trovato: {cliente.nome} {cliente.cognome}")

        fatture = xml_service.get_fatture_by_cliente(cliente.id_cliente)

        logger.info(f"Fatture trovate per il cliente: {len(fatture)}")

        xml_data = xml_service.generate_xml_report_cliente(cliente, fatture)

        logger.info("Report XML generato con successo per il cliente")

        return Response(xml_data, mimetype='text/xml', headers={"Content-disposition": "attachment; filename=report_cliente.xml"})
    except ValueError as ve:

        logger.error(f"Errore nella generazione del report XML: {str(ve)}")

        return {"error": str(ve)}, 404
    except Exception as e:

        logger.error(f"Errore imprevisto nella generazione del report XML: {str(e)}")

        return {"error": "Errore nel generare il report", "details": str(e)}, 500

@xml_bp.route('/prodotto')
def xml_prodotto():
    nome_prodotto = request.args.get("nome")

    logger.info(f"Richiesta XML per prodotto con nome: {nome_prodotto}")

    if not nome_prodotto:

        logger.error("Nome prodotto non fornito")

        return {"error": "Nome prodotto richiesto"}, 400

    try:
        prodotto = xml_service.get_prodotto_by_nome(nome_prodotto)

        logger.info(f"Prodotto trovato: {prodotto.nome}")

        vendite = xml_service.get_vendite_by_prodotto(nome_prodotto)

        logger.info(f"Vendite trovate per il prodotto: {len(vendite)}")

        xml_data = xml_service.generate_xml_report_prodotto(prodotto, vendite)

        logger.info("Report XML generato con successo per il prodotto")

        return Response(xml_data, mimetype='text/xml', headers={"Content-disposition": "attachment; filename=report_prodotto.xml"})
    except ValueError as ve:

        logger.error(f"Errore nella generazione del report XML: {str(ve)}")

        return {"error": str(ve)}, 404
    except Exception as e:

        logger.error(f"Errore imprevisto nella generazione del report XML: {str(e)}")

        return {"error": "Errore nel generare il report", "details": str(e)}, 500
