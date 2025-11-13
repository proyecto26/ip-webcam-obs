#!/usr/bin/env python3
"""Quick test to check OBS WebSocket connection"""

from obswebsocket import obsws
import sys
import getpass

try:
    print("Testing OBS WebSocket connection...")
    ws = obsws("localhost", 4455, "")
    ws.connect()
    print("✓ Successfully connected to OBS WebSocket!")
    ws.disconnect()
except Exception as e:
    error_msg = str(e).lower()
    
    if "password" in error_msg or "empty response" in error_msg:
        print("\n⚠️  OBS WebSocket requires a password.")
        print("\nYou have two options:")
        print("\n1. Remove the password in OBS:")
        print("   - Go to Tools → WebSocket Server Settings")
        print("   - Uncheck 'Enable authentication'")
        print("   - Click Apply")
        print("\n2. Or test with your password:")
        try:
            password = getpass.getpass("   Enter OBS WebSocket password: ")
            ws = obsws("localhost", 4455, password)
            ws.connect()
            print("\n✓ Successfully connected with password!")
            print(f"\nUse this when running the script:")
            print(f"  python3 ip_webcam_virtual.py <IP> --obs-password '{password}'")
            ws.disconnect()
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(1)
        except Exception as e2:
            print(f"\n✗ Still failed: {e2}")
            sys.exit(1)
    else:
        print(f"✗ Failed to connect: {e}")
        print("\nTo enable WebSocket in OBS:")
        print("1. Open OBS Studio")
        print("2. Go to Tools → WebSocket Server Settings")
        print("3. Check 'Enable WebSocket server'")
        sys.exit(1)
