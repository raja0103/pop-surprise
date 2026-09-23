[app]

# App
title = Pop Surprise
package.name = popsurprise
package.domain = com.popsurprise

# Source
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,mp3

# Version
version = 0.1.0

# Python dependencies
requirements = python3,kivy

# App orientation
orientation = portrait

# Full screen mobile game
fullscreen = 1


# =========================================================
# ANDROID
# =========================================================

# Android API
android.api = 35

# Minimum Android version
android.minapi = 24

# Build architecture
android.archs = arm64-v8a

# Accept Android SDK license
android.accept_sdk_license = True


# =========================================================
# BUILD
# =========================================================

[buildozer]

log_level = 2

warn_on_root = 1