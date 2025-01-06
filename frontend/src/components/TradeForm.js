import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";

const TradeForm = ({ selectedCoin, onTradeSuccess }) => {
    const [coinSymbol, setCoinSymbol] = useState(selectedCoin || "BTCUSDT");
    const [quantity, setQuantity] = useState("");
    const [price, setPrice] = useState("");
    const [direction, setDirection] = useState("long"); // long or short
    const [tradeType, setTradeType] = useState("spot"); // spot or futures
    const [error, setError] = useState(null);

    useEffect(() => {
        setCoinSymbol(selectedCoin);
    }, [selectedCoin]);

    const handleTrade = async (e) => {
        e.preventDefault();

        if (!quantity || !price || parseFloat(quantity) <= 0 || parseFloat(price) <= 0) {
            setError("Invalid quantity or price.");
            return;
        }

        try {
            const response = await axiosInstance.post(
                "/trades/",
                {
                    coin_symbol: coinSymbol,
                    trade_type: tradeType,
                    quantity: parseFloat(quantity),
                    price_at_trade: parseFloat(price),
                    direction: tradeType === "futures" ? direction : undefined,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                }
            );

            alert("Trade executed successfully!");
            onTradeSuccess(); // Refresh trade history after placing a trade
        } catch (err) {
            console.error("Trade Error:", err);
            setError(err.response?.data?.error || "Trade execution failed.");
        }
    };

    return (
        <div className="trade-form">
            <h3>Execute a Trade</h3>
            <form onSubmit={handleTrade}>
                <div className="form-group">
                    <label>Cryptocurrency:</label>
                    <input type="text" value={coinSymbol} readOnly className="form-control" />
                </div>
                <div className="form-group">
                    <label>Trade Type:</label>
                    <select value={tradeType} onChange={(e) => setTradeType(e.target.value)}>
                        <option value="spot">Spot</option>
                        <option value="futures">Futures</option>
                    </select>
                </div>
                {tradeType === "futures" && (
                    <div className="form-group">
                        <label>Direction:</label>
                        <select value={direction} onChange={(e) => setDirection(e.target.value)}>
                            <option value="long">Long</option>
                            <option value="short">Short</option>
                        </select>
                    </div>
                )}
                <div className="form-group">
                    <label>Quantity:</label>
                    <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Price:</label>
                    <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} required />
                </div>
                {error && <p className="text-danger">{error}</p>}
                <button type="submit" className="btn btn-primary">Execute Trade</button>
            </form>
        </div>
    );
};

export default TradeForm;
