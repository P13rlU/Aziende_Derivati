from app.models import Dipendente
from app.schemas.dipendente_write_schema import dipendente_write_schema


class DipendenteService:

    def __init__(self, db_session=None):
        self.db = db_session

    def get_all_dipendenti(self, page=1, per_page=10):
        return Dipendente.query.paginate(page=page, per_page=per_page, error_out=False)

    def get_dipendente_by_id(self, dipendente_id):
        return Dipendente.query.get(dipendente_id)

    def create_dipendente(self, data):
        try:
            validated_data = dipendente_write_schema.load(data)

            dipendente = Dipendente(**validated_data)

            self.db.session.add(dipendente)
            self.db.session.commit()

            return dipendente
        except Exception as e:
            self.db.session.rollback()
            raise e

    def update_dipendente(self, dipendente_id, data):
        dipendente = Dipendente.query.get(dipendente_id)
        if not dipendente:
            raise ValueError("Dipendente not found")

        validated_data = dipendente_write_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(dipendente, key, value)

        self.db.session.commit()
        return dipendente

    def delete_dipendente(self, dipendente_id):
        dipendente = Dipendente.query.get(dipendente_id)
        if not dipendente:
            raise ValueError("Dipendente not found")

        self.db.session.delete(dipendente)
        self.db.session.commit()
        return {"message": "Dipendente deleted successfully"}

    def top_venditore(self):
        """
        Restituisce il venditore con il totale vendite più alto.
        Return:
            Dict[str, any]: {id_dipendente, nome, cognome, totale_vendite}
            None: se nessun venditore trovato
        """
        query = self.db.text("""
                             WITH TotaleVenditePerVenditore AS
                                      (SELECT d.id_dipendente,
                                              d.nome,
                                              d.cognome,
                                              SUM(f.totale) AS totale_vendite
                                       FROM a_dipendente d
                                                JOIN a_fattura f ON d.id_dipendente = f.ID_VENDITORE
                                       WHERE d.settore = 'vendita'
                                       GROUP BY d.id_dipendente,
                                                d.nome,
                                                d.cognome)
                             SELECT id_dipendente,
                                    nome,
                                    cognome,
                                    totale_vendite
                             FROM TotaleVenditePerVenditore
                             WHERE totale_vendite = (SELECT MAX(totale_vendite)
                                                     FROM TotaleVenditePerVenditore)
                             """)

        result = self.db.session.execute(query).mappings().all()
        return [dict(row) for row in result] if result else None
