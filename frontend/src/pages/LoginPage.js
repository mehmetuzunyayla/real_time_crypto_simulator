import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../services/axiosInstance';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axiosInstance.post('/users/login', {
                email,
                password,
            });
            console.log('Login Successful:', response.data);
            // Save the token and username to localStorage
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('username', response.data.username);
            alert('Login Successful!');
            navigate('/'); // Redirect to homepage
        } catch (err) {
            console.error('Login Error:', err.response ? err.response.data : err.message);
            const errorMessage =
                err.response && err.response.data && err.response.data.error
                    ? err.response.data.error
                    : 'An unexpected error occurred. Please try again.';
            setError(errorMessage);
        }
    };
    

    return (
        <div className="container mt-4">
            <h2 className="text-center mb-4">Login</h2>
            <form onSubmit={handleSubmit}>
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
                <button type="submit" className="btn btn-primary btn-block">
                    Login
                </button>
            </form>
        </div>
    );
};

export default LoginPage;
