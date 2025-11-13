#!/usr/bin/env python3
"""
IP Webcam to Virtual Camera via OBS
Streams an IP Webcam feed to OBS virtual camera on macOS.
Requires: OBS Studio with WebSocket plugin enabled
"""

import argparse
import sys
import time
import os
from pathlib import Path
from obswebsocket import obsws, requests as obs_requests

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, will use CLI args only


def main():
    parser = argparse.ArgumentParser(
        description="Stream IP Webcam to OBS virtual camera"
    )
    parser.add_argument(
        "ip_address",
        nargs='?',
        default=os.getenv('ANDROID_IP'),
        help="IP address of the IP Webcam server (e.g., 192.168.1.100:8080). Can also be set in .env file as ANDROID_IP"
    )
    parser.add_argument(
        "--obs-host",
        default=os.getenv('OBS_HOST', 'localhost'),
        help="OBS WebSocket host (default: localhost or OBS_HOST from .env)"
    )
    parser.add_argument(
        "--obs-port",
        type=int,
        default=int(os.getenv('OBS_PORT', '4455')),
        help="OBS WebSocket port (default: 4455 or OBS_PORT from .env)"
    )
    parser.add_argument(
        "--obs-password",
        default=os.getenv('OBS_PASSWORD', ''),
        help="OBS WebSocket password (if set). Can also be set in .env file as OBS_PASSWORD"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=int(os.getenv('VIDEO_WIDTH', '1920')),
        help="Output width (default: 1920 or VIDEO_WIDTH from .env)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=int(os.getenv('VIDEO_HEIGHT', '1080')),
        help="Output height (default: 1080 or VIDEO_HEIGHT from .env)"
    )
    
    args = parser.parse_args()
    
    # Validate that we have an IP address
    if not args.ip_address:
        print("Error: No IP address provided.")
        print("Either pass it as an argument or set ANDROID_IP in .env file")
        print("\nExample usage:")
        print("  python3 ip_webcam_virtual.py 192.168.1.100:8080")
        print("\nOr create a .env file (see .env.example)")
        sys.exit(1)
    
    # Build the video stream URL
    if not args.ip_address.startswith("http"):
        stream_url = f"http://{args.ip_address}/video"
    else:
        stream_url = f"{args.ip_address}/video"
    
    print(f"Connecting to OBS at {args.obs_host}:{args.obs_port}...")
    
    try:
        ws = obsws(args.obs_host, args.obs_port, args.obs_password)
        ws.connect()
        print("✓ Connected to OBS")
    except Exception as e:
        print(f"Error: Could not connect to OBS WebSocket")
        print(f"Details: {e}")
        print("\nMake sure:")
        print("  1. OBS Studio is running")
        print("  2. WebSocket server is enabled in OBS")
        print("     (Tools → WebSocket Server Settings)")
        sys.exit(1)
    
    try:
        # Check if source already exists
        source_name = "IP_Webcam_Feed"
        scene_name = "IP Webcam Scene"
        
        # Get or create scene
        try:
            ws.call(obs_requests.GetSceneList())
            scenes = ws.call(obs_requests.GetSceneList()).getScenes()
            scene_exists = any(s['sceneName'] == scene_name for s in scenes)
            
            if not scene_exists:
                print(f"Creating scene: {scene_name}")
                ws.call(obs_requests.CreateScene(sceneName=scene_name))
        except Exception as e:
            print(f"Error managing scenes: {e}")
        
        # Create browser source for IP Webcam
        try:
            print(f"Setting up video source from: {stream_url}")
            
            # Remove existing source if present
            try:
                ws.call(obs_requests.RemoveInput(inputName=source_name))
            except:
                pass
            
            # Create new browser source
            settings = {
                "url": stream_url,
                "width": args.width,
                "height": args.height,
                "fps_custom": True,
                "fps": 30
            }
            
            ws.call(obs_requests.CreateInput(
                sceneName=scene_name,
                inputName=source_name,
                inputKind="browser_source",
                inputSettings=settings
            ))
            print(f"✓ Created video source: {source_name}")
            
        except Exception as e:
            print(f"Error creating source: {e}")
            sys.exit(1)
        
        # Set the scene as current
        try:
            ws.call(obs_requests.SetCurrentProgramScene(sceneName=scene_name))
            print(f"✓ Activated scene: {scene_name}")
        except Exception as e:
            print(f"Error setting scene: {e}")
        
        # Start virtual camera
        try:
            # Check if virtual camera is already running
            status = ws.call(obs_requests.GetVirtualCamStatus())
            if not status.getOutputActive():
                ws.call(obs_requests.StartVirtualCam())
                print("✓ Virtual camera started!")
            else:
                print("✓ Virtual camera already running")
        except Exception as e:
            print(f"Error starting virtual camera: {e}")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("Virtual camera is now active!")
        print("You can use 'OBS Virtual Camera' in other apps")
        print("Press Ctrl+C to stop")
        print("="*50 + "\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping virtual camera...")
            ws.call(obs_requests.StopVirtualCam())
            print("✓ Virtual camera stopped")
    
    finally:
        ws.disconnect()
        print("Done!")


if __name__ == "__main__":
    main()
