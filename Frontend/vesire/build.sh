#!/bin/bash
# Flutter installation script for Netlify

# Install Flutter
if [ ! -d "$HOME/flutter" ]; then
  echo "Installing Flutter..."
  cd $HOME
  git clone https://github.com/flutter/flutter.git -b stable --depth 1
  export PATH="$HOME/flutter/bin:$PATH"
fi

# Add Flutter to PATH
export PATH="$HOME/flutter/bin:$PATH"

# Enable web support
flutter config --enable-web

# Get dependencies
flutter pub get

# Build web app
flutter build web --release --web-renderer canvaskit
