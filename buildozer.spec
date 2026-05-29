[app]
title = JARVIS CORE
package.name = jarvis_core_apk
package.domain = org.stark.jarviscore
source.dir = .
source.include_exts = py,png,jpg,kv,json,html,css
version = 1.0

# Sabse zaroori: Pehle sirf basic requirements rakho
requirements = python3,kivy

# Permissions
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Build settings
android.accept_sdk_licenses = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
