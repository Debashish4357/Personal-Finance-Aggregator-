#!/usr/bin/env python3
"""
Simple test script for authentication endpoints
Run this after starting the server to test signup and login functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    print("Testing user signup...")
    
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
        "phone_no": "1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"Signup Status Code: {response.status_code}")
        print(f"Signup Response: {response.json()}")
        
        if response.status_code == 200:
            return signup_data["email"], signup_data["password"]
        
    except requests.exceptions.RequestException as e:
        print(f"Error during signup: {e}")
    
    return None, None

def test_login(email, password):
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Login Status Code: {response.status_code}")
        print(f"Login Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")

def test_duplicate_signup():
    """Test duplicate signup (should fail)"""
    print("\nTesting duplicate signup...")
    
    signup_data = {
        "name": "Test User 2",
        "email": "test@example.com",  # Same email
        "password": "testpass123",
        "phone_no": "1234567891"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"Duplicate Signup Status Code: {response.status_code}")
        print(f"Duplicate Signup Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error during duplicate signup: {e}")

if __name__ == "__main__":
    print("Starting authentication tests...")
    print("Make sure your server is running on http://localhost:8000")
    print("-" * 50)
    
    # Test signup
    email, password = test_signup()
    
    if email and password:
        # Test login with created user
        test_login(email, password)
        
        # Test duplicate signup
        test_duplicate_signup()
        
        # Test wrong password
        print("\nTesting wrong password...")
        test_login(email, "wrongpassword")
        
    print("\nTests completed!")