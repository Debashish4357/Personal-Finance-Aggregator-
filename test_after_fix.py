#!/usr/bin/env python3
"""
Test registration after database fix
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup_after_fix():
    """Test signup after database fix"""
    print("Testing signup after database schema fix...")
    
    signup_data = {
        "name": "Ravish Kumar",
        "email": "ravish983540@gmail.com",  # Using lowercase directly
        "password": "Ravish@99055.",
        "phone_no": "9905534207"  # Clean phone number
    }
    
    print(f"Signup data: {json.dumps(signup_data, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"\nSignup Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
            return response_data.get("user", {}).get("email"), signup_data["password"]
        else:
            print("❌ Registration failed!")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None, None

def test_login_after_signup(email, password):
    """Test login after successful signup"""
    if not email or not password:
        return
        
    print(f"\nTesting login with email: {email}")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Login Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            response_data = response.json()
            print(f"Login response: {json.dumps(response_data, indent=2)}")
        else:
            print("❌ Login failed!")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing registration after database schema fix")
    print("=" * 60)
    
    email, password = test_signup_after_fix()
    test_login_after_signup(email, password)
    
    print("\nTest completed!")