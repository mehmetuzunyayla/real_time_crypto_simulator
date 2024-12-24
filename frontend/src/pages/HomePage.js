import React, { useEffect, useState } from 'react';
import axiosInstance from '../services/axiosInstance';

const HomePage = () => {
    const [prices, setPrices] = useState([]);

    useEffect(() => {
        const fetchPrices = async () => {
            try {
                const response = await axiosInstance.get('/coins/prices');
                setPrices(response.data);
            } catch (error) {
                console.error('Error fetching prices:', error);
            }
        };

        fetchPrices();
    }, []);

    return (
        <div>
            <h1>Live Cryptocurrency Prices</h1>
            <ul>
                {Object.keys(prices).map((symbol) => (
                    <li key={symbol}>
                        {symbol}: ${prices[symbol].price.toFixed(2)}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default HomePage;
