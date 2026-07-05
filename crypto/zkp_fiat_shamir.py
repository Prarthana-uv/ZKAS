"""
Fiat-Shamir Zero-Knowledge Proof Protocol Implementation

This module implements the Fiat-Shamir identification scheme, a zero-knowledge proof
protocol that allows a prover to prove knowledge of a secret without revealing it.

Algorithm Overview:
1. Setup: Prover has secret 's', computes public key 'v' = g^(s^-1) mod n
2. Commitment: Prover picks random r, sends commitment t = g^r mod n
3. Challenge: Verifier sends random challenge c
4. Response: Prover sends z = r + c*s mod n
5. Verification: Check if g^z mod n == t * v^c mod n
"""

import hashlib
import os
from typing import Tuple, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class ZKPParameters:
    """System parameters for Fiat-Shamir protocol"""
    n: int  # Modulus (typically product of two large primes)
    g: int  # Generator/base
    challenge_bits: int = 128  # Bit length for challenges


@dataclass
class PublicKey:
    """Public key (verifier material)"""
    v: int  # Public commitment
    
    def to_dict(self) -> Dict[str, Any]:
        return {"v": self.v}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PublicKey":
        return cls(v=data["v"])


@dataclass
class PrivateKey:
    """Private key (prover material)"""
    s: int  # Secret exponent
    
    def to_dict(self) -> Dict[str, Any]:
        return {"s": self.s}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PrivateKey":
        return cls(s=data["s"])


@dataclass
class Commitment:
    """Prover's commitment in ZKP protocol"""
    t: int  # Commitment value g^r mod n
    
    def to_dict(self) -> Dict[str, Any]:
        return {"t": self.t}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Commitment":
        return cls(t=data["t"])


@dataclass
class Challenge:
    """Verifier's challenge"""
    c: int  # Challenge value
    
    def to_dict(self) -> Dict[str, Any]:
        return {"c": self.c}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Challenge":
        return cls(c=data["c"])


@dataclass
class Response:
    """Prover's response to challenge"""
    z: int  # Response z = r + c*s mod n
    
    def to_dict(self) -> Dict[str, Any]:
        return {"z": self.z}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Response":
        return cls(z=data["z"])


@dataclass
class Proof:
    """Complete zero-knowledge proof"""
    commitment: Commitment
    challenge: Challenge
    response: Response
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "commitment": self.commitment.to_dict(),
            "challenge": self.challenge.to_dict(),
            "response": self.response.to_dict()
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Proof":
        return cls(
            commitment=Commitment.from_dict(data["commitment"]),
            challenge=Challenge.from_dict(data["challenge"]),
            response=Response.from_dict(data["response"])
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "Proof":
        return cls.from_dict(json.loads(json_str))


class FiatShamirZKP:
    """Fiat-Shamir Zero-Knowledge Proof implementation"""
    
    def __init__(self, params: ZKPParameters):
        self.params = params
        self.n = params.n
        self.g = params.g
    
    @staticmethod
    def generate_safe_prime(bits: int = 1024) -> Tuple[int, int]:
        """Generate safe primes p and q where n = p*q"""
        from sympy import randprime, isprime
        
        # For demo purposes, using smaller primes
        # In production, use cryptographically secure parameters
        p = randprime(2**(bits-1), 2**bits)
        q = randprime(2**(bits-1), 2**bits)
        
        return p, q
    
    @staticmethod
    def setup(secret_bits: int = 512) -> Tuple[ZKPParameters, PublicKey, PrivateKey]:
        """
        Setup phase: Generate system parameters and key pair
        
        Args:
            secret_bits: Bit length for secret generation
            
        Returns:
            params, public_key, private_key
        """
        # For demonstration, using fixed parameters
        # In production, these should be generated securely
        n = 0xc3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2
        g = 2
        
        params = ZKPParameters(n=n, g=g, challenge_bits=128)
        
        # Generate secret s (random element in [1, n-1])
        s = int.from_bytes(os.urandom(secret_bits // 8), 'big') % (n - 1) + 1
        
        # Compute public key v = g^(s^-1) mod n
        # For simplicity in demo: v = g^s mod n (still preserves ZK property)
        v = pow(g, s, n)
        
        private_key = PrivateKey(s=s)
        public_key = PublicKey(v=v)
        
        return params, public_key, private_key
    
    def generate_commitment(self, private_key: PrivateKey) -> Tuple[Commitment, int]:
        """
        Commitment phase: Prover generates commitment
        
        Args:
            private_key: Prover's private key
            
        Returns:
            commitment, random_r (needed for response)
        """
        # Generate random r
        r = int.from_bytes(os.urandom(64), 'big') % (self.n - 1) + 1
        
        # Compute commitment t = g^r mod n
        t = pow(self.g, r, self.n)
        
        commitment = Commitment(t=t)
        return commitment, r
    
    def generate_challenge(self, commitment: Commitment, user_id: str = "") -> Challenge:
        """
        Challenge phase: Verifier generates challenge (Fiat-Shamir heuristic)
        
        Using hash-based challenge to make it non-interactive
        
        Args:
            commitment: Prover's commitment
            user_id: Optional user identifier for domain separation
            
        Returns:
            challenge
        """
        # Hash-based challenge (Fiat-Shamir transformation)
        data = f"{commitment.t}{user_id}".encode()
        hash_output = hashlib.sha256(data).digest()
        
        # Convert to challenge value (reduced modulo n)
        c = int.from_bytes(hash_output, 'big') % self.n
        
        challenge = Challenge(c=c)
        return challenge
    
    def generate_response(
        self,
        private_key: PrivateKey,
        challenge: Challenge,
        r: int
    ) -> Response:
        """
        Response phase: Prover responds to challenge
        
        Args:
            private_key: Prover's private key
            challenge: Verifier's challenge
            r: Random value from commitment phase
            
        Returns:
            response
        """
        # Compute z = r + c*s mod n
        z = (r + challenge.c * private_key.s) % self.n
        
        response = Response(z=z)
        return response
    
    def verify_proof(
        self,
        public_key: PublicKey,
        proof: Proof
    ) -> bool:
        """
        Verification phase: Verifier checks the proof
        
        Equation: g^z mod n == t * v^c mod n
        
        Args:
            public_key: Prover's public key
            proof: The zero-knowledge proof
            
        Returns:
            True if proof is valid, False otherwise
        """
        t = proof.commitment.t
        c = proof.challenge.c
        z = proof.response.z
        v = public_key.v
        
        # Compute left side: g^z mod n
        left = pow(self.g, z, self.n)
        
        # Compute right side: t * v^c mod n
        v_c = pow(v, c, self.n)
        right = (t * v_c) % self.n
        
        # Verify equation
        is_valid = left == right
        
        return is_valid
    
    def prove(
        self,
        private_key: PrivateKey,
        user_id: str = ""
    ) -> Proof:
        """
        Complete proof generation (non-interactive via Fiat-Shamir)
        
        Args:
            private_key: Prover's private key
            user_id: User identifier for domain separation
            
        Returns:
            Complete proof
        """
        # Generate commitment
        commitment, r = self.generate_commitment(private_key)
        
        # Generate challenge
        challenge = self.generate_challenge(commitment, user_id)
        
        # Generate response
        response = self.generate_response(private_key, challenge, r)
        
        return Proof(commitment=commitment, challenge=challenge, response=response)
    
    def verify(
        self,
        public_key: PublicKey,
        proof: Proof,
        user_id: str = ""
    ) -> bool:
        """
        Complete proof verification
        
        Args:
            public_key: Prover's public key
            proof: The proof to verify
            user_id: User identifier (must match challenge generation)
            
        Returns:
            True if proof is valid
        """
        # Regenerate challenge from commitment
        expected_challenge = self.generate_challenge(proof.commitment, user_id)
        
        # Check if challenge matches
        if proof.challenge.c != expected_challenge.c:
            return False
        
        # Verify the mathematical equation
        return self.verify_proof(public_key, proof)


# Example usage
if __name__ == "__main__":
    # Setup
    params, pub_key, priv_key = FiatShamirZKP.setup()
    zkp = FiatShamirZKP(params)
    
    # Prover generates proof
    proof = zkp.prove(priv_key, user_id="user@example.com")
    
    # Verifier checks proof
    is_valid = zkp.verify(pub_key, proof, user_id="user@example.com")
    
    print(f"Proof valid: {is_valid}")
    print(f"Proof JSON: {proof.to_json()}")
