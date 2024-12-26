import React, { useEffect, useState } from "react";
import axiosInstance from "../services/axiosInstance";

const ProfilePage = () => {
    const [profile, setProfile] = useState({});
    const [username, setUsername] = useState("");
    const [walletBalance, setWalletBalance] = useState(0);
    const [error, setError] = useState(null);

    // Fetch profile details
    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await axiosInstance.get("/users/profile", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                });
                setProfile(response.data);
                setUsername(response.data.username);
                setWalletBalance(response.data.wallet_balance);
            } catch (err) {
                console.error("Error fetching profile:", err);
                setError("Failed to fetch profile details.");
            }
        };

        fetchProfile();
    }, []);

    // Update username
    const handleUpdateUsername = async () => {
        try {
            await axiosInstance.put(
                "/users/update_username",
                { username },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                }
            );
            alert("Username updated successfully!");
        } catch (err) {
            console.error("Error updating username:", err);
            alert("Failed to update username.");
        }
    };

    // Add money to wallet
    const handleAddMoney = async () => {
        try {
            const response = await axiosInstance.post(
                "/wallets/update",
                { amount: 1000 }, // Pass amount in the body
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
                    },
                }
            );
            console.log("Add Money Response:", response.data);

            // Update wallet balance in state
            setWalletBalance(response.data.balance);
            alert("$1000 added to your wallet!");
        } catch (err) {
            console.error("Error adding money:", err);
            alert("Failed to add money.");
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="text-center mb-4">Profile</h2>
            {error ? (
                <p className="text-danger">{error}</p>
            ) : (
                <div>
                    <div className="form-group">
                        <label>Email:</label>
                        <p>{profile.email}</p>
                    </div>
                    <div className="form-group">
                        <label>Username:</label>
                        <input
                            type="text"
                            className="form-control"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <button
                            className="btn btn-primary mt-2"
                            onClick={handleUpdateUsername}
                        >
                            Update Username
                        </button>
                    </div>
                    <div className="form-group">
                        <label>Wallet Balance:</label>
                        <p>${walletBalance.toLocaleString()}</p>
                        <button
                            className="btn btn-success"
                            onClick={handleAddMoney}
                        >
                            Add $1000
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ProfilePage;
