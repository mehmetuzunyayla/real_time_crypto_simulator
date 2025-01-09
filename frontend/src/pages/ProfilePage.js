import React, { useState, useEffect } from "react";
import axiosInstance from "../services/axiosInstance";

const ProfilePage = () => {
    const [user, setUser] = useState(null);
    const [walletBalance, setWalletBalance] = useState(0);
    const [tradeCount, setTradeCount] = useState(0);
    const [editing, setEditing] = useState(false);
    const [newUsername, setNewUsername] = useState("");

    useEffect(() => {
        fetchUserData();
        fetchWalletInfo();
        fetchTradeHistory();
    }, []);

    // Fetch User Data
    const fetchUserData = async () => {
        try {
            const response = await axiosInstance.get("/users/profile", {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            setUser(response.data);
            setNewUsername(response.data.username);
        } catch (error) {
            console.error("Error fetching user data:", error);
        }
    };

    // Fetch Wallet Balance
    const fetchWalletInfo = async () => {
        try {
            const response = await axiosInstance.get("/wallets/", {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            setWalletBalance(response.data.balance);
        } catch (error) {
            console.error("Error fetching wallet balance:", error);
        }
    };

    // Fetch Total Number of Trades
    const fetchTradeHistory = async () => {
        try {
            const response = await axiosInstance.get("/trades/history", {
                headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
            });
            setTradeCount(response.data.length);
        } catch (error) {
            console.error("Error fetching trade history:", error);
        }
    };

    // Handle Username Update
    const handleUpdateUsername = async () => {
        try {
            const response = await axiosInstance.put(
                "/users/update_username", // ✅ Update username API route
                { username: newUsername },
                { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
            );

            setUser((prevUser) => ({ ...prevUser, username: newUsername }));
            setEditing(false);
        } catch (error) {
            console.error("Error updating username:", error);
        }
    };
// Add $1000 to wallet
const handleAddMoney = async () => {
    try {
        const response = await axiosInstance.post(
            "/wallets/update", // ✅ Ensure this matches your API
            { amount: 1000 },  // ✅ Pass the correct request body
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                },
            }
        );

        console.log("Add Money Response:", response.data);

        // ✅ Update wallet balance from API response
        if (response.data.balance !== undefined) {
            setWalletBalance(response.data.balance);
            alert("$1000 added to your wallet!");
        } else {
            alert("Unexpected response format. Check API.");
        }
    } catch (err) {
        console.error("Error adding money:", err);
        alert("Failed to add money. Please try again.");
    }
};
    return (
        <div className="container mt-4">
            <div className="card bg-dark text-white p-4">
                <h2 className="text-center">Profile</h2>
                {user ? (
                    <>
                        <div className="mb-3">
                            <h4>
                                <strong>Username:</strong>{" "}
                                {editing ? (
                                    <input
                                        type="text"
                                        className="form-control d-inline w-50"
                                        value={newUsername}
                                        onChange={(e) => setNewUsername(e.target.value)}
                                    />
                                ) : (
                                    user.username
                                )}
                                {editing ? (
                                    <button className="btn btn-success ms-2" onClick={handleUpdateUsername}>
                                        Save
                                    </button>
                                ) : (
                                    <button className="btn btn-primary ms-2" onClick={() => setEditing(true)}>
                                        Edit
                                    </button>
                                )}
                            </h4>
                        </div>
                        <hr />
                        <div className="mb-3">
                            <h4><strong>Wallet Balance:</strong> ${walletBalance.toFixed(2)}</h4>
                        </div>
                        <div className="mb-3">
                            <h4><strong>Total Trades:</strong> {tradeCount}</h4>
                        </div>
                        <button className="btn btn-success mt-2" onClick={handleAddMoney}>
                            Deposit $1000
                        </button>
                    </>
                ) : (
                    <p>Loading profile...</p>
                )}
            </div>
        </div>
    );
};

export default ProfilePage;
