/**
 * ZKAS Frontend - Zero-Knowledge Authentication System
 * React application for authentication using Zero-Knowledge Proofs
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';
const CRYPTO_API_URL = process.env.REACT_APP_CRYPTO_URL || 'http://localhost:5000';

export default function App() {
  const [currentPage, setCurrentPage] = useState('login');
  const [authToken, setAuthToken] = useState(localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if user is already authenticated
    if (authToken) {
      verifyToken();
    }
  }, [authToken]);

  const verifyToken = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/verify`, {
        token: authToken
      });
      
      if (response.data.valid) {
        setUser(response.data.user);
        setCurrentPage('dashboard');
      } else {
        logout();
      }
    } catch (error) {
      logout();
    }
  };

  const handleRegister = async (username, email) => {
    setLoading(true);
    try {
      // Step 1: Generate keypair from crypto service
      const keyResponse = await axios.post(`${CRYPTO_API_URL}/setup`, {
        user_id: email
      });

      const { public_key, private_key } = keyResponse.data;

      // Step 2: Register user with backend
      const registerResponse = await axios.post(`${API_BASE_URL}/auth/register`, {
        username,
        email,
        public_key
      });

      // Step 3: Store private key securely on client (demo only)
      const userData = {
        id: registerResponse.data.user.id,
        username,
        email,
        private_key,
        public_key
      };

      localStorage.setItem('userData', JSON.stringify(userData));

      alert('Registration successful! Your private key has been saved locally. Keep it safe!');
      setCurrentPage('login');
    } catch (error) {
      console.error('Registration error:', error);
      alert('Registration failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (email) => {
    setLoading(true);
    try {
      // Step 1: Request session from backend
      const sessionResponse = await axios.post(`${API_BASE_URL}/auth/login/request`, {
        email
      });

      const sessionId = sessionResponse.data.sessionId;

      // Step 2: Get user's private key from storage
      const userData = JSON.parse(localStorage.getItem('userData'));
      if (!userData || userData.email !== email) {
        throw new Error('User data not found. Please register first.');
      }

      // Step 3: Generate proof using crypto service
      const proofResponse = await axios.post(`${CRYPTO_API_URL}/prove`, {
        user_id: email,
        private_key: userData.private_key
      });

      const proof = proofResponse.data.proof;

      // Step 4: Submit proof to backend for verification
      const loginResponse = await axios.post(`${API_BASE_URL}/auth/login/submit`, {
        sessionId,
        email,
        proof
      });

      // Step 5: Store auth token and user info
      const token = loginResponse.data.token;
      localStorage.setItem('authToken', token);
      setAuthToken(token);
      setUser(loginResponse.data.user);
      setCurrentPage('dashboard');

      alert('Login successful!');
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    setAuthToken(null);
    setUser(null);
    setCurrentPage('login');
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🔐 ZKAS - Zero-Knowledge Authentication</h1>
          {user && (
            <div className="user-info">
              <span>{user.email}</span>
              <button onClick={logout} className="logout-btn">Logout</button>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        {loading && <div className="loading-spinner">Loading...</div>}
        
        {!loading && currentPage === 'register' && (
          <RegisterPage 
            onRegister={handleRegister}
            onSwitchToLogin={() => setCurrentPage('login')}
          />
        )}

        {!loading && currentPage === 'login' && (
          <LoginPage 
            onLogin={handleLogin}
            onSwitchToRegister={() => setCurrentPage('register')}
          />
        )}

        {!loading && currentPage === 'dashboard' && (
          <DashboardPage user={user} />
        )}
      </main>

      <footer className="app-footer">
        <p>Zero-Knowledge Authentication System • Secure Passwordless Login</p>
      </footer>
    </div>
  );
}
