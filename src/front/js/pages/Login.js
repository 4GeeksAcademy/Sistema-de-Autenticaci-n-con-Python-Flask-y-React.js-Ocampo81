import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom'; 
import { Context } from '../store/appContext';
import '../../styles/Login.css';

const Login = () => {
    const { actions } = useContext(Context);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await actions.login(email, password);
        if (success) {
            setMessage('Login successful! Redirecting...');
            setTimeout(() => {
                window.location.href = '/private'; 
            }, 2000);
        } else {
            setMessage('Failed to login');
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    required
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                <button type="submit">Login</button>
            </form>
            {message && <p>{message}</p>}
            <p>Don't have an account? <Link to="/signup">Sign Up</Link></p> 
        </div>
    );
};

export default Login;
