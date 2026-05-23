#!/usr/bin/env python3
"""
YouTube Video Production Pipeline
Fully automated: new tool page → script → voiceover+subs → render → upload → captions
"""
import sys, os, json, subprocess, time, re, glob
from pathlib import Path

# ─── CONFIG ──────────────────────────────────────────────────────────────────
SITE = "listingsai.directory"
TRACKER = "/home/hermes/brain-storm-corp/youtube/PRODUCTION_TRACKER.json"
TOOLS_DIR = f"/home/hermes/{SITE}/tools"
SCRIPTS_DIR = "/home/hermes/brain-storm-corp/youtube/scripts"
RENDER_DIR = "/home/hermes/brain-storm-corp/youtube"
YOUTUBE_UPLOAD_SCRIPT = "/home/hermes/brain-storm-corp/youtube/scripts/youtube-upload.py"
AUTH_FILE = os.path.expanduser("~/.hermes/auth.json")
EDGE_VOICE = "en-US-AndrewMultilingualNeural"
FPS = 30
# ─── ─────────────────────────────────────────────────────────────────────────

def log(msg):
    print(f"[yt-video] {msg}", flush=True)

def load_tracker():
    with open(TRACKER) as f:
        return json.load(f)

def save_tracker(t):
    with open(TRACKER, 'w') as f:
        json.dump(t, f, indent=2)

def get_auth():
    with open(AUTH_FILE) as f:
        return json.load(f)

