[app]

# =========================================================
# APP
# =========================================================

title = Pop Surprise

package.name = popsurprise
package.domain = com.popsurprise

# Source folder
source.dir = .

# Files included in APK
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,mp3

# App version
version = 0.1.0


# =========================================================
# PYTHON DEPENDENCIES
# =========================================================

requirements = python3,kivy==2.3.1


# =========================================================
# DISPLAY
# =========================================================

orientation = portrait

fullscreen = 1


# =========================================================
# ANDROID
# =========================================================

# Target Android API
android.api = 35

# Minimum Android API
android.minapi = 24

# 64-bit Android
android.archs = arm64-v8a

# Accept SDK licenses
android.accept_sdk_license = True


# =========================================================
# BUILDOZER
# =========================================================

[buildozer]

log_level = 2

warn_on_root = 1
