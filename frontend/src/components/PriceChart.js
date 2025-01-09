import React, { useState, useEffect, useRef } from "react";
import ApexCharts from "react-apexcharts";
import { io } from "socket.io-client";
import axiosInstance from "../services/axiosInstance";

const MAX_CANDLES = 50; // Keep chart efficient

const PriceChart = ({ selectedCoin }) => {
    const [ohlcData, setOhlcData] = useState([]);
    const [interval, setInterval] = useState("1m");
    const [latestPrice, setLatestPrice] = useState(null);
    const [priceChangeColor, setPriceChangeColor] = useState("green");
    const lastUpdatedTimeRef = useRef(null);

    // Fetch historical data once
    useEffect(() => {
        const fetchChartData = async () => {
            try {
                const response = await axiosInstance.get(`/coins/${selectedCoin.toLowerCase()}/ohlc/${interval}`);
                const formattedData = response.data.map((entry) => ({
                    x: new Date(entry.time).getTime(),
                    y: [entry.open, entry.high, entry.low, entry.close]
                }));

                setOhlcData(formattedData.slice(-MAX_CANDLES));
                setLatestPrice(formattedData[formattedData.length - 1].y[3]);
                lastUpdatedTimeRef.current = formattedData[formattedData.length - 1].x;
            } catch (err) {
                console.error("Failed to fetch OHLC data:", err);
            }
        };

        fetchChartData();
    }, [selectedCoin, interval]);

    // WebSocket price updates
    useEffect(() => {
        const socket = io("http://127.0.0.1:5000");

        socket.on("price_update", (data) => {
            if (data[selectedCoin]) {
                updateLatestCandlestick(data[selectedCoin].price);
            }
        });

        return () => socket.disconnect();
    }, [selectedCoin]);

    // Update last candlestick or add new one if new minute starts
    const updateLatestCandlestick = (newPrice) => {
        setOhlcData((prevData) => {
            if (!prevData.length) return prevData;

            const now = new Date();
            const lastCandleTime = new Date(lastUpdatedTimeRef.current);
            const isSameCandle = now.getMinutes() === lastCandleTime.getMinutes();

            let updatedData = [...prevData];

            if (isSameCandle) {
                let lastCandle = { ...updatedData[updatedData.length - 1] };
                lastCandle.y[3] = newPrice; // Update close price
                lastCandle.y[1] = Math.max(lastCandle.y[1], newPrice); // Update high if needed
                lastCandle.y[2] = Math.min(lastCandle.y[2], newPrice); // Update low if needed
                updatedData[updatedData.length - 1] = lastCandle;
            } else {
                const newCandle = {
                    x: now.getTime(),
                    y: [newPrice, newPrice, newPrice, newPrice]
                };
                updatedData = [...updatedData.slice(-MAX_CANDLES + 1), newCandle];
                lastUpdatedTimeRef.current = now.getTime();
            }

            return updatedData;
        });

        setPriceChangeColor(newPrice > latestPrice ? "green" : "red");
        setLatestPrice(newPrice);
    };

    // Determine Y-axis min/max dynamically
    const minPrice = Math.min(...ohlcData.map(candle => candle.y[2])) || 0;
    const maxPrice = Math.max(...ohlcData.map(candle => candle.y[1])) || 1;
    const priceBuffer = (maxPrice - minPrice) * 0.05; // 5% padding

    const options = {
        chart: { type: "candlestick", height: 400 },
        xaxis: {
            type: "datetime",
            labels: {
                formatter: function (val) {
                    let date = new Date(val);
                    date.setHours(date.getHours() + 3); // ✅ Convert UTC to UTC+3
                    
                    return date.toLocaleString("en-GB", {
                        hour: "2-digit",
                        minute: "2-digit",
                        day: "2-digit",
                        month: "short"
                    }).replace(",", ""); // ✅ Format as "00.00 09 Jan"
                }
            }
        },
        yaxis: {
            opposite: true, // Moves Y-axis to the right
            min: minPrice - priceBuffer,
            max: maxPrice + priceBuffer,
            labels: {
                formatter: (value) => `$${value.toFixed(2)}` // Format prices
            }
        },
        annotations: {
            yaxis: [
                {
                    y: latestPrice,
                    borderColor: priceChangeColor,
                    label: {
                        text: `$${latestPrice}`,
                        position: "right", // Align with Y-axis
                        offsetX: 45, // Shift label inside chart
                        style: { color: "#fff", background: priceChangeColor, fontSize: "11px" }
                    }
                }
            ]
        }
    };
    
    

    return (
        <div>
            <h3>{selectedCoin.toUpperCase()} Price Chart</h3>
            <select value={interval} onChange={(e) => setInterval(e.target.value)}>
                <option value="1m">1 Minute</option>
                <option value="1h">1 Hour</option>
                <option value="1d">1 Day</option>
            </select>
            {ohlcData.length ? (
                <ApexCharts options={options} series={[{ data: ohlcData }]} type="candlestick" height={400} />
            ) : (
                <p>Loading chart...</p>
            )}
        </div>
    );
};

export default PriceChart;
