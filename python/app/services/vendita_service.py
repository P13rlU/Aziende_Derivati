class VenditaService:

    def __init__(self, db_session=None):
        self.db = db_session

    def vendite_per_categoria(self):
        """
        Restituisce il totale delle vendite per categoria
        Return:
            Dict[str, any]: {categoria, totale_vendite}
        """
        query = self.db.text("""
                        SELECT p.categoria,
                               SUM(d.quantita * d.costo) AS totale_vendite
                        FROM a_dettaglio d
                                 JOIN a_prodotto p ON d.prodotto = p.nome
                        GROUP BY p.categoria
                        ORDER BY totale_vendite DESC
                        """)
        result = self.db.session.execute(query).mappings().all()
        return [dict(row) for row in result]
