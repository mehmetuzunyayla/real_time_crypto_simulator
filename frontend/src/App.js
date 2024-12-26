import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { io } from 'socket.io-client';
import Navbar from './components/Navbar'; // Import Navbar
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TradePage from './pages/TradePage';
import WalletPage from './pages/WalletPage';
import ProfilePage from './pages/ProfilePage';

const App = () => {
    const [prices, setPrices] = useState({});
    const [previousPrices, setPreviousPrices] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        const socket = io('http://127.0.0.1:5000'); // Connect to Flask WebSocket server

        // Listen for price updates
        socket.on('price_update', (data) => {
            setPreviousPrices(prices); // Save current prices as previous
            setPrices(data); // Update prices dynamically
        });

        // Handle connection errors
        socket.on('connect_error', (err) => {
            console.error('WebSocket Connection Error:', err);
            setError('Failed to connect to the server.');
        });

        // Cleanup the socket connection on component unmount
        return () => socket.disconnect();
    }, [prices]);

    return (
        <Router>
            <Navbar />
            <div className="container mt-4">
                <Routes>
                    <Route
                        path="/"
                        element={<HomePage prices={prices} previousPrices={previousPrices} error={error} />}
                    />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/trade" element={<TradePage />} />
                    <Route path="/wallet" element={<WalletPage />} />
                    <Route path="/profile" element={<ProfilePage />} />

                </Routes>
            </div>
        </Router>
    );
};

export default App;
