// src/components/Navigation.tsx
import React from 'react';
import { Link } from 'react-router-dom';

const Navigation: React.FC = () => {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/dipendente">Dipendente</Link></li>
                <li><Link to="/cliente">Cliente</Link></li>
            </ul>
        </nav>
    );
};

export default Navigation;