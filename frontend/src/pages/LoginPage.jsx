/**
 * Login Page Component
 * Handles ZKP-based authentication
 */

import React, { useState } from 'react';
import '../styles/auth.css';

export default function LoginPage({ onLogin, onSwitchToRegister }) {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      alert('Please enter your email');
      return;
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('Please enter a valid email');
      return;
    }

    // Check if user has private key stored
    const userData = JSON.parse(localStorage.getItem('userData') || 'null');
    if (!userData || userData.email !== email) {
      alert('User not found. Please register first.');
      return;
    }

    setLoading(true);
    try {
      await onLogin(email);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>
        <p className="subtitle">Prove your identity with Zero-Knowledge Proofs</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Authenticating...' : 'Login with ZKP'}
          </button>
        </form>

        <div className="info-box">
          <h4>🔐 How it works</h4>
          <ol>
            <li>You provide your email address</li>
            <li>Your browser generates a zero-knowledge proof</li>
            <li>The proof is sent to the server for verification</li>
            <li>Server confirms you know the secret without revealing it</li>
            <li>You're logged in securely!</li>
          </ol>
        </div>

        <div className="features">
          <div className="feature">
            <span>✅</span>
            <p>No passwords</p>
          </div>
          <div className="feature">
            <span>🛡️</span>
            <p>No phishing</p>
          </div>
          <div className="feature">
            <span>🚀</span>
            <p>Math-based</p>
          </div>
        </div>

        <p className="switch-auth">
          Don't have an account?{' '}
          <button
            type="button"
            className="link-btn"
            onClick={onSwitchToRegister}
          >
            Register here
          </button>
        </p>
      </div>
    </div>
  );
}
