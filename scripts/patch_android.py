"""Patches the freshly generated Capacitor Android project (run after `npx cap add android`)."""
import pathlib
import re
import shutil

root = pathlib.Path("android")
manifest = root / "app/src/main/AndroidManifest.xml"
s = manifest.read_text(encoding="utf-8")

# --- permissions ---
perms = [
    "INTERNET", "WAKE_LOCK", "FOREGROUND_SERVICE", "FOREGROUND_SERVICE_MEDIA_PLAYBACK",
    "POST_NOTIFICATIONS", "ACCESS_NETWORK_STATE", "ACCESS_WIFI_STATE", "RECEIVE_BOOT_COMPLETED",
]
add = "".join(
    f'    <uses-permission android:name="android.permission.{p}" />\n'
    for p in perms
    if f'android.permission.{p}"' not in s
)
s = s.replace("<application", add + "    <application", 1)

# --- cleartext HTTP (stations are often plain http / VPN addresses) ---
if "usesCleartextTraffic" not in s:
    s = s.replace("<application", '<application android:usesCleartextTraffic="true"', 1)

# --- foreground service + ML Kit scanner module + deep link ---
extra_app = ""
if "RadioService" not in s:
    extra_app += '    <service android:name=".RadioService" android:exported="false" android:foregroundServiceType="mediaPlayback" />\n'
if "com.google.mlkit.vision.DEPENDENCIES" not in s:
    extra_app += '    <meta-data android:name="com.google.mlkit.vision.DEPENDENCIES" android:value="barcode_ui" />\n'
s = s.replace("</application>", extra_app + "    </application>", 1)

if 'android:scheme="djape1"' not in s:
    intent_filter = (
        '        <intent-filter>\n'
        '            <action android:name="android.intent.action.VIEW" />\n'
        '            <category android:name="android.intent.category.DEFAULT" />\n'
        '            <category android:name="android.intent.category.BROWSABLE" />\n'
        '            <data android:scheme="djape1" />\n'
        '        </intent-filter>\n'
    )
    s = s.replace("</activity>", intent_filter + "        </activity>", 1)

manifest.write_text(s, encoding="utf-8")

# --- native sources (service, plugin, MainActivity) ---
dest = root / "app/src/main/java/gr/djape1/listener"
dest.mkdir(parents=True, exist_ok=True)
for f in pathlib.Path("native").glob("*.java"):
    shutil.copy(f, dest / f.name)

# --- ML Kit needs minSdk 23+ ---
vg = root / "variables.gradle"
if vg.exists():
    v = vg.read_text(encoding="utf-8")
    v = re.sub(r"minSdkVersion\s*=\s*(\d+)", lambda m: "minSdkVersion = " + str(max(24, int(m.group(1)))), v)
    vg.write_text(v, encoding="utf-8")

print("Android project patched")
