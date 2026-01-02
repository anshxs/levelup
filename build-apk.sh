#!/bin/bash
# Build APK using Docker on macOS

echo "Building Android APK using Docker..."
echo "This may take 30-60 minutes on first run (downloads dependencies)"
echo ""

docker run --rm -v "$PWD":/home/user/hostcwd \
  kivy/buildozer \
  --verbose android debug

echo ""
if [ -d "bin" ]; then
  echo "✓ Build complete! APK is in: bin/"
  ls -lh bin/*.apk 2>/dev/null || echo "APK file:"
  find bin -name "*.apk" -exec ls -lh {} \;
else
  echo "❌ Build failed - no bin/ folder created"
  echo "Check the output above for errors"
fi
