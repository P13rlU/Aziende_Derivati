import re
from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.cliente import Cliente

class ClienteWriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = False

    @validates("codice_fiscale")
    def validate_codice_fiscale(self, value, **kwargs):
        """
        Valida il formato del codice fiscale italiano.

        Formato: r'^[A-Z0-9]{16}$'
        Esempio: RSSMRA90A01H501Z
        """
        if not value:
            return

        pattern = r'^(?:[A-Z][AEIOUX][AEIOUX]|[B-DF-HJ-NP-TV-Z]{2}[A-Z]){2}(?:[\dLMNP-V]{2}(?:[A-EHLMPR-T](?:[04LQ][1-9MNP-V]|[15MR][\dLMNP-V]|[26NS][0-8LMNP-U])|[DHPS][37PT][0L]|[ACELMRT][37PT][01LM]|[AC-EHLMPR-T][26NS][9V])|(?:[02468LNQSU][048LQU]|[13579MPRTV][26NS])B[26NS][9V])(?:[A-MZ][1-9MNP-V][\dLMNP-V]{2}|[A-M][0L](?:[1-9MNP-V][\dLMNP-V]|[0L][1-9MNP-V]))[A-Z]$'

        if not re.match(pattern, value):
            raise ValidationError(
                "Codice fiscale non valido. Deve seguire il formato italiano (es. RSSMRA90A01H501Z)"
            )

cliente_write_schema = ClienteWriteSchema()