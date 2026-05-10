// src/components/Header.tsx
import React from 'react';

const Header: React.FC<{ title: string }> = ({ title }) => {
    return <h1>{title}</h1>;
};

export default Header;