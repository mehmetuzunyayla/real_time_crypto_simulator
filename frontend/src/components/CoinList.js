import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";

const CryptoList = ({ onSelectCoin }) => {
    const [coins, setCoins] = useState([]);
    const [prices, setPrices] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchCoins();
        fetchPrices();
    }, []);

    const fetchCoins = async () => {
        try {
            const response = await axiosInstance.get("/coins/all");
            setCoins(response.data.coins);
        } catch (err) {
            setError("Failed to load cryptocurrency list.");
        }
    };

    const fetchPrices = async () => {
        try {
            const response = await axiosInstance.get("/coins/latest_prices");
            setPrices(response.data);
        } catch (err) {
            setError("Failed to load latest prices.");
        }
    };

    return (
        <div className="crypto-list">
            <h3>Cryptocurrency List</h3>
            {error && <p className="text-danger">{error}</p>}
            <ul>
                {coins.length > 0 ? (
                    coins.map((coin) => (
                        <li key={coin} onClick={() => onSelectCoin(coin)}>
                            {coin.toUpperCase()} - ${prices[coin]?.price?.toFixed(2) || "N/A"}
                        </li>
                    ))
                ) : (
                    <li>No cryptocurrencies available.</li>
                )}
            </ul>
        </div>
    );
};

export default CryptoList;
