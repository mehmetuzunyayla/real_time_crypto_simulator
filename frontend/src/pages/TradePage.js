import React, { useEffect, useState } from "react";
import ApexCharts from "react-apexcharts";
import axiosInstance from "../services/axiosInstance";

const TradePage = () => {
    const [ohlcData, setOhlcData] = useState([]);
    const [error, setError] = useState(null);
    const [interval, setInterval] = useState("1m");

    useEffect(() => {
        const fetchOhlcData = async () => {
            try {
                const response = await axiosInstance.get(`/coins/history/btcusdt?interval=${interval}`);
                const formattedData = response.data.map((item) => ({
                    x: new Date(item.time).getTime(), // Timestamp
                    y: [item.open, item.high, item.low, item.close], // OHLC values
                }));
                setOhlcData(formattedData);
            } catch (err) {
                console.error("Error fetching OHLC data:", err);
                setError("Failed to fetch candlestick data.");
            }
        };

        fetchOhlcData();
    }, [interval]); // Fetch data when the interval changes

    const options = {
        chart: {
            type: "candlestick",
            height: 350,
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            tooltip: {
                enabled: true,
            },
        },
    };

    const series = [
        {
            data: ohlcData,
        },
    ];

    return (
        <div className="container mt-4">
            <h2 className="text-center">Trade Page</h2>
            <div className="mb-3">
                <label htmlFor="interval" className="form-label">
                    Interval:
                </label>
                <select
                    id="interval"
                    className="form-select"
                    value={interval}
                    onChange={(e) => setInterval(e.target.value)}
                >
                    <option value="1m">1 Minute</option>
                    <option value="15m">15 Minutes</option>
                    <option value="1h">1 Hour</option>
                    <option value="4h">4 Hours</option>
                    <option value="1d">1 Day</option>
                    <option value="1w">1 Week</option>
                </select>
            </div>
            {error ? (
                <div className="alert alert-danger">{error}</div>
            ) : (
                <ApexCharts options={options} series={series} type="candlestick" height={350} />
            )}
        </div>
    );
};

export default TradePage;
