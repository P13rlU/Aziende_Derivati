import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import DipendentePage from './pages/DipendentePage'
import ClientePage from './pages/ClientePage'
import './App.css'
import Navigation from "./components/Navigation.tsx";

function App() {
    return (
        <Router>
            <div>
                <Navigation />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/dipendente" element={<DipendentePage />} />
                    <Route path="/cliente" element={<ClientePage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App
