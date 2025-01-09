import React, { useEffect, useState } from "react";
import axiosInstance from "../services/axiosInstance";
import { io } from "socket.io-client";

const TradeHistory = () => {
    const [trades, setTrades] = useState([]);
    const [error, setError] = useState(null);
    const [livePrices, setLivePrices] = useState({}); // ✅ Store live market prices

    // ✅ Fetch trade history from backend
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

    useEffect(() => {
        fetchTrades(); // ✅ Initial fetch

        // ✅ WebSocket: Listen for price updates
        const socket = io("http://127.0.0.1:5000");
        socket.on("price_update", (data) => {
            setLivePrices(data); // ✅ Store live prices
        });

        socket.on("trade_update", () => {
            console.log("[WebSocket] Trade update received, refreshing history...");
            fetchTrades(); // ✅ Refresh trade history
        });

        return () => socket.disconnect(); // ✅ Cleanup WebSocket on unmount
    }, []);

    // ✅ Function to close a trade
    const handleCloseTrade = async (tradeId) => {
        try {
            await axiosInstance.post(`/trades/${tradeId}/close`, {}, {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            console.log(`Trade ${tradeId} closed successfully.`);
            fetchTrades(); // ✅ Refresh trade history after closing
        } catch (err) {
            console.error(`Error closing trade ${tradeId}:`, err);
            alert("Failed to close trade.");
        }
    };

    const calculatePnL = (trade, livePrices) => {
        // ✅ Use `close_pnl` for closed trades
        if (trade.status === "closed" && trade.close_pnl !== null) {
            return trade.close_pnl.toFixed(2);
        }
    
        // ✅ Use live price for open trades
        const livePrice = livePrices[trade.coin_symbol]?.price;
        if (!livePrice || !trade.price_at_trade || !trade.quantity) {
            return "Waiting..."; // ✅ Prevent crashes if values are missing
        }
    
        return ((livePrice - trade.price_at_trade) * trade.quantity).toFixed(2);
    };
    
    return (
        <div className="trade-history">
            <h3>Trade History</h3>
            {error && <p className="text-danger">{error}</p>}
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Trade ID</th>
                        <th>Symbol</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>PnL</th> {/* ✅ Shows real-time PnL for open trades */}
                        <th>Status</th>
                        <th>Action</th> {/* ✅ "Close" button column */}
                    </tr>
                </thead>
                <tbody>
                    {trades.length > 0 ? (
                        [...trades].reverse().map((trade) => (
                            <tr key={trade.id}>
                                <td>{trade.id}</td>
                                <td>{trade.coin_symbol}</td>
                                <td>{trade.quantity}</td>
                                <td>${trade.price_at_trade.toFixed(2)}</td>
                                <td 
                                    className={calculatePnL(trade, livePrices) >= 0 ? "text-success" : "text-danger"}
                                >
                                    ${calculatePnL(trade, livePrices)}
                                </td>
                                <td>{trade.status}</td>
                                <td>
                                    {trade.status === "open" && (
                                        <button
                                            className="btn btn-danger btn-sm"
                                            onClick={() => handleCloseTrade(trade.id)}
                                        >
                                            Close
                                        </button>
                                    )}
                                </td> {/* ✅ Close Button for Open Trades */}
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
