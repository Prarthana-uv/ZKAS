"""
Unit tests for Fiat-Shamir ZKP implementation
"""

import pytest
from crypto.zkp_fiat_shamir import (
    FiatShamirZKP, ZKPParameters, PublicKey, PrivateKey,
    Commitment, Challenge, Response, Proof
)


class TestFiatShamirZKP:
    """Test suite for Fiat-Shamir implementation"""
    
    @pytest.fixture
    def zkp_setup(self):
        """Setup ZKP system for testing"""
        params, pub_key, priv_key = FiatShamirZKP.setup()
        zkp = FiatShamirZKP(params)
        return params, pub_key, priv_key, zkp
    
    def test_setup(self):
        """Test system setup"""
        params, pub_key, priv_key = FiatShamirZKP.setup()
        
        assert params is not None
        assert pub_key is not None
        assert priv_key is not None
        assert pub_key.v > 0
        assert priv_key.s > 0
    
    def test_commitment_generation(self, zkp_setup):
        """Test commitment phase"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        commitment, r = zkp.generate_commitment(priv_key)
        
        assert commitment is not None
        assert commitment.t > 0
        assert r > 0
    
    def test_challenge_generation(self, zkp_setup):
        """Test challenge generation"""
        params, pub_key, priv_key, zkp = zkp_setup
        commitment, r = zkp.generate_commitment(priv_key)
        
        challenge = zkp.generate_challenge(commitment, user_id="test@example.com")
        
        assert challenge is not None
        assert 0 <= challenge.c < params.n
    
    def test_challenge_deterministic(self, zkp_setup):
        """Test that challenges are deterministic for same commitment"""
        params, pub_key, priv_key, zkp = zkp_setup
        commitment, r = zkp.generate_commitment(priv_key)
        user_id = "test@example.com"
        
        challenge1 = zkp.generate_challenge(commitment, user_id)
        challenge2 = zkp.generate_challenge(commitment, user_id)
        
        assert challenge1.c == challenge2.c
    
    def test_response_generation(self, zkp_setup):
        """Test response phase"""
        params, pub_key, priv_key, zkp = zkp_setup
        commitment, r = zkp.generate_commitment(priv_key)
        challenge = zkp.generate_challenge(commitment)
        
        response = zkp.generate_response(priv_key, challenge, r)
        
        assert response is not None
        assert 0 <= response.z < params.n
    
    def test_proof_verification_valid(self, zkp_setup):
        """Test verification of valid proof"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        # Generate complete proof
        proof = zkp.prove(priv_key)
        
        # Verify proof
        is_valid = zkp.verify_proof(pub_key, proof)
        
        assert is_valid is True
    
    def test_proof_verification_invalid_response(self, zkp_setup):
        """Test verification fails with modified response"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        proof = zkp.prove(priv_key)
        
        # Tamper with response
        proof.response.z = (proof.response.z + 1) % params.n
        
        is_valid = zkp.verify_proof(pub_key, proof)
        
        assert is_valid is False
    
    def test_proof_verification_invalid_commitment(self, zkp_setup):
        """Test verification fails with modified commitment"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        proof = zkp.prove(priv_key)
        
        # Tamper with commitment
        proof.commitment.t = (proof.commitment.t + 1) % params.n
        
        is_valid = zkp.verify_proof(pub_key, proof)
        
        assert is_valid is False
    
    def test_full_prove_verify_cycle(self, zkp_setup):
        """Test complete prove and verify cycle"""
        params, pub_key, priv_key, zkp = zkp_setup
        user_id = "alice@example.com"
        
        # Prover generates proof
        proof = zkp.prove(priv_key, user_id=user_id)
        
        # Verifier checks proof
        is_valid = zkp.verify(pub_key, proof, user_id=user_id)
        
        assert is_valid is True
    
    def test_full_cycle_wrong_user_id(self, zkp_setup):
        """Test verification fails with wrong user_id"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        proof = zkp.prove(priv_key, user_id="alice@example.com")
        
        # Try to verify with different user_id
        is_valid = zkp.verify(pub_key, proof, user_id="bob@example.com")
        
        assert is_valid is False
    
    def test_proof_serialization(self, zkp_setup):
        """Test proof serialization to/from JSON"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        # Generate proof
        proof = zkp.prove(priv_key)
        
        # Serialize to JSON
        json_str = proof.to_json()
        
        # Deserialize from JSON
        proof_restored = Proof.from_json(json_str)
        
        # Verify restored proof
        is_valid = zkp.verify_proof(pub_key, proof_restored)
        
        assert is_valid is True
    
    def test_public_key_serialization(self):
        """Test public key serialization"""
        pub_key = PublicKey(v=12345)
        
        # Serialize
        data = pub_key.to_dict()
        
        # Deserialize
        restored = PublicKey.from_dict(data)
        
        assert restored.v == pub_key.v
    
    def test_private_key_serialization(self):
        """Test private key serialization"""
        priv_key = PrivateKey(s=67890)
        
        # Serialize
        data = priv_key.to_dict()
        
        # Deserialize
        restored = PrivateKey.from_dict(data)
        
        assert restored.s == priv_key.s
    
    def test_multiple_proofs_different(self, zkp_setup):
        """Test that multiple proofs for same key are different"""
        params, pub_key, priv_key, zkp = zkp_setup
        
        proof1 = zkp.prove(priv_key)
        proof2 = zkp.prove(priv_key)
        
        # Proofs should be different (different random r values)
        assert proof1.response.z != proof2.response.z
        
        # But both should verify
        assert zkp.verify_proof(pub_key, proof1) is True
        assert zkp.verify_proof(pub_key, proof2) is True
    
    def test_replay_attack_prevention(self, zkp_setup):
        """Test that proofs cannot be replayed with different challenge"""
        params, pub_key, priv_key, zkp = zkp_setup
        user_id = "user@example.com"
        
        proof = zkp.prove(priv_key, user_id=user_id)
        
        # Try to verify with different user_id (simulates replay attack)
        is_valid = zkp.verify(pub_key, proof, user_id="different@example.com")
        
        assert is_valid is False


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
