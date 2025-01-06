import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";
import PriceChart from "../components/PriceChart";

const TradePage = () => {
    const [coins, setCoins] = useState([]);
    const [selectedCoin, setSelectedCoin] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCoins = async () => {
            try {
                const response = await axiosInstance.get("/coins/");
                console.log("Coins Fetched:", response.data);
                setCoins(response.data);
                setSelectedCoin(response.data.length > 0 ? response.data[0].symbol : null); // Select first coin
            } catch (error) {
                console.error("Error fetching coins:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchCoins();
    }, []);

    const handleCoinChange = (event) => {
        setSelectedCoin(event.target.value.toLowerCase()); // Ensure lowercase
    };

    return (
        <div className="container mt-4">
            <h1 className="text-center">Trade {selectedCoin?.toUpperCase() || "Select a Coin"}</h1>

            {loading ? (
                <p>Loading coins...</p>
            ) : (
                <select onChange={handleCoinChange} value={selectedCoin}>
                    {coins.map((coin) => (
                        <option key={coin.symbol} value={coin.symbol}>
                            {coin.symbol.toUpperCase()}
                        </option>
                    ))}
                </select>
            )}

            {selectedCoin && <PriceChart selectedCoin={selectedCoin} />}

            <div className="wallet-summary mt-4">
                <h3>Wallet Summary</h3>
                <p>Balance: $0.00</p>
                <h4>Recent Transactions</h4>
                <ul>
                    <li>No recent transactions.</li>
                </ul>
            </div>

            <div className="trade-form mt-4">
                <h3>Execute a Trade</h3>
                <label>Cryptocurrency:</label>
                <input type="text" value={selectedCoin || ""} readOnly />

                <label>Trade Type:</label>
                <select>
                    <option value="spot">Spot</option>
                    <option value="futures">Futures</option>
                </select>

                <label>Quantity:</label>
                <input type="number" placeholder="Enter quantity" />

                <label>Price:</label>
                <input type="number" placeholder="Enter price" />

                <button className="btn btn-primary mt-3">Execute Trade</button>
            </div>

            <div className="trade-history mt-4">
                <h3>Trade History</h3>
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
                        <tr>
                            <td colSpan="7" className="text-center">No trade history available.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TradePage;
