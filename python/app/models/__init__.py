from .prodotto import Prodotto
from .cliente import Cliente
from .dipendente import Dipendente
from .fattura import Fattura
from .dettaglio import Dettaglio
from .gestione import Gestione


def import_all_models():
    """
    Import all models to ensure they are registered with SQLAlchemy.
    This function is called in the app's context to ensure models are loaded.
    """
    pass
