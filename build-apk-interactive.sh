#!/bin/bash
# Build APK using Docker on macOS (Interactive Mode)

echo "Building Android APK using Docker..."
echo "This may take 30-60 minutes on first run (downloads dependencies)"
echo "You will be asked to confirm running as root - type 'y' and press Enter"
echo ""

docker run -it --rm --network host -v "$PWD":/home/user/hostcwd \
  kivy/buildozer \
  android debug

echo ""
if [ -d "bin" ]; then
  echo "✓ Build complete! APK is in: bin/"
  ls -lh bin/*.apk 2>/dev/null
else
  echo "❌ Build failed - no bin/ folder created"
fi
