"""Actual adb lifecycle scenarios; preserve unmodified Logcat and assert callback order."""
import json
import os
import queue
import re
import subprocess
import threading
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT / ".security-reports"
(ROOT / "evidence").mkdir(parents=True, exist_ok=True)
ADB = str(Path(os.environ.get("ANDROID_HOME", Path.home() / "Library/Android/sdk")) / "platform-tools/adb")
PACKAGE = "com.example.activitylifecycle"

def adb(*args):
    return subprocess.check_output([ADB, *args], text=True).strip()

def shell(*args):
    return adb("shell", *args)

adb("install", "-r", str(PROJECT / "app/build/outputs/apk/debug/app-debug.apk"))
shell("am", "force-stop", PACKAGE)
original = {key: shell("settings", "get", "system", key) for key in ["accelerometer_rotation", "user_rotation"]}
shell("settings", "put", "system", "accelerometer_rotation", "0")
shell("settings", "put", "system", "user_rotation", "0")
logcat = subprocess.Popen([ADB, "logcat", "-v", "threadtime", "-T", "1", "ActivityLifecycle:D", "*:S"], stdout=subprocess.PIPE, text=True)
events = queue.Queue()
threading.Thread(target=lambda: [events.put(line) for line in logcat.stdout], daemon=True).start()
raw_lines = []
results = []
pid = None

def expect(scenario, expected):
    actual = []
    deadline = time.monotonic() + 25
    while len(actual) < len(expected):
        line = events.get(timeout=max(0.1, deadline - time.monotonic()))
        match = re.search(r"ActivityLifecycle:\s+(on\w+) instance=", line)
        if match and line.split()[2] == pid:
            raw_lines.append(line)
            actual.append(match.group(1))
    assert actual == expected, (scenario, actual, expected)
    results.append({"scenario": scenario, "callbacks": actual, "passed": True})
    (ROOT / "evidence" / f"lifecycle-{scenario}.log").write_text("".join(raw_lines[-len(expected):]))

def screenshot(name):
    previous = None
    stable = 0
    deadline = time.monotonic() + 15
    while stable < 3:
        assert time.monotonic() < deadline, "Screen did not settle"
        data = subprocess.check_output([ADB, "exec-out", "screencap", "-p"])
        stable = stable + 1 if data == previous else 0
        previous = data
    (ROOT / "evidence" / f"lab6-lifecycle-{name}.png").write_bytes(data)

try:
    shell("am", "start", "-W", "-n", f"{PACKAGE}/.MainActivity")
    pid = shell("pidof", PACKAGE)
    expect("launch", ["onCreate", "onStart", "onResume"])
    screenshot("portrait")
    shell("input", "keyevent", "KEYCODE_HOME")
    expect("home", ["onPause", "onStop"])
    shell("am", "start", "-W", "-n", f"{PACKAGE}/.MainActivity")
    expect("return", ["onRestart", "onStart", "onResume"])
    shell("settings", "put", "system", "user_rotation", "1")
    expect("rotation", ["onPause", "onStop", "onDestroy", "onCreate", "onStart", "onResume"])
    screenshot("landscape")
    (ROOT / "evidence/lifecycle-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(json.dumps(results, ensure_ascii=False, indent=2))
finally:
    (ROOT / "evidence/lifecycle-logcat.log").write_text("".join(raw_lines))
    logcat.terminate()
    logcat.wait(timeout=5)
    shell("am", "force-stop", PACKAGE)
    for key, value in original.items():
        if value == "null":
            shell("settings", "delete", "system", key)
        else:
            shell("settings", "put", "system", key, value)
