from app.models import Fattura, Cliente, Dettaglio, Prodotto
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from sqlalchemy.orm import joinedload

class XMLService:
    def __init__(self, db_session):
        self.db = db_session

    def get_cliente_by_cf(self, codice_fiscale):
        cliente = Cliente.query.filter(Cliente.codice_fiscale == codice_fiscale).first()
        if not cliente:
            raise ValueError("Cliente non trovato")
        return cliente

    def get_fatture_by_cliente(self, id_cliente):
        return Fattura.query.filter(Fattura.id_cliente == id_cliente).all()

    def get_prodotto_by_nome(self, nome):
        prodotto = Prodotto.query.filter(Prodotto.nome == nome).first()
        if not prodotto:
            raise ValueError("Prodotto non trovato")
        return prodotto

    def get_vendite_by_prodotto(self, nome_prodotto):
        return (
            Dettaglio.query
            .filter(Dettaglio.prodotto == nome_prodotto)
            .join(Dettaglio.fattura)
            .options(joinedload(Dettaglio.fattura))
            .all()
        )

    def generate_xml_report_cliente(self, cliente, fatture):
        root = Element("report")
        cliente_node = SubElement(root, "cliente")
        cliente_node.text = f"{cliente.nome} {cliente.cognome}"

        ordini_node = SubElement(root, "ordini")

        for fattura in fatture:
            ordine = SubElement(ordini_node, "ordine")
            ordine.set("data", str(fattura.data_vendita))
            ordine.set("id_fattura", fattura.id_fattura)

            dettagli = fattura.dettagli
            for d in dettagli:
                prod_node = SubElement(ordine, "prodotto")
                prod_node.set("nome", d.prodotto)
                prod_node.set("quantita", str(d.quantita))
                prod_node.set("costo", str(d.costo))
                prod_node.set("totale", str(d.quantita * d.costo))

        return self._pretty_xml(root)

    def generate_xml_report_prodotto(self, prodotto, vendite):
        root = Element("report")
        prod_node = SubElement(root, "prodotto")
        prod_node.text = prodotto.nome

        vendite_node = SubElement(root, "vendite")

        for dettaglio in vendite:
            ordine = SubElement(vendite_node, "ordine")
            ordine.set("data", str(dettaglio.fattura.data_vendita))
            ordine.set("cliente", f"{dettaglio.fattura.cliente.nome} {dettaglio.fattura.cliente.cognome}")

            qta = SubElement(ordine, "quantita")
            qta.text = str(dettaglio.quantita)

            tot = SubElement(ordine, "totale")
            tot.text = str(dettaglio.quantita * dettaglio.costo)

        return self._pretty_xml(root)

    def _pretty_xml(self, element):
        rough_string = tostring(element, encoding='utf-8', method='xml')
        parsed = minidom.parseString(rough_string)
        return parsed.toprettyxml(indent="  ")