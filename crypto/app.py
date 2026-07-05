"""
Crypto Service API - Flask wrapper around ZKP protocol
Provides REST API for proof generation and verification
"""

from flask import Flask, request, jsonify
import json
from crypto.zkp_fiat_shamir import FiatShamirZKP, ZKPParameters, PrivateKey, PublicKey, Proof

app = Flask(__name__)

# Initialize ZKP system
params, _, _ = FiatShamirZKP.setup()
zkp = FiatShamirZKP(params)

# Store for demo (in production, use database)
user_keys = {}


@app.route('/setup', methods=['POST'])
def setup_user():
    """
    Generate keypair for new user
    
    Request:
        {
            "user_id": "user@example.com"
        }
    
    Response:
        {
            "success": true,
            "public_key": {...},
            "private_key": {...}
        }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        if user_id in user_keys:
            return jsonify({'error': 'User already exists'}), 409
        
        # Generate keypair
        _, pub_key, priv_key = FiatShamirZKP.setup()
        
        # Store public key (private key goes to user)
        user_keys[user_id] = pub_key.to_dict()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'public_key': pub_key.to_dict(),
            'private_key': priv_key.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/prove', methods=['POST'])
def prove():
    """
    Generate ZKP proof for authentication
    
    Request:
        {
            "user_id": "user@example.com",
            "private_key": {...}
        }
    
    Response:
        {
            "success": true,
            "proof": {...}
        }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        priv_key_data = data.get('private_key')
        
        if not user_id or not priv_key_data:
            return jsonify({'error': 'user_id and private_key required'}), 400
        
        if user_id not in user_keys:
            return jsonify({'error': 'User not found'}), 404
        
        # Reconstruct private key
        priv_key = PrivateKey.from_dict(priv_key_data)
        
        # Generate proof
        proof = zkp.prove(priv_key, user_id=user_id)
        
        return jsonify({
            'success': True,
            'proof': proof.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/verify', methods=['POST'])
def verify():
    """
    Verify ZKP proof
    
    Request:
        {
            "user_id": "user@example.com",
            "proof": {...}
        }
    
    Response:
        {
            "valid": true/false,
            "message": "..."
        }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        proof_data = data.get('proof')
        
        if not user_id or not proof_data:
            return jsonify({'error': 'user_id and proof required'}), 400
        
        if user_id not in user_keys:
            return jsonify({'error': 'User not found'}), 404
        
        # Reconstruct proof and public key
        proof = Proof.from_dict(proof_data)
        pub_key = PublicKey.from_dict(user_keys[user_id])
        
        # Verify proof
        is_valid = zkp.verify(pub_key, proof, user_id=user_id)
        
        return jsonify({
            'valid': is_valid,
            'user_id': user_id,
            'message': 'Proof verified successfully' if is_valid else 'Proof verification failed'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ZKAS Crypto Service'
    }), 200


@app.route('/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        'registered_users': len(user_keys),
        'zkp_algorithm': 'Fiat-Shamir',
        'modulus_bits': params.n.bit_length()
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
