import React, { useEffect, useState } from "react";
import axiosInstance from "../services/axiosInstance";

const TradeHistory = () => {
    const [trades, setTrades] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTrades = async () => {
            try {
                const response = await axiosInstance.get("/trades/history", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                });
                setTrades(response.data);
            } catch (err) {
                console.error("Error fetching trades:", err);
                setError("Failed to load trade history.");
            }
        };
        
        fetchTrades();
    }, []);

    return (
        <div className="trade-history">
            <h3>Trade History</h3>
            {error && <p className="text-danger">{error}</p>}
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Trade ID</th>
                        <th>Symbol</th>
                        <th>Type</th>
                        <th>Direction</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {trades.length > 0 ? (
                        trades.map((trade) => (
                            <tr key={trade.id}>
                                <td>{trade.id}</td>
                                <td>{trade.coin_symbol}</td>
                                <td>{trade.trade_type}</td>
                                <td>{trade.direction}</td>
                                <td>{trade.quantity}</td>
                                <td>${trade.price_at_trade.toFixed(2)}</td>
                                <td>{trade.status}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="7" className="text-center">No trade history available.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default TradeHistory;