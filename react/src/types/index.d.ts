export type Dipendente = {
    id_dipendente: string;
    nome: string;
    cognome: string;
    stipendio: number | null;
    settore: string;
    categoria: string | null;
};

export type Cliente = {
    id_cliente: number;
    nome: string;
    cognome: string;
    citta: string;
    codice_fiscale: string;
};

export type Fattura = {
    id_fattura: string;
    id_cliente: number;
    id_venditore: string;
    data_vendita: string;
    totale: number;
};