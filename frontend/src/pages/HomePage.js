import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";

const HomePage = () => {
    const [prices, setPrices] = useState({});
    const [error, setError] = useState(null);

    // Map of hardcoded coin icons
    const coinIcons = {
        BTCUSDT: "http://127.0.0.1:5000/static/icons/btcusdt.png",
        ETHUSDT: "http://127.0.0.1:5000/static/icons/eth.png",
        BNBUSDT: "http://127.0.0.1:5000/static/icons/bnb.png",
        ADAUSDT: "http://127.0.0.1:5000/static/icons/ada.png",
        DOGEUSDT: "http://127.0.0.1:5000/static/icons/doge.png",
        SOLUSDT: "http://127.0.0.1:5000/static/icons/sol.png",
        DOTUSDT: "http://127.0.0.1:5000/static/icons/dot.png",
        LTCUSDT: "http://127.0.0.1:5000/static/icons/ltc.png",
        LINKUSDT: "http://127.0.0.1:5000/static/icons/link.png",
        UNIUSDT: "http://127.0.0.1:5000/static/icons/uni.png",
        XLMUSDT: "http://127.0.0.1:5000/static/icons/xlm.png",
        VETUSDT: "http://127.0.0.1:5000/static/icons/vet.png",
        TRXUSDT: "http://127.0.0.1:5000/static/icons/trx.png",
        XVGUSDT: "http://127.0.0.1:5000/static/icons/xvg.png",
        XTZUSDT: "http://127.0.0.1:5000/static/icons/xtz.png",
        AAVEUSDT: "http://127.0.0.1:5000/static/icons/aave.png",
        THETAUSDT: "http://127.0.0.1:5000/static/icons/theta.png",
        EOSUSDT: "http://127.0.0.1:5000/static/icons/eos.png",
        ATOMUSDT: "http://127.0.0.1:5000/static/icons/atom.png",
        FILUSDT: "http://127.0.0.1:5000/static/icons/fil.png",
    };

    useEffect(() => {
        // Connect to the WebSocket server
        const socket = io("http://127.0.0.1:5000"); // Adjust based on your Flask server

        // Listen for price updates
        socket.on("price_update", (data) => {
            console.log("Received price update:", data);
            setPrices(data);
        });

        // Handle WebSocket errors
        socket.on("connect_error", (err) => {
            console.error("WebSocket Connection Error:", err);
            setError("Failed to connect to the server.");
        });

        // Cleanup WebSocket connection on component unmount
        return () => socket.disconnect();
    }, []);

    return (
        <div className="container mt-4">
            <h1 className="text-center mb-4">Live Cryptocurrency Prices</h1>
            {error ? (
                <div className="alert alert-danger text-center">{error}</div>
            ) : (
                <div className="table-responsive">
                    <table className="table table-striped table-bordered">
                        <thead className="thead-dark">
                            <tr>
                                <th scope="col">Cryptocurrency</th>
                                <th scope="col">Price (USD)</th>
                                <th scope="col">Daily Change (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.keys(prices).map((coin) => {
                                const { price, daily_change } = prices[coin];
                                const coinKey = coin.toUpperCase(); // Convert to uppercase to match icon map
                                const icon = coinIcons[coinKey] || "/static/icons/default.png"; // Use default icon if missing

                                // Determine the color for daily change
                                const changeColor =
                                    daily_change > 0
                                        ? "text-success" // Green for positive change
                                        : daily_change < 0
                                        ? "text-danger" // Red for negative change
                                        : "text-dark"; // Neutral color

                                return (
                                    <tr key={coin}>
                                        <td>
                                            <img
                                                src={icon}
                                                alt={coinKey}
                                                style={{
                                                    width: "20px",
                                                    marginRight: "10px",
                                                }}
                                            />
                                            {coinKey}
                                        </td>
                                        <td>${price.toLocaleString()}</td>
                                        <td className={changeColor}>
                                            {daily_change > 0 && "+"}
                                            {daily_change}%
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default HomePage;
