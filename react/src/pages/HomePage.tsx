import React from 'react';
import Header from '../components/Header';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div>
            <Header title="Ciao, dove vuoi andare?" />
            <button onClick={() => navigate('/dipendente')}>Vai alla pagina Dipendente</button>
            <button onClick={() => navigate('/cliente')}>Vai alla pagina Cliente</button>
        </div>
    );
};

export default HomePage;