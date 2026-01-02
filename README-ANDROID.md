# LevelUp Server - Android APK

Your Python server is now set up to build as an Android APK!

## 📱 What's been created:

1. **main.py** - Kivy app with Start/Stop buttons and live logs
2. **buildozer.spec** - Configuration for building APK
3. **requirements-android.txt** - All dependencies for Android

## 🚀 How to build APK:

### On Linux (or WSL on Windows):

1. **Install Buildozer:**
   ```bash
   pip install buildozer cython
   ```

2. **Install Android dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

3. **Build the APK:**
   ```bash
   buildozer android debug
   ```

4. **Find your APK:**
   - Location: `bin/levelupserver-0.1-arm64-v8a-debug.apk`
   - Transfer to phone and install!

### On macOS (requires Linux VM or Docker):

Use Docker:
```bash
docker run --rm -v "$PWD":/app -w /app kivy/buildozer android debug
```

## 📲 Using the app:

1. Install APK on Android
2. Open "LevelUp Server" app
3. Tap **START SERVER** to run
4. View logs in real-time
5. Tap **STOP SERVER** to stop

## ⚠️ Important Notes:

- Server only runs while app is open
- Phone must stay awake for server to work
- Server uses phone's network connection
- APK size will be ~40-50 MB
- Requires Android 5.0+ (API 21)

## 🔧 Next steps:

You might want to integrate your actual server startup code in `main.py` at the `run_server()` method. Currently it's a placeholder - you'll need to call your actual server logic there.

Want me to integrate your actual server code into the Kivy app?
