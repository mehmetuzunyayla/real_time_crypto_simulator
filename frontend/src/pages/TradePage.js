import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";
import PriceChart from "../components/PriceChart";
import TradeForm from "../components/TradeForm";
import TradeHistory from "../components/TradeHistory";

const TradePage = () => {
    const [coins, setCoins] = useState([]);
    const [selectedCoin, setSelectedCoin] = useState(null);
    const [walletBalance, setWalletBalance] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchCoins();
        fetchWalletInfo();
    }, []);

    // Fetch available coins
    const fetchCoins = async () => {
        try {
            const response = await axiosInstance.get("/coins/");
            setCoins(response.data);
            setSelectedCoin(response.data.length > 0 ? response.data[0].symbol : null);
        } catch (error) {
            console.error("Error fetching coins:", error);
            setError("Failed to load coin data.");
        } finally {
            setLoading(false);
        }
    };

    // Fetch user's wallet balance
    const fetchWalletInfo = async () => {
        try {
            const response = await axiosInstance.get("/wallets/", {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            setWalletBalance(response.data.balance);
        } catch (error) {
            console.error("Error fetching wallet balance:", error);
            setError("Failed to load wallet balance.");
        }
    };

    const handleCoinChange = (event) => {
        setSelectedCoin(event.target.value.toLowerCase());
    };

    return (
        <div className="container mt-4">
            <h1 className="text-center">Trade {selectedCoin?.toUpperCase() || "Select a Coin"}</h1>

            {loading ? (
                <p>Loading coins...</p>
            ) : (
            <select onChange={handleCoinChange} value={selectedCoin || ""}>
                {coins.map((coin) => (
                    <option key={coin.symbol} value={coin.symbol}>
                        {coin.symbol.toUpperCase()}
                    </option>
                ))}
            </select>
            )}

            {selectedCoin && <PriceChart selectedCoin={selectedCoin} />}

            {/* Wallet Summary */}
            <div className="wallet-summary mt-4">
                <h3>Wallet Summary</h3>
                <p><strong>Balance:</strong> ${walletBalance.toFixed(2)}</p>
            </div>

            {/* ✅ Use TradeForm Component */}
            <TradeForm selectedCoin={selectedCoin} onTradeSuccess={() => {}} />

            {/* ✅ Use TradeHistory Component */}
            <TradeHistory />
        </div>
    );
};

export default TradePage;
