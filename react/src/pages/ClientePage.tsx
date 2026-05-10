import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import DataTable from '../components/DataTable';
import type {Fattura} from '../types';

const ClientePage: React.FC = () => {
    const [fatture, setFatture] = useState<Fattura[]>([]);

    useEffect(() => {
        fetch('http://localhost:5000/fatture/')
            .then(res => res.json())
            .then(data => setFatture(data.items || []))
            .catch(err => console.error(err));
    }, []);

    const columnsFatture = [
        { key: 'id_fattura', label: 'ID Fattura' },
        { key: 'data_vendita', label: 'Data Vendita' },
        { key: 'totale', label: 'Totale' }
    ];

    return (
        <div>
            <Header title="Sei loggato come cliente" />
            <h2>Queste sono le tue fatture:</h2>
            <DataTable data={fatture} columns={columnsFatture} />
        </div>
    );
};

export default ClientePage;