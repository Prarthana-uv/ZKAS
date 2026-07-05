"""
ZKAS Usage Example - Zero-Knowledge Authentication System

This example demonstrates how to use the ZKAS system:
1. User registration
2. Proof generation
3. Authentication verification
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:3000/api"
CRYPTO_URL = "http://localhost:5000"

def example_complete_flow():
    """Complete authentication flow example"""
    
    print("\n" + "="*60)
    print("ZKAS - Zero-Knowledge Authentication Example")
    print("="*60)
    
    # Step 1: Generate Keypair
    print("\n1️⃣  REGISTRATION - Generating keypair...")
    
    user_id = "alice@example.com"
    setup_response = requests.post(
        f"{CRYPTO_URL}/setup",
        json={"user_id": user_id}
    ).json()
    
    public_key = setup_response["public_key"]
    private_key = setup_response["private_key"]
    
    print(f"   Public Key (v):  {public_key['v']}")
    print(f"   Private Key (s): {private_key['s']}")
    
    # Step 2: Register with Backend
    print("\n2️⃣  REGISTRATION - Registering with backend...")
    
    register_response = requests.post(
        f"{BACKEND_URL}/auth/register",
        json={
            "username": "alice",
            "email": user_id,
            "public_key": public_key
        }
    ).json()
    
    print(f"   Status: {register_response['success']}")
    print(f"   User ID: {register_response['user']['id']}")
    
    # Step 3: Request Login Session
    print("\n3️⃣  LOGIN - Requesting session...")
    
    login_request_response = requests.post(
        f"{BACKEND_URL}/auth/login/request",
        json={"email": user_id}
    ).json()
    
    session_id = login_request_response["sessionId"]
    print(f"   Session ID: {session_id}")
    
    # Step 4: Generate Proof
    print("\n4️⃣  LOGIN - Generating zero-knowledge proof...")
    
    prove_response = requests.post(
        f"{CRYPTO_URL}/prove",
        json={
            "user_id": user_id,
            "private_key": private_key
        }
    ).json()
    
    proof = prove_response["proof"]
    print(f"   Commitment (t):  {proof['commitment']['t']}")
    print(f"   Challenge (c):   {proof['challenge']['c']}")
    print(f"   Response (z):    {proof['response']['z']}")
    
    # Step 5: Submit Proof for Verification
    print("\n5️⃣  LOGIN - Submitting proof to server...")
    
    login_submit_response = requests.post(
        f"{BACKEND_URL}/auth/login/submit",
        json={
            "sessionId": session_id,
            "email": user_id,
            "proof": proof
        }
    ).json()
    
    if login_submit_response["success"]:
        print(f"   ✅ Authentication successful!")
        token = login_submit_response["token"]
        print(f"   Token: {token}")
    else:
        print(f"   ❌ Authentication failed!")
        return
    
    # Step 6: Verify Token
    print("\n6️⃣  VERIFY - Verifying authentication token...")
    
    verify_response = requests.post(
        f"{BACKEND_URL}/auth/verify",
        json={"token": token}
    ).json()
    
    if verify_response["valid"]:
        print(f"   ✅ Token is valid!")
        print(f"   User: {verify_response['user']['email']}")
    else:
        print(f"   ❌ Token is invalid!")
    
    # Step 7: Demonstrate Proof Non-Transferability
    print("\n7️⃣  SECURITY - Testing proof reusability...")
    
    # Try to reuse the same proof
    login_request_response2 = requests.post(
        f"{BACKEND_URL}/auth/login/request",
        json={"email": user_id}
    ).json()
    
    session_id2 = login_request_response2["sessionId"]
    
    # Try to submit old proof with new session
    replay_response = requests.post(
        f"{BACKEND_URL}/auth/login/submit",
        json={
            "sessionId": session_id2,
            "email": user_id,
            "proof": proof
        }
    ).json()
    
    if not replay_response["success"]:
        print(f"   ✅ Replay attack blocked! (proof cannot be reused)")
    else:
        print(f"   ⚠️  Warning: Proof was accepted (shouldn't happen)")
    
    print("\n" + "="*60)
    print("✨ Example Complete - All steps successful!")
    print("="*60 + "\n")


def example_crypto_api():
    """Direct cryptographic API usage"""
    
    print("\n" + "="*60)
    print("ZKAS Crypto API - Direct Usage")
    print("="*60)
    
    # Setup
    print("\n📝 Setting up new user cryptography...")
    setup = requests.post(
        f"{CRYPTO_URL}/setup",
        json={"user_id": "bob@example.com"}
    ).json()
    
    print(f"   Generated public key: {setup['public_key']}")
    
    # Prove
    print("\n🔐 Generating zero-knowledge proof...")
    prove = requests.post(
        f"{CRYPTO_URL}/prove",
        json={
            "user_id": "bob@example.com",
            "private_key": setup['private_key']
        }
    ).json()
    
    print(f"   Proof generated successfully")
    print(f"   Proof JSON: {json.dumps(prove['proof'], indent=2)}")
    
    # Verify
    print("\n✅ Verifying proof...")
    verify = requests.post(
        f"{CRYPTO_URL}/verify",
        json={
            "user_id": "bob@example.com",
            "proof": prove['proof']
        }
    ).json()
    
    if verify['valid']:
        print(f"   ✅ Proof verification successful!")
    else:
        print(f"   ❌ Proof verification failed!")
    
    print("\n" + "="*60 + "\n")


def example_api_endpoints():
    """Show all available API endpoints"""
    
    print("\n" + "="*60)
    print("ZKAS API Endpoints Reference")
    print("="*60)
    
    endpoints = {
        "Authentication": [
            {
                "method": "POST",
                "path": "/api/auth/register",
                "description": "Register new user",
                "body": {
                    "username": "string",
                    "email": "string",
                    "public_key": {"v": "integer"}
                }
            },
            {
                "method": "POST",
                "path": "/api/auth/login/request",
                "description": "Request login session",
                "body": {"email": "string"}
            },
            {
                "method": "POST",
                "path": "/api/auth/login/submit",
                "description": "Submit ZKP proof",
                "body": {
                    "sessionId": "string",
                    "email": "string",
                    "proof": {"commitment": {}, "challenge": {}, "response": {}}
                }
            },
            {
                "method": "POST",
                "path": "/api/auth/verify",
                "description": "Verify token",
                "body": {"token": "string"}
            }
        ],
        "Cryptography": [
            {
                "method": "POST",
                "path": "/setup",
                "description": "Generate keypair",
                "body": {"user_id": "string"}
            },
            {
                "method": "POST",
                "path": "/prove",
                "description": "Generate proof",
                "body": {
                    "user_id": "string",
                    "private_key": {"s": "integer"}
                }
            },
            {
                "method": "POST",
                "path": "/verify",
                "description": "Verify proof",
                "body": {
                    "user_id": "string",
                    "proof": {}
                }
            },
            {
                "method": "GET",
                "path": "/health",
                "description": "Health check",
                "body": None
            }
        ]
    }
    
    for category, eps in endpoints.items():
        print(f"\n📍 {category}:")
        for ep in eps:
            print(f"   {ep['method']} {ep['path']}")
            print(f"      → {ep['description']}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        # Run examples
        example_api_endpoints()
        example_crypto_api()
        example_complete_flow()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to ZKAS services")
        print("   Make sure services are running:")
        print("   docker-compose up -d")
    except Exception as e:
        print(f"❌ Error: {e}")
