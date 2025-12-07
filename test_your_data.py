#!/usr/bin/env python3
"""
Test script specifically for your registration data
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_your_signup():
    """Test signup with your specific data"""
    print("Testing signup with your data...")
    
    signup_data = {
        "name": "Ravish Kumar",
        "email": "RAVISH983540@GMAIL.COM",
        "password": "Ravish@99055.",
        "phone_no": "+919905534207"
    }
    
    print(f"Original data: {signup_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Signup successful!")
            return signup_data["email"].lower(), signup_data["password"]
        else:
            print("❌ Signup failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None, None

def test_your_login(email, password):
    """Test login with your data"""
    print("\nTesting login with your data...")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_validation():
    """Test the validation logic locally"""
    import re
    
    print("\nTesting validation logic...")
    
    # Test phone number cleaning
    phone = "+919905534207"
    phone_clean = re.sub(r'\D', '', phone)
    if len(phone_clean) == 12 and phone_clean.startswith('91'):
        phone_clean = phone_clean[2:]
    print(f"Phone: {phone} -> {phone_clean}")
    
    # Test email normalization
    email = "RAVISH983540@GMAIL.COM"
    email_normalized = email.lower()
    print(f"Email: {email} -> {email_normalized}")
    
    # Test name formatting
    name = "Ravish Kumar"
    name_formatted = name.strip().title()
    print(f"Name: {name} -> {name_formatted}")

if __name__ == "__main__":
    print("Testing your specific registration data...")
    print("=" * 50)
    
    # Test validation locally first
    test_validation()
    print("\n" + "=" * 50)
    
    # Test actual signup
    email, password = test_your_signup()
    
    if email and password:
        # Test login
        test_your_login(email, password)
    
    print("\nTest completed!")