import subprocess
import os

out_dir = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\debug_frames"
os.makedirs(out_dir, exist_ok=True)
timestamps = ["00:00:05", "00:00:20", "00:00:35", "00:00:50", "00:00:58", "00:01:08"]
video_path = r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\ep2_preview_1min.mp4"

for ts in timestamps:
    safe_ts = ts.replace(":", "_")
    out = os.path.join(out_dir, f"frame_{safe_ts}.png")
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", video_path, "-vframes", "1", out]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(out):
        print(f"Extracted {ts} -> {out} ({os.path.getsize(out)} bytes)")
    else:
        print(f"Failed {ts}")
