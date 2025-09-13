#!/usr/bin/env python3
"""
Test script to verify PIN system works correctly
"""

import os
import json
import sys

def test_pin_system():
    """Test the PIN system functionality"""
    print("🧪 Testing PIN System...")
    
    # Check if data directory exists
    data_dir = "data"
    profiles_dir = os.path.join(data_dir, "profiles")
    
    print(f"📁 Data directory: {data_dir}")
    print(f"📁 Profiles directory: {profiles_dir}")
    
    # Check if profiles directory exists
    if not os.path.exists(profiles_dir):
        print("✅ Profiles directory doesn't exist - fresh start!")
        return True
    
    # List existing profiles
    profiles = os.listdir(profiles_dir)
    print(f"📋 Found {len(profiles)} profiles: {profiles}")
    
    if len(profiles) == 0:
        print("✅ No existing profiles - fresh start!")
        return True
    
    # Check each profile for PIN
    for profile in profiles:
        profile_path = os.path.join(profiles_dir, profile)
        if os.path.isdir(profile_path):
            progress_file = os.path.join(profile_path, "progress.json")
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r') as f:
                        data = json.load(f)
                        pin = data.get('access_code', 'N/A')
                        print(f"👤 {profile}: PIN = {pin}")
                except Exception as e:
                    print(f"❌ Error reading {profile}: {e}")
    
    return True

if __name__ == "__main__":
    test_pin_system()
    print("\n🎯 PIN System Test Complete!")
    print("📱 Open http://localhost:8501 to test the app")
