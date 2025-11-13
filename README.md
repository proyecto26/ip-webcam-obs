# IP Webcam to Virtual Camera

Convert your Android device into a virtual webcam on macOS using IP Webcam app and OBS Studio.

## Setup

### 1. Install OBS Studio
```bash
brew install --cask obs
```

### 2. Enable OBS Virtual Camera Extension
**Important:** This is required for the virtual camera to work in other apps.

1. Open OBS Studio
2. Go to **Tools → Start Virtual Camera**
3. If prompted with "The virtual camera is not installed", click **OK**
4. macOS will open **System Settings** automatically
5. Navigate to: **General → Login Items & Extensions → Camera Extensions**
6. Find **"OBS Virtual Camera"** and **enable it** (toggle on)
7. **Restart OBS Studio**

### 3. Enable OBS WebSocket Server
1. Open OBS Studio
2. Go to **Tools → WebSocket Server Settings**
3. Check **Enable WebSocket server**
4. Note the port (default: 4455) and password (if set)
5. Click **Apply** and **OK**

### 4. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the example environment file and fill in your values:
```bash
cp .env.example .env
```

Edit `.env` and set:
- `ANDROID_IP`: Your Android device IP (you'll get this from the IP Webcam app)
- `OBS_PASSWORD`: Your OBS WebSocket password

### 6. Setup IP Webcam on Android
1. Install "IP Webcam" app from Google Play Store
2. Open the app and scroll down to "Start server"
3. Note the IP address shown (e.g., `192.168.1.100:8080`)

## Usage

**Important:** Make sure OBS Studio is running before starting the script!

### Option 1: Using .env file (Recommended)

Once you've configured your `.env` file, simply run:
```bash
python3 ip_webcam_virtual.py
```

### Option 2: Using command-line arguments

```bash
python3 ip_webcam_virtual.py <IP_ADDRESS>
```

### Examples

```bash
# Using .env file (simplest!)
webcam

# With command-line argument
webcam 192.168.1.100:8080

# Override .env with custom resolution
webcam --width 1280 --height 720

# Full manual configuration
webcam 192.168.1.100:8080 --obs-password your_password --width 1920 --height 1080
```

### Options
- `--width`: Output video width (default: 1920)
- `--height`: Output video height (default: 1080)
- `--obs-host`: OBS WebSocket host (default: localhost)
- `--obs-port`: OBS WebSocket port (default: 4455)
- `--obs-password`: OBS WebSocket password (if set)

## Usage in Other Apps

Once the script is running, the virtual camera will be available in:
- Zoom (select "OBS Virtual Camera")
- Google Meet
- Microsoft Teams
- Discord
- Any app that uses webcams

## Stopping

Press `Ctrl+C` to stop the virtual camera.

## Troubleshooting

### Virtual camera not appearing in Google Meet/Zoom

1. **Check if the camera extension is enabled:**
   ```bash
   system_profiler SPCameraDataType
   ```
   You should see "OBS Virtual Camera" in the list.

2. **If not listed:**
   - Go to **System Settings → General → Login Items & Extensions → Camera Extensions**
   - Make sure **OBS Virtual Camera** is enabled (toggled on)
   - Restart OBS and your browser

3. **Restart everything:**
   - Quit and restart OBS
   - Close all browser windows
   - Run the script again: `python3 ip_webcam_virtual.py`
   - Open Google Meet in a fresh browser window

### Cannot connect to OBS WebSocket

Run the test script:
```bash
python3 test_obs_connection.py
```

This will help diagnose connection issues and test your password.

### IP Webcam stream not loading

- Make sure your Android device and Mac are on the same WiFi network
- Check that the IP Webcam app shows "Server is running"
- Try accessing the stream in your browser: `http://<ANDROID_IP>/video`
