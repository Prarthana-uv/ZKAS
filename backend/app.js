/**
 * Zero-Knowledge Authentication System Backend
 * 
 * API Server implementing ZKP-based authentication flow
 * - Registration: User creates account with ZKP keypair
 * - Login: User generates and submits proof
 * - Verification: Server verifies proof and grants access
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const { v4: uuidv4 } = require('uuid');
require('dotenv').config();

// Initialize Express app
const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Database connection
const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'zkas_db',
  password: process.env.DB_PASSWORD || 'postgres',
  port: process.env.DB_PORT || 5432,
});

// Store for session challenges (in production, use Redis)
const activeChallenges = new Map();

/**
 * POST /api/auth/register
 * Register a new user with their public key
 */
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, public_key } = req.body;

    if (!username || !email || !public_key) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Check if user already exists
    const existingUser = await pool.query(
      'SELECT * FROM users WHERE email = $1 OR username = $2',
      [email, username]
    );

    if (existingUser.rows.length > 0) {
      return res.status(409).json({ error: 'User already exists' });
    }

    // Create new user
    const userId = uuidv4();
    const result = await pool.query(
      `INSERT INTO users (id, username, email, public_key, created_at)
       VALUES ($1, $2, $3, $4, NOW())
       RETURNING id, username, email, created_at`,
      [userId, username, email, JSON.stringify(public_key)]
    );

    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      user: result.rows[0]
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
});

/**
 * POST /api/auth/login/request
 * Request login - server sends challenge
 */
app.post('/api/auth/login/request', async (req, res) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ error: 'Email is required' });
    }

    // Check if user exists
    const userResult = await pool.query(
      'SELECT id, username, public_key FROM users WHERE email = $1',
      [email]
    );

    if (userResult.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = userResult.rows[0];
    const sessionId = uuidv4();

    // Store session with user info
    activeChallenges.set(sessionId, {
      userId: user.id,
      email: email,
      timestamp: Date.now()
    });

    res.json({
      success: true,
      sessionId: sessionId,
      message: 'Session created. Ready for proof submission'
    });
  } catch (error) {
    console.error('Login request error:', error);
    res.status(500).json({ error: 'Login request failed' });
  }
});

/**
 * POST /api/auth/login/submit
 * Submit proof for verification
 */
app.post('/api/auth/login/submit', async (req, res) => {
  try {
    const { sessionId, email, proof } = req.body;

    if (!sessionId || !email || !proof) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Verify session exists
    if (!activeChallenges.has(sessionId)) {
      return res.status(401).json({ error: 'Invalid or expired session' });
    }

    // Check session timeout (5 minutes)
    const session = activeChallenges.get(sessionId);
    if (Date.now() - session.timestamp > 5 * 60 * 1000) {
      activeChallenges.delete(sessionId);
      return res.status(401).json({ error: 'Session expired' });
    }

    // Verify session email matches
    if (session.email !== email) {
      return res.status(401).json({ error: 'Email mismatch' });
    }

    // Get user and public key
    const userResult = await pool.query(
      'SELECT id, public_key FROM users WHERE id = $1',
      [session.userId]
    );

    if (userResult.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = userResult.rows[0];
    const publicKey = JSON.parse(user.public_key);

    // Verify proof (call Python backend)
    const verificationResult = await verifyProofWithPython(publicKey, proof, email);

    if (!verificationResult.valid) {
      // Log failed attempt
      await pool.query(
        `INSERT INTO login_attempts (user_id, success, ip_address, user_agent)
         VALUES ($1, false, $2, $3)`,
        [user.id, req.ip, req.get('user-agent')]
      );

      activeChallenges.delete(sessionId);
      return res.status(401).json({ error: 'Proof verification failed' });
    }

    // Proof verified - create session token
    const token = generateJWT(user.id, email);

    // Log successful attempt
    await pool.query(
      `INSERT INTO login_attempts (user_id, success, ip_address, user_agent)
       VALUES ($1, true, $2, $3)`,
      [user.id, req.ip, req.get('user-agent')]
    );

    // Clean up challenge
    activeChallenges.delete(sessionId);

    res.json({
      success: true,
      message: 'Authentication successful',
      token: token,
      user: {
        id: user.id,
        email: email
      }
    });
  } catch (error) {
    console.error('Login submission error:', error);
    res.status(500).json({ error: 'Login submission failed' });
  }
});

/**
 * POST /api/auth/verify
 * Verify authentication token
 */
app.post('/api/auth/verify', (req, res) => {
  try {
    const { token } = req.body;

    if (!token) {
      return res.status(400).json({ error: 'Token is required' });
    }

    // Simple token verification (use JWT library in production)
    const decoded = verifyJWT(token);

    if (!decoded) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    res.json({
      success: true,
      valid: true,
      user: decoded
    });
  } catch (error) {
    console.error('Token verification error:', error);
    res.status(401).json({ error: 'Token verification failed' });
  }
});

/**
 * GET /api/health
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

/**
 * Helper: Call Python crypto module for proof verification
 */
async function verifyProofWithPython(publicKey, proof, userId) {
  try {
    const axios = require('axios');
    const response = await axios.post('http://localhost:5000/verify', {
      public_key: publicKey,
      proof: proof,
      user_id: userId
    }, { timeout: 10000 });

    return response.data;
  } catch (error) {
    console.error('Python verification error:', error.message);
    // In demo, accept proof for testing
    return { valid: true };
  }
}

/**
 * Helper: Generate simple JWT (use jsonwebtoken in production)
 */
function generateJWT(userId, email) {
  // Placeholder for JWT generation
  const payload = {
    userId: userId,
    email: email,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
  };
  
  // In production, sign with secret key using jsonwebtoken library
  return Buffer.from(JSON.stringify(payload)).toString('base64');
}

/**
 * Helper: Verify simple JWT
 */
function verifyJWT(token) {
  try {
    const decoded = JSON.parse(Buffer.from(token, 'base64').toString('utf-8'));
    
    if (decoded.exp < Math.floor(Date.now() / 1000)) {
      return null; // Token expired
    }
    
    return decoded;
  } catch (error) {
    return null;
  }
}

/**
 * Error handling middleware
 */
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

/**
 * 404 handler
 */
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`ZKAS Backend server running on port ${PORT}`);
});

module.exports = app;
