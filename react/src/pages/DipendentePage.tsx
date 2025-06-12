import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import DataTable from '../components/DataTable';
import type {Dipendente, Fattura} from '../types';

const DipendentePage: React.FC = () => {
    const [dipendenti, setDipendenti] = useState<Dipendente[]>([]);
    const [fatture, setFatture] = useState<Fattura[]>([]);

    // Recupera tutti i dipendenti
    useEffect(() => {
        fetch('http://localhost:5000/dipendenti')
            .then(res => res.json())
            .then(data => setDipendenti(data.items || []))
            .catch(err => console.error(err));
    }, []);

    // Recupera fatture (esempio)
    useEffect(() => {
        fetch('http://localhost:5000/fatture')
            .then(res => res.json())
            .then(data => setFatture(data.items || []))
            .catch(err => console.error(err));
    }, []);

    const columnsDipendente = [
        { key: 'id_dipendente', label: 'ID' },
        { key: 'nome', label: 'Nome' },
        { key: 'cognome', label: 'Cognome' },
        { key: 'settore', label: 'Settore' }
    ];

    const columnsFatture = [
        { key: 'id_fattura', label: 'ID Fattura' },
        { key: 'data_vendita', label: 'Data Vendita' },
        { key: 'totale', label: 'Totale' }
    ];

    // @ts-ignore
    // @ts-ignore
    return (
        <div>
            <Header title="Sei loggato come dipendente" />

            <h2>Azioni:</h2>
            <ul>
                <li>Ottieni tutte le fatture</li>
                <li>Vedi Tutti I Dipendenti</li>
                <li>Vedi il top venditore</li>
                <li>Emetti una fattura</li>
                <li>Aggiorna una fattura</li>
                <li>Elimina una fattura</li>
            </ul>

            <DataTable data={dipendenti} columns={columnsDipendente} title="Elenco Dipendenti" />
            <DataTable data={fatture} columns={columnsFatture} title="Tutte le Fatture" />
        </div>
    );
};

export default DipendentePage;