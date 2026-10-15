"""Render an animated story HTML (1080x1920, CSS animations) to MP4.

Usage: python3 tools/render_story.py <story.html> <out.mp4> [seconds=10] [music.mp3]
Steps every CSS animation frame by frame (30 fps), so the result is smooth and exact.
Optional music: trimmed to length, faded in/out.
"""
import os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

src, out = sys.argv[1], sys.argv[2]
secs = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
music = sys.argv[4] if len(sys.argv) > 4 else None
FPS = 30
tmp = tempfile.mkdtemp()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.abspath(src))
    pg.evaluate("document.getAnimations().forEach(a => a.pause())")
    for i in range(int(secs * FPS)):
        t = i * 1000 / FPS
        pg.evaluate(f"document.getAnimations().forEach(a => a.currentTime = {t})")
        pg.screenshot(path=f"{tmp}/f{i:04d}.jpg", type="jpeg", quality=92)
    b.close()

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.jpg"]
if music:
    cmd += ["-i", music, "-filter_complex",
            f"[1:a]atrim=0:{secs},afade=t=in:d=0.5,afade=t=out:st={secs-1.2}:d=1.2[a]",
            "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
else:
    # silent audio track - some platforms reject videos without audio
    cmd += ["-f", "lavfi", "-t", str(secs), "-i", "anullsrc=r=44100:cl=stereo",
            "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-shortest"]
cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
        "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("ok", out)
