import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../services/axiosInstance';

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("Sending registration data:", { username, email, password });
            const response = await axiosInstance.post('/users/register', {
                username,
                email,
                password,
            });
            console.log('Registration Successful:', response.data);
            // Save the token and username to localStorage
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('username', response.data.username);
            alert('Registration Successful!');
            navigate('/'); // Redirect to homepage
        } catch (err) {
            console.error('Registration Error:', err.response ? err.response.data : err.message);
            const errorMessage =
                err.response && err.response.data && err.response.data.error
                    ? err.response.data.error
                    : 'An unexpected error occurred. Please try again.';
            setError(errorMessage);
        }
    };
    

    return (
        <div className="container mt-4">
            <h2 className="text-center mb-4">Register</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Email</label>
                    <input
                        type="email"
                        className="form-control"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        className="form-control"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p className="text-danger">{error}</p>}
                <button type="submit" className="btn btn-secondary btn-block">
                    Register
                </button>
            </form>
        </div>
    );
};

export default RegisterPage;
