import subprocess
import time
import base64
import ctypes
from ctypes import wintypes
import time
import os
import random
from mss import mss
from PIL import Image
import random
import json
import urllib.parse
import urllib.request

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.SetProcessDPIAware()

# ---------------- CONSTANTS ----------------
SW_RESTORE = 9
SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0
SW_MAXIMIZE = 3


# ---------------- STRUCTS ----------------
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


# ---------------- FIND WINDOW ----------------
def find_powershell_window():
    result = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def enum_proc(hwnd, lparam):
        title = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(hwnd, title, 512)
        if "PowerShell" in title.value:
            result.append(hwnd)
        return True

    user32.EnumWindows(enum_proc, 0)
    return result[-1] if result else None


# ---------------- MOVE AND RESIZE WINDOW ----------------
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040


def move_and_resize_window(hwnd, x, y, width, height):
    user32.SetWindowPos(
        hwnd, None, x, y, width, height, SWP_NOZORDER | SWP_NOACTIVATE | SWP_SHOWWINDOW
    )


# ---------------- CAPTURE WINDOW ----------------
def capture_window(hwnd, output_file):
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))

    monitor = {
        "left": rect.left,
        "top": rect.top,
        "width": rect.right - rect.left,
        "height": rect.bottom - rect.top,
    }

    # Let DWM settle (prevents partial frames)
    time.sleep(0.3)

    with mss() as sct:
        img = sct.grab(monitor)
        Image.frombytes("RGB", img.size, img.rgb).save(output_file)


def random_public_place_name_photon(max_retries=5):
    photon_url = "https://photon.komoot.io/api/"

    queries = [
        "park",
        "library",
        "hospital",
        "museum",
        "stadium",
        "shopping mall",
        "market",
        "bus station",
        "railway station",
        "university",
        "public garden",
    ]

    for attempt in range(max_retries):
        query = random.choice(queries)

        params = {
            "q": query,
            "limit": 10,
            "lang": "en",
        }

        url = photon_url + "?" + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            features = data.get("features", [])
            if not features:
                raise ValueError("No results")

            feature = random.choice(features)
            name = feature.get("properties", {}).get("name")

            if name:
                return name
            else:
                raise ValueError("Unnamed place")

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            json.JSONDecodeError,
            ValueError,
        ):

            time.sleep(1 + attempt)

    return None


location = random_public_place_name_photon()
print("Generated location:", location)
with open(os.path.join("course4/geodata/where.data"), "a", encoding="utf-8") as f:
    f.write(location + "\n")
SCRIPT_PATHS = ["course4\\geodata\\geoload.py", "course4\\geodata\\geodump.py"]
LOGFILE = "output.txt"
for SCRIPT_PATH in SCRIPT_PATHS:
    OUTPUT_FILE = f"screenshots\\{os.path.basename(SCRIPT_PATH).replace('.py', '')}.png"
    WORKDIR = os.path.dirname(SCRIPT_PATH)
    SCRIPT = os.path.abspath(SCRIPT_PATH)
    SCREENSHOT = os.path.abspath(OUTPUT_FILE)
    ps_worker = rf"""
    Set-Location "{WORKDIR}"

    $log = "{LOGFILE}"
    $restartMarker = "Retrieved 100 locations, restart to retrieve more"

    do {{
        $shouldRestart = $false
        Remove-Item $log -ErrorAction Ignore

        Write-Host "`n===== RUN START =====" -ForegroundColor Cyan

        python -u {SCRIPT} 2>&1 |
        Tee-Object -FilePath $log |
        ForEach-Object {{
            # RAW live output (no regex, no colors)
            Write-Host $_

            # Restart detection only
            if ($_ -like "*$restartMarker*") {{
                $shouldRestart = $true
            }}
        }}

        if ($shouldRestart) {{
            Write-Host "`n>>> Restart condition detected. Running again..." -ForegroundColor Yellow
        }} else {{
            Write-Host "`n>>> No restart condition. Worker exiting." -ForegroundColor Green
        }}
    }} while ($shouldRestart)

    Start-Sleep -Milliseconds 300
    """

    encoded_worker = base64.b64encode(ps_worker.encode("utf-16le")).decode()

    print("Launching worker PowerShell...")
    proc = subprocess.Popen(
        ["powershell.exe", "-EncodedCommand", encoded_worker],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )

    # ✅ WAIT PROPERLY
    proc.wait()
    print("Worker finished")

    # ---------------- VIEWER POWERSHELL ----------------
    ps_viewer = rf"""
    Set-Location "{WORKDIR}"

    $highlightRegex = '\d+\.\d+|Retrieving|Found'
    $lines = Get-Content "{LOGFILE}"

    # Find index of LAST matching line
    $lastMatchIndex = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {{
        if ($lines[$i] -match $highlightRegex) {{
            $lastMatchIndex = $i
        }}
    }}

    Write-Host "===== OUTPUT (LAST MATCH HIGHLIGHTED) =====" -ForegroundColor Cyan

    # Replay output
    for ($i = 0; $i -lt $lines.Count; $i++) {{
        if ($i -eq $lastMatchIndex) {{
            # Selected-like highlight
            Write-Host $lines[$i] -BackgroundColor White -ForegroundColor Black
        }} else {{
            Write-Host $lines[$i]
        }}
    }}
    """

    encoded_viewer = base64.b64encode(ps_viewer.encode("utf-16le")).decode()

    print("Launching viewer PowerShell...")
    subprocess.Popen(
        ["powershell.exe", "-NoExit", "-EncodedCommand", encoded_viewer],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )

    time.sleep(5)

    hwnd = find_powershell_window()
    SAFE_X = 100
    SAFE_Y = 100
    SAFE_W = 1280
    SAFE_H = 720

    move_and_resize_window(hwnd, SAFE_X, SAFE_Y, SAFE_W, SAFE_H)

    if hwnd:
        capture_window(hwnd, SCREENSHOT)
        # close the powershell window
        user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
    else:
        print("PowerShell window not found, cannot capture screenshot.")

    print("Screenshot saved:", SCREENSHOT)
