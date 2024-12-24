import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav style={{ padding: '10px', background: '#333', color: '#fff' }}>
            <ul style={{ display: 'flex', listStyle: 'none', gap: '10px' }}>
                <li><Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>Home</Link></li>
                <li><Link to="/wallet" style={{ color: '#fff', textDecoration: 'none' }}>Wallet</Link></li>
                <li><Link to="/trade" style={{ color: '#fff', textDecoration: 'none' }}>Trade</Link></li>
                <li><Link to="/login" style={{ color: '#fff', textDecoration: 'none' }}>Login</Link></li>
                <li><Link to="/register" style={{ color: '#fff', textDecoration: 'none' }}>Register</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
