[app]

# =========================================================
# APP
# =========================================================

title = Pop Surprise

package.name = popsurprise
package.domain = com.popsurprise

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,mp3

version = 0.1.0


# =========================================================
# PYTHON / KIVY
#
# IMPORTANT:
# Pin BOTH Android Python and host Python.
# Otherwise p4a currently resolves python3 to Python 3.14.
# =========================================================

requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.1


# =========================================================
# DISPLAY
# =========================================================

orientation = portrait

fullscreen = 1


# =========================================================
# ANDROID
# =========================================================

android.api = 35

android.minapi = 24

android.archs = arm64-v8a

android.accept_sdk_license = True


# =========================================================
# BUILDOZER
# =========================================================

[buildozer]

log_level = 2

warn_on_root = 1
