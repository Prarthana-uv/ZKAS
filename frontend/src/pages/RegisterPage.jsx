/**
 * Registration Page Component
 * Allows new users to register for ZKP-based authentication
 */

import React, { useState } from 'react';
import '../styles/auth.css';

export default function RegisterPage({ onRegister, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username || !email) {
      alert('Please fill in all fields');
      return;
    }

    if (!agreeTerms) {
      alert('Please agree to the terms and conditions');
      return;
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('Please enter a valid email');
      return;
    }

    setLoading(true);
    try {
      await onRegister(username, email);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p className="subtitle">Join ZKAS for secure passwordless authentication</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              disabled={loading}
            />
          </div>

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

          <div className="form-group checkbox">
            <input
              id="terms"
              type="checkbox"
              checked={agreeTerms}
              onChange={(e) => setAgreeTerms(e.target.checked)}
              disabled={loading}
            />
            <label htmlFor="terms">
              I agree to the terms and conditions
            </label>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div className="info-box">
          <h4>ℹ️ About Zero-Knowledge Proofs</h4>
          <ul>
            <li>Your private key never leaves your device</li>
            <li>No passwords are stored on our servers</li>
            <li>Authentication happens through mathematical proofs</li>
            <li>Resistant to phishing and data breaches</li>
          </ul>
        </div>

        <p className="switch-auth">
          Already have an account?{' '}
          <button
            type="button"
            className="link-btn"
            onClick={onSwitchToLogin}
          >
            Login here
          </button>
        </p>
      </div>
    </div>
  );
}
