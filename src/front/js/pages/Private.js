import React, { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Context } from '../store/appContext';
import '../../styles/Private.css';

const Private = () => {
    const { store, actions } = useContext(Context);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem('token');
        
        if (!token) {
            navigate('/login'); 
            return;
        }

        const fetchPrivateData = async () => {
            try {
                const success = await actions.getPrivateData();
                if (!success) {
                    setError("Session expired or unauthorized access.");
                    sessionStorage.removeItem('token'); 
                    navigate('/login'); 
                }
            } catch (err) {
                setError("Error fetching private data.");
            }
        };

        fetchPrivateData();

    }, [navigate]); 

    const handleLogout = () => {
        sessionStorage.removeItem('token'); 
        navigate('/login');
    };

    return (
        <div className="private-container">
            <h2>Private Page</h2>
            {error ? <p className="error-message">{error}</p> : <p>{store.message}</p>}
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Private;
