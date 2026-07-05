/**
 * Dashboard Page Component
 * Shows authenticated user information and demo stats
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/dashboard.css';

export default function DashboardPage({ user }) {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/status');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Welcome, {user?.email}! 👋</h2>
        <p>You have successfully authenticated using Zero-Knowledge Proofs</p>
      </div>

      <div className="dashboard-grid">
        <div className="card">
          <h3>🔐 Authentication Method</h3>
          <p>Zero-Knowledge Proof (Fiat-Shamir Protocol)</p>
          <code>Status: Active</code>
        </div>

        <div className="card">
          <h3>🔑 Security Features</h3>
          <ul>
            <li>No password storage</li>
            <li>No phishing vulnerability</li>
            <li>Replay attack resistant</li>
            <li>Cryptographically secure</li>
          </ul>
        </div>

        <div className="card">
          <h3>👤 Account Information</h3>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>User ID:</strong> {user?.userId}</p>
          <p><strong>Private Key:</strong> Stored locally (Never sent to server)</p>
        </div>

        {stats && (
          <div className="card">
            <h3>📊 System Statistics</h3>
            <p><strong>Registered Users:</strong> {stats.registered_users}</p>
            <p><strong>Algorithm:</strong> {stats.zkp_algorithm}</p>
            <p><strong>Key Size:</strong> {stats.modulus_bits} bits</p>
          </div>
        )}
      </div>

      <div className="technical-info">
        <h3>🔬 Technical Details</h3>
        <div className="info-section">
          <h4>How Zero-Knowledge Proofs Work:</h4>
          <ol>
            <li><strong>Setup:</strong> System generates a public/private key pair for you</li>
            <li><strong>Commitment:</strong> You create a mathematical commitment</li>
            <li><strong>Challenge:</strong> Server sends a cryptographic challenge</li>
            <li><strong>Response:</strong> You compute a response using your secret</li>
            <li><strong>Verification:</strong> Server verifies the math without knowing your secret</li>
          </ol>
        </div>

        <div className="info-section">
          <h4>Security Benefits:</h4>
          <ul>
            <li><strong>No Phishing:</strong> No password to steal, only mathematical proofs</li>
            <li><strong>No Replay Attacks:</strong> Each proof includes a unique challenge</li>
            <li><strong>No Data Leaks:</strong> Server only stores public keys, not secrets</li>
            <li><strong>Forward Secrecy:</strong> Even if server is breached, proofs can't be forged</li>
          </ul>
        </div>
      </div>

      <div className="demo-flow">
        <h3>📋 Your Login Flow</h3>
        <div className="flow-step">
          <span className="step-number">1</span>
          <p><strong>Registration:</strong> Your browser generates a ZKP keypair</p>
        </div>
        <div className="flow-step">
          <span className="step-number">2</span>
          <p><strong>Storage:</strong> Private key stored locally, public key on server</p>
        </div>
        <div className="flow-step">
          <span className="step-number">3</span>
          <p><strong>Login Request:</strong> You provide your email</p>
        </div>
        <div className="flow-step">
          <span className="step-number">4</span>
          <p><strong>Proof Generation:</strong> Browser creates a zero-knowledge proof</p>
        </div>
        <div className="flow-step">
          <span className="step-number">5</span>
          <p><strong>Verification:</strong> Server mathematically verifies the proof</p>
        </div>
        <div className="flow-step">
          <span className="step-number">6</span>
          <p><strong>Access Granted:</strong> You're logged in securely!</p>
        </div>
      </div>
    </div>
  );
}
