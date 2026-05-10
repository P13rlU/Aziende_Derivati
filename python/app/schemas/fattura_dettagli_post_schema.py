from marshmallow import Schema, fields, validates, ValidationError

class DettaglioProdottoSchema(Schema):
    prodotto = fields.String(required=True)
    quantita = fields.Integer(required=True, validate=lambda x: x > 0)
    costo = fields.Decimal(required=True, as_string=True, validate=lambda x: x > 0)


class FatturaPostSchema(Schema):
    cf_cliente = fields.String(required=True)
    data_vendita = fields.Date(format='%Y-%m-%d', required=True)
    id_fattura = fields.String(required=True)
    venditore = fields.String(required=True)
    dettagli = fields.Nested(DettaglioProdottoSchema, many=True, required=True)

    @validates('cf_cliente')
    def validate_cf(self, value, **kwargs):
        if not value:
            raise ValidationError("Codice fiscale richiesto")

    @validates('dettagli')
    def validate_dettagli(self, value, **kwargs):
        if not value or len(value) == 0:
            raise ValidationError("Devi inserire almeno un prodotto nei dettagli")


fattura_post_schema = FatturaPostSchema()