import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";

const WalletSummary = () => {
    const [balance, setBalance] = useState(0);
    const [transactions, setTransactions] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchWalletData();
    }, []);

    const fetchWalletData = async () => {
        try {
            const response = await axiosInstance.get("/wallets/", {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            setBalance(response.data.balance);
        } catch (err) {
            setError("Failed to load wallet balance.");
        }

        try {
            const response = await axiosInstance.get("/trade/history", {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            setTransactions(response.data);
        } catch (err) {
            setError("Failed to load transaction history.");
        }
    };

    return (
        <div className="wallet-summary">
            <h3>Wallet Summary</h3>
            {error && <p className="text-danger">{error}</p>}
            <p><strong>Balance:</strong> ${balance.toFixed(2)}</p>
            <h4>Recent Transactions</h4>
            <ul>
                {transactions.length > 0 ? (
                    transactions.slice(0, 5).map((tx) => (
                        <li key={tx.id}>
                            {tx.type.toUpperCase()} {tx.amount} USDT ({tx.status})
                        </li>
                    ))
                ) : (
                    <li>No recent transactions.</li>
                )}
            </ul>
        </div>
    );
};

export default WalletSummary;
