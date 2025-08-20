import subprocess
import re
import os
from tqdm import tqdm

def detect_black_frames(video_path, black_duration=0.5, black_threshold=0.98):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"blackdetect=d={black_duration}:pic_th={black_threshold}",
        "-an", "-f", "null", "-"
    ]

    print("[INFO] Running FFmpeg to detect black frames...")
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    output = result.stderr

    # Regex to extract black_start and black_end
    black_end_times = []
    for line in output.splitlines():
        match = re.search(r"black_start:(\d+\.\d+)\s+black_end:(\d+\.\d+)", line)
        if match:
            black_end_times.append(float(match.group(2)))

    return black_end_times

def split_video(video_path, cut_points, output_dir="black_splits"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Add start (0.0) and final video end time
    cut_points = [0.0] + cut_points

    # Get total duration of input video
    duration_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    total_duration = float(subprocess.check_output(duration_cmd).strip())
    cut_points.append(total_duration)

    print(f"[INFO] Splitting video into {len(cut_points) - 1} segments...")

    for i in tqdm(range(len(cut_points) - 1)):
        start = cut_points[i]
        end = cut_points[i + 1]
        output_file = os.path.join(output_dir, f"part_{i+1:03}.mp4")

        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", str(start),
            "-to", str(end),
            "-c", "copy",
            "-avoid_negative_ts", "1",
            output_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[INFO] Done! Clips saved to: {output_dir}")

# === MAIN ===

VIDEO_FILE = "2001 TV Commercials - 2000s Commercial Compilation #3 [h3owWrPqM6c].mp4"  # <-- Replace with your actual file
black_ends = detect_black_frames(VIDEO_FILE, black_duration=0.08, black_threshold=0.95)
split_video(VIDEO_FILE, black_ends, output_dir="output_black_splits")