def run(cmd, timeout=300, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    if r.returncode != 0:
        log(f"ERROR running: {cmd[:80]}\n  stderr: {r.stderr[-500:]}")
    return r

def get_active_tools():
    """Return list of tool .html files (not archived, not article)"""
    tools = []
    for f in os.listdir(TOOLS_DIR):
        if f.endswith('.html') and '-article' not in f and f != 'index.html':
            path = os.path.join(TOOLS_DIR, f)
            tools.append({'file': f, 'path': path, 'mtime': os.path.getmtime(path)})
    return sorted(tools, key=lambda x: -x['mtime'])

def get_rendered_tools():
    """Return tools that already have videos rendered"""
    t = load_tracker()
    return {v['tool'] for v in t['videos'] if v.get('render_status') == 'done'}

def tool_to_video_id(tool_file):
    """Convert 'mortgage-payment-estimator.html' → 'mortgage-payment-estimator'"""
    return tool_file.replace('.html', '')

def next_video_number(tracker):
    nums = []
    for v in tracker['videos']:
        m = re.search(r'video-(\d+)', v['id'])
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1

def read_script(script_path):
    with open(script_path) as f:
        return f.read()

def parse_script_for_voiceover(script_text):
    """Extract all text between \"\" in script — these are the spoken parts"""
    parts = re.findall(r'"([^"]+)"', script_text)
    return [p.strip() for p in parts if len(p.strip()) > 10]

def generate_voiceover_with_subs(text_parts, output_prefix, speed=1.0):
    """
    Generate combined voiceover MP3 + VTT subtitles from text parts.
    Returns path to final MP3 and subtitle file.
    """
    part_files = []
    sub_entries = []
    current_time = 0.0

    # Generate each part + subtitle
    for i, text in enumerate(text_parts):
        mp3 = f"{output_prefix}_part{i+1}.mp3"
        ttml = f"{output_prefix}_part{i+1}.ttml"
        run(f'edge-tts -t "{text}" -v {EDGE_VOICE} --write-media {mp3} --write-subtitles {ttml}')
        part_files.append(mp3)

        # Parse TTML to get duration
        if os.path.exists(ttml):
            with open(ttml) as f:
                content = f.read()
            # Parse TTML timing lines like: 00:00:00,050 --> 00:00:03,225
            matches = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', content)
            if matches:
                start_t = parse_ttml_time(matches[0][0])
                end_t = parse_ttml_time(matches[0][1])
                dur = end_t - start_t
                sub_entries.append((current_time, current_time + dur, text[:80]))
                current_time += dur

        time.sleep(0.1)

    # Combine MP3s
    combined_mp3 = f"{output_prefix}_raw.mp3"
    concat_txt = f"{output_prefix}_concat.txt"
    with open(concat_txt, 'w') as f:
        for pf in part_files:
            f.write(f"file '{pf}'\n")
    run(f'ffmpeg -y -f concat -safe 0 -i {concat_txt} -c copy {combined_mp3} 2>/dev/null')

    # Apply speedup
    final_mp3 = f"{output_prefix}_final.mp3"
    speed_filter = f'atempo={speed}'
    run(f'ffmpeg -y -i {combined_mp3} -filter:a "{speed_filter},afade=t=in:st=0:d=1,afade=t=out:st={current_time/speed-2}:d=2" {final_mp3} 2>/dev/null')

    # Generate VTT subtitle
    vtt = f"{output_prefix}.vtt"
    write_vtt(sub_entries, speed, vtt)

    return final_mp3, vtt

def parse_ttml_time(t):
    """Parse TTML time '00:01:23,456' → seconds float"""
    h,m,s = t.replace(',','.').split(':')
    return int(h)*3600 + int(m)*60 + float(s)

def write_vtt(entries, speed, path):
    """Write WebVTT subtitle file"""
    with open(path, 'w') as f:
        f.write("WEBVTT\n\n")
        for i, (start, end, text) in enumerate(entries):
            f.write(f"{i+1}\n")
            f.write(f"{format_vtt_time(start/speed)} --> {format_vtt_time(end/speed)}\n")
            f.write(f"{text}\n\n")

def format_vtt_time(s):
    """Format seconds to VTT time 00:00:00.000"""
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f"{h:02}:{m:02}:{sec:02}.{ms:03}"

def generate_music(duration_s, output_path):
    """Generate ambient background music using ffmpeg lavfi"""
    cmd = (
        f'ffmpeg -y -f lavfi -i "anoisesrc=d=90:c=pink:r=44100:a=0.2" '
        f'-f lavfi -i "sine=f=110:sine=0.3" '
        f'-f lavfi -i "sine=f=220:sine=0.15" '
        f'-filter_complex "[0:a][1:a][2:a]amix=inputs=3:duration=first:dropout_transition=0,dynaudnorm,lowpass=f=800,volume=0.15,afade=t=in:st=0:d=2,afade=t=out:st={duration_s-3}:d=3" '
        f'-t {duration_s} {output_path} 2>/dev/null'
    )
    run(cmd)

def generate_frames(tool_name, tool_title, output_dir, duration_s, script_text, speed):
    """
    Generate video frames using Pillow.
    Returns list of frame PNG paths.
    """
    from PIL import Image as PILImage
    os.makedirs(output_dir, exist_ok=True)
    num_frames = int(duration_s * FPS)
    frames_per_scene = num_frames // 5  # 5 scenes

    scenes = build_scenes(tool_name, tool_title, script_text)

    frame_num = 0
    for scene_idx, scene in enumerate(scenes):
        start_frame = scene_idx * frames_per_scene
        end_frame = start_frame + frames_per_scene
        scene_duration_frames = frames_per_scene

        for f in range(scene_duration_frames):
            progress = f / scene_duration_frames  # 0 to 1 within scene
            img = render_scene_frame(scene, progress, f, scene_duration_frames)
            img.save(f"{output_dir}/frame_{frame_num+1:04d}.png")
            frame_num += 1
            if frame_num % 300 == 0:
                log(f"  frame {frame_num}/{num_frames}")

    return num_frames

def build_scenes(tool_name, tool_title, script_text):
    """Define 5 scenes for a tool video"""
    scenes = []
    # Scene 1: Problem/Hook
    scenes.append({'type': 'problem', 'duration': 15, 'title': tool_title})
    # Scene 2: Tool intro
    scenes.append({'type': 'tool_intro', 'duration': 10, 'title': tool_title, 'tool': tool_name})
    # Scene 3: Demo/How it works
    scenes.append({'type': 'demo', 'duration': 25, 'title': tool_title, 'tool': tool_name})
    # Scene 4: Features
    scenes.append({'type': 'features', 'duration': 20, 'title': tool_title, 'tool': tool_name})
    # Scene 5: CTA
    scenes.append({'type': 'cta', 'duration': 20, 'title': tool_title})
    return scenes

def render_scene_frame(scene, progress, frame_num, scene_frames):
    """Render a single frame using Pillow"""
    W, H = 1920, 1080
    # Background color scheme
    BG = (13, 17, 23)
    ACCENT = (0, 200, 150)  # teal
    TEXT = (255, 255, 255)
    SUBTEXT = (180, 190, 200)

    img = PILImage.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # Try to use a system font
    font_paths = ['/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
                  '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                  '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    font_main = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_main = ImageFont.truetype(fp, 60)
            font_small = ImageFont.truetype(fp, 32)
            font_large = ImageFont.truetype(fp, 90)
            break

    if font_main is None:
        font_main = font_small = font_large = ImageFont.load_default()

    stype = scene['type']

    if stype == 'problem':
        # Gradient-like bg + problem text
        # Draw accent bar at top
        d.rectangle([0, 0, W, 6], fill=ACCENT)
        # Big question/problem text
        msg = "Every Agent's Hidden Problem"
        cx, cy = W//2, H//2 - 50
        d.text((cx, cy), msg, fill=TEXT, font=font_large, anchor='mm')
        d.text((cx, cy+100), "The tool that finally fixes it →", fill=SUBTEXT, font=font_main, anchor='mm')

    elif stype == 'tool_intro':
        d.rectangle([0, 0, W, 6], fill=ACCENT)
        d.text((W//2, H//2-80), scene['title'], fill=TEXT, font=font_large, anchor='mm')
        d.text((W//2, H//2+20), f"listingsai.directory/tools/{scene['tool']}", fill=ACCENT, font=font_main, anchor='mm')
        d.text((W//2, H//2+100), "Free • No signup required", fill=SUBTEXT, font=font_main, anchor='mm')

    elif stype == 'demo':
        # Show tool in action - simulate a UI
        d.rectangle([0, 0, W, 6], fill=ACCENT)
        # Simulate tool interface boxes
        box_x, box_y = W//2 - 400, H//2 - 200
        d.rectangle([box_x, box_y, box_x+800, box_y+400], outline=ACCENT, width=3)
        # Simulate input field
        d.rectangle([box_x+50, box_y+50, box_x+750, box_y+120], outline=TEXT, width=2)
        d.text((box_x+60, box_y+70), "Enter property address...", fill=SUBTEXT, font=font_small)
        # Buttons
        d.rectangle([box_x+50, box_y+150, box_x+250, box_y+200], fill=ACCENT)
        d.text((box_x+150, box_y+165), "GENERATE", fill=BG, font=font_small, anchor='mm')
        d.rectangle([box_x+270, box_y+150, box_x+420, box_y+200], outline=TEXT, width=1)
        d.text((box_x+345, box_y+165), "CLEAR", fill=SUBTEXT, font=font_small, anchor='mm')
        # Progress bar animation
        bar_y = box_y + 250
        d.rectangle([box_x+50, bar_y, box_x+750, bar_y+20], outline=SUBTEXT, width=1)
        filled = int(700 * progress)
        if filled > 0:
            d.rectangle([box_x+51, bar_y+1, box_x+51+filled, bar_y+19], fill=ACCENT)
        d.text((W//2, box_y+320), f"Generating... {int(progress*100)}%", fill=SUBTEXT, font=font_small, anchor='mm')

    elif stype == 'features':
        d.rectangle([0, 0, W, 6], fill=ACCENT)
        d.text((W//2, 120), "What You Get", fill=TEXT, font=font_large, anchor='mm')
        features = ["Instant Results • Professional Quality • 100% Free",
                    "No Signup • No Credit Card • Works on Mobile"]
        y = H//2 - 80
        for feat in features:
            d.text((W//2, y), feat, fill=TEXT, font=font_main, anchor='mm')
            y += 80

    elif stype == 'cta':
        # Ken Burns: zoom in slowly
        zoom = 1.0 + 0.04 * progress  # 4% zoom in over scene
        # Apply zoom transform (center crop)
        cx, cy = W//2, H//2
        new_w = int(W / zoom)
        new_h = int(H / zoom)
        crop_x = (W - new_w) // 2
        crop_y = (H - new_h) // 2
        img = img.crop((crop_x, crop_y, crop_x+new_w, crop_y+new_h))
        img = img.resize((W, H), Image.LANCZOS)
        d = ImageDraw.Draw(img)

        d.rectangle([0, 0, W, 8], fill=ACCENT)
        d.text((W//2, H//2-80), "Stop Guessing. Start Using It.", fill=TEXT, font=font_large, anchor='mm')
        d.text((W//2, H//2+20), "listingsai.directory", fill=ACCENT, font=font_main, anchor='mm')
        d.text((W//2, H//2+100), "Link in description ↓", fill=SUBTEXT, font=font_small, anchor='mm')

    return img

def render_video(frames_dir, audio_file, sub_file, output_mp4, duration_s):
    """Encode frames + audio → final MP4 with hardcoded subtitles"""
    log(f"Encoding video: {output_mp4}")
    # Encode video from frames
    video_only = output_mp4.replace('.mp4', '_novid.mp4')
    cmd = (
        f'ffmpeg -y -framerate {FPS} -i {frames_dir}/frame_%04d.png '
        f'-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p '
        f'-r {FPS} {video_only} 2>&1 | tail -5'
    )
    r = run(cmd)
    if r.returncode != 0:
        log(f"Video encode warn: {r.stderr[-200:]}")

    # Mix audio + music
    audio_mixed = output_mp4.replace('.mp4', '_audiomix.mp3')
    # voice at 100%, music at 15%
    run(f'ffmpeg -y -i {audio_file} -i /tmp/ambient_bg.mp3 -filter_complex "[0:a]volume=1.0[vo];[1:a]volume=0.15[mu];[vo][mu]amix=inputs=2:duration=first" {audio_mixed} 2>/dev/null')

    # Combine video + audio
    run(f'ffmpeg -y -i {video_only} -i {audio_mixed} -c:v copy -c:a aac -b:a 128k -shortest {output_mp4} 2>/dev/null')

    # Attach subtitles as closed captions (burned in) - optional step
    # For now, subtitle file is passed separately for YouTube upload
    return output_mp4

def upload_to_youtube(video_path, title, description, tags, privacy='public'):
    """Upload to YouTube via upload script"""
    log(f"Uploading: {title[:50]}")
    cmd = (
        f'python3 {YOUTUBE_UPLOAD_SCRIPT} '
        f'--file "{video_path}" '
        f'--title "{title}" '
        f'--description "{description}" '
        f'--tags "{",".join(tags)}" '
        f'--privacy "{privacy}"'
    )
    r = run(cmd, timeout=180)
    if r.returncode == 0:
        # Extract video ID from output
        match = re.search(r'(?:video_id|https://youtu\.be/)([a-zA-Z0-9_-]+)', r.stdout)
        if match:
            return match.group(1)
    log(f"Upload failed: {r.stderr[-300:]}")
    return None

def add_captions_to_youtube(video_id, sub_file, lang='en'):
    """Add captions to YouTube video via API"""
    try:
        auth = get_auth()
        access_token = auth['providers']['youtube']['access_token']
    except:
        log("No YouTube auth token found, skipping captions")
        return False

    import requests
    # Upload caption file
    with open(sub_file, 'rb') as f:
        sub_data = f.read()

    # Determine snippet name from VTT
    name = sub_file.split('/')[-1].replace('.vtt', '')

    url = f"https://www.googleapis.com/upload/youtube/v3/captions"
    boundary = "boundary1234567890"
    body = (
        f"--{boundary}\r\n"
        f'Content-Type: application/json\r\n\r\n'
        f'{{"snippet":{"videoId":"{video_id}","language":"{lang}","name":"{name}"}}}\r\n'
        f"--{boundary}\r\n"
        f'Content-Type: text/vtt\r\n\r\n'
    ).encode() + sub_data + f"\r\n--{boundary}--\r\n".encode()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': f'multipart/related; boundary={boundary}',
    }

    try:
        resp = requests.post(url, headers=headers, data=body)
        if resp.status_code in (200, 201):
            log(f"Caption added to {video_id}: {resp.json()}")
            return True
        elif resp.status_code == 401:
            log("Token expired, need refresh")
            return False
        else:
            log(f"Caption upload failed: {resp.status_code} {resp.text[:200]}")
            return False
    except Exception as e:
        log(f"Caption upload error: {e}")
        return False

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: youtube-video-maker.py <tool-name> [--with-subs]")
        print("  tool-name: e.g. mortgage-payment-estimator")
        print("  --with-subs: include subtitles")
        sys.exit(1)

    tool_name = sys.argv[1]
    with_subs = '--with-subs' in sys.argv

    log(f"Starting video production for: {tool_name}")
    log(f"  Subtitle mode: {with_subs}")

    # Load tracker
    tracker = load_tracker()
    n = next_video_number(tracker)
    video_id = f"video-{n:02d}"

    # Find tool HTML
    tool_file = f"{tool_name}.html"
    tool_path = os.path.join(TOOLS_DIR, tool_file)
    if not os.path.exists(tool_path):
        log(f"Tool file not found: {tool_path}")
        sys.exit(1)

    tool_url = f"https://{SITE}/tools/{tool_name}.html"

    # Read or generate script
    script_file = None
    for sf in os.listdir(SCRIPTS_DIR):
        if tool_name.replace('-', '-') in sf:
            script_file = os.path.join(SCRIPTS_DIR, sf)
            break

    if not script_file:
        log(f"No script found for {tool_name}, generating auto-script...")
        # Run auto script generator
        r = subprocess.run(
            ['python3', '/home/hermes/brain-storm-corp/youtube/scripts/auto_script_generator.py', tool_name],
            capture_output=True, text=True
        )
        auto_file = f"/home/hermes/brain-storm-corp/youtube/scripts/video-AUTO-{tool_name}.md"
        if r.returncode == 0 and os.path.exists(auto_file):
            script_file = auto_file
            log(f"Auto-generated script: {script_file}")
        if not script_file:
            log("Could not generate script, exiting")
            sys.exit(1)

    with open(script_file) as f:
        script_text = f.read()

    # Parse voiceover parts
    text_parts = parse_script_for_voiceover(script_text)
    if not text_parts:
        log("No voiceover text found in script!")
        sys.exit(1)

    log(f"Voiceover: {len(text_parts)} parts, ~{sum(len(p) for p in text_parts)/150}s spoken")

    # Setup directories
    video_dir = os.path.join(RENDER_DIR, video_id, "renders")
    frames_dir = f"/tmp/{tool_name}-frames"
    os.makedirs(video_dir, exist_ok=True)

    # Generate ambient music
    generate_music(90, "/tmp/ambient_bg.mp3")

    # Generate voiceover + subtitles
    mp3_final, vtt_file = generate_voiceover_with_subs(text_parts, f"/tmp/{tool_name}_vo", speed=1.4)

    # Get audio duration
    r = run(f'ffprobe -v quiet -show_entries format=duration -of csv=p=0 {mp3_final}')
    duration_s = float(r.stdout.strip()) if r.returncode == 0 else 90

    # Generate frames
    log(f"Generating {int(duration_s*FPS)} frames...")
    num_frames = generate_frames(tool_name, tool_name.replace('-', ' ').title(), frames_dir, duration_s, script_text, 1.4)

    # Render video
    output_mp4 = os.path.join(video_dir, f"{tool_name}.mp4")
    render_video(frames_dir, mp3_final, vtt_file, output_mp4, duration_s)

    # Upload
    title = f"{tool_name.replace('-', ' ').title()} — Free AI Tool for Real Estate"
    description = f"Check the description box below for the free tool!\n\nFree Tool: {tool_url}\n\n#realestate #aitools"
    tags = ['real estate', 'ai tools', 'real estate agent', tool_name]

    video_id_yt = upload_to_youtube(output_mp4, title, description, tags, 'public')

    # Add captions if available
    if with_subs and os.path.exists(vtt_file) and video_id_yt:
        add_captions_to_youtube(video_id_yt, vtt_file)

    # Update tracker
    tracker['videos'].append({
        'id': video_id,
        'title': tool_name,
        'tool': tool_name,
        'tool_url': tool_url,
        'script': os.path.basename(script_file) if script_file else 'auto-generated',
        'script_status': 'done',
        'render_status': 'done',
        'upload_status': 'done' if video_id_yt else 'failed',
        'youtube_id': video_id_yt,
        'youtube_url': f"https://www.youtube.com/watch?v={video_id_yt}" if video_id_yt else None,
        'privacy': 'public',
        'duration_s': int(duration_s),
        'has_subtitles': with_subs,
        'has_ken_burns': True,
        'has_music': True,
        'rendered_at': time.strftime('%Y-%m-%d'),
    })
    save_tracker(tracker)

    log(f"Done! YouTube: https://www.youtube.com/watch?v={video_id_yt}" if video_id_yt else "Done but upload failed")

if __name__ == '__main__':
    main()
