import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";
import { io } from "socket.io-client";

const TradeForm = ({ selectedCoin, onTradeSuccess }) => {
    const [quantity, setQuantity] = useState("");
    const [price, setPrice] = useState(""); // User-input price
    const [livePrice, setLivePrice] = useState(null); // Live market price from WebSocket
    const [tradeType] = useState("SPOT"); // "SPOT" or "FUTURES"
    const [direction] = useState("long"); // 
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState("");

    useEffect(() => {
        if (!selectedCoin) return; // Ensure coin is selected before connecting

        const socket = io("http://127.0.0.1:5000");
        const lowerSymbol = selectedCoin.toLowerCase();

        socket.on("price_update", (data) => {
            if (data[lowerSymbol]) {
                console.log(`[WebSocket] Live price for ${lowerSymbol}:`, data[lowerSymbol].price);
                setLivePrice(data[lowerSymbol].price);
            }
        });

        return () => socket.disconnect();
    }, [selectedCoin]);

    const handleTrade = async (e) => {
        e.preventDefault();
        setError(""); // Reset errors
        setSuccessMessage(""); // Reset success message

        if (!quantity || parseFloat(quantity) <= 0) {
            setError("Invalid quantity. Please enter a positive value.");
            return;
        }

        if (!price || parseFloat(price) <= 0) {
            setError("Price must be a valid number.");
            return;
        }

        if (!livePrice) {
            setError("Live price is not available yet. Please wait.");
            return;
        }

        // Calculate allowed ±2% range
        const minPrice = livePrice * 0.98; // 98% of live price
        const maxPrice = livePrice * 1.02; // 102% of live price
        const enteredPrice = parseFloat(price).toFixed(2); // Ensure decimal format

        if (enteredPrice < minPrice || enteredPrice > maxPrice) {
            setError(`Price must be within ±2% of the current market price ($${livePrice.toFixed(2)}). Allowed range: $${minPrice.toFixed(2)} - $${maxPrice.toFixed(2)}`);
            return;
        }

        try {
            // Create request body
            let requestBody = {
                coin_symbol: selectedCoin.toLowerCase(), // ✅ Ensure lowercase symbol
                trade_type: "SPOT", // ✅ Convert trade type to uppercase
                quantity: parseFloat(quantity),
                price_at_trade: parseFloat(enteredPrice),
                direction: "long",
            };

            // ✅ Include "direction" only for FUTURES trades
            if (tradeType.toUpperCase() === "FUTURES") {
                requestBody.direction = direction;
            }

            console.log("[Trade Request] Sending request:", requestBody);

            const response = await axiosInstance.post("/trades/", requestBody, {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });

            setSuccessMessage("Trade executed successfully!");
            onTradeSuccess(); // Refresh trade history after trade execution
        } catch (err) {
            console.error("[Trade Error]:", err.response ? err.response.data : err.message);
            setError(err.response?.data?.error || "Trade execution failed.");
        }
    };

    return (
        <div className="trade-form card p-3 mt-4">
            <h3 className="text-center">Buy a Coin</h3>
            <form onSubmit={handleTrade}>
                <div className="form-group">
                    <label>Cryptocurrency:</label>
                    <input type="text" value={selectedCoin || ""} readOnly className="form-control" />
                </div>

                <div className="form-group">
                    <label>Quantity:</label>
                    <input
                        type="number"
                        className="form-control"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Price (Allowed range: ±1% of live price):</label>
                    <input
                        type="number"
                        className="form-control"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        required
                    />
                    {livePrice && (
                        <small className="text-white">
                            Live Price: ${livePrice?.toFixed(4)} | Allowed Range: ${(
                                livePrice * 0.99
                            ).toFixed(2)} - ${(livePrice * 1.01).toFixed(4)}
                        </small>

                    )}
                </div>

                {error && <p className="text-danger">{error}</p>}
                {successMessage && <p className="text-success">{successMessage}</p>}

                <button type="submit" className="btn btn-success btn-block mt-3">
                    Buy
                </button>
            </form>
        </div>
    );
};

export default TradeForm;
