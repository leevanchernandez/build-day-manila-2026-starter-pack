import subprocess
from core.practice import _detect_ffmpeg

def listDirectShowDevices():
    ffmpeg_exe = _detect_ffmpeg()
    process_result = subprocess.run(
        [ffmpeg_exe, "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
        capture_output=True,
        text=True
    )
    print(process_result.stderr)

if __name__ == "__main__":
    listDirectShowDevices()