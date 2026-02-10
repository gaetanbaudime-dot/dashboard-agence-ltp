"""
TikFusion - Apple-inspired design + Smart Features
Auto-Download URL | Score de Viralité | Analyse Captions
"""
import streamlit as st
import os
import sys
import json
import random
import subprocess
import shutil
import tempfile
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

st.set_page_config(page_title="TikFusion x LTP", page_icon="assets/favicon.svg", layout="wide", initial_sidebar_state="collapsed")

# ============ APPLE-INSPIRED CSS ============
st.markdown("""
<style>
    /* Hide default sidebar */
    [data-testid="stSidebar"] { display: none; }

    /* SF Pro inspired typography */
    * { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif; }

    /* Header bar */
    .header-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        padding: 12px 0 8px 0;
        border-bottom: 1px solid #2C2C2E;
        margin-bottom: 16px;
    }
    .header-logo {
        background: #F5F5F7;
        color: #000;
        font-weight: 800;
        font-size: 1.3rem;
        padding: 6px 14px;
        border-radius: 8px;
        letter-spacing: 2px;
    }
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        color: #F5F5F7;
        letter-spacing: -0.5px;
    }

    /* Apple card style */
    .apple-card {
        background: #1C1C1E;
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        border: 1px solid #2C2C2E;
    }

    /* Tags */
    .tag-sm {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 5px;
        font-size: 0.65rem;
        font-weight: 500;
        margin: 1px 1px;
    }
    .tag-mirror { background: #FF453A; color: white; }
    .tag-speed { background: #2C2C2E; color: #64D2FF; border: 1px solid #3A3A3C; }
    .tag-hue { background: #2C2C2E; color: #FF9F0A; border: 1px solid #3A3A3C; }
    .tag-crop { background: #2C2C2E; color: #30D158; border: 1px solid #3A3A3C; }
    .tag-zoom { background: #2C2C2E; color: #FFD60A; border: 1px solid #3A3A3C; }
    .tag-noise { background: #2C2C2E; color: #FF6482; border: 1px solid #3A3A3C; }
    .tag-pitch { background: #2C2C2E; color: #5E5CE6; border: 1px solid #3A3A3C; }
    .tag-meta { background: #2C2C2E; color: #BF5AF2; border: 1px solid #3A3A3C; }

    /* Uniqueness badges */
    .badge-safe {
        background: #30D158;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-warning {
        background: #FF9F0A;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-danger {
        background: #FF453A;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Legend */
    .legend {
        background: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 10px;
        padding: 6px 14px;
        font-size: 0.75rem;
        color: #86868B;
        margin-bottom: 12px;
    }

    /* Folder badge */
    .folder-badge {
        background: #1C1C1E;
        color: #64D2FF;
        padding: 6px 14px;
        border-radius: 10px;
        font-family: 'SF Mono', 'Menlo', monospace;
        font-size: 0.8rem;
        border: 1px solid #2C2C2E;
        display: inline-block;
        margin-bottom: 8px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 12px;
        padding: 10px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: #1C1C1E;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        color: #86868B !important;
    }
    .stTabs [aria-selected="true"] {
        background: #007AFF !important;
        color: #FFFFFF !important;
    }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
    }

    /* Button styling */
    .stButton > button[kind="primary"] {
        background: #007AFF;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 24px;
    }
    .stButton > button[kind="primary"]:hover {
        background: #0056CC;
    }

    /* Download button */
    .stDownloadButton > button {
        background: #2C2C2E;
        border: 1px solid #3A3A3C;
        border-radius: 8px;
        font-size: 0.75rem;
        padding: 4px 8px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1C1C1E;
        border-radius: 12px;
    }

    /* Compact video preview for upload area */
    .compact-video video {
        max-height: 180px !important;
        border-radius: 10px;
    }

    /* Result row - horizontal card for each variation */
    .result-row {
        background: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 10px;
        padding: 6px 10px;
        margin: 3px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .result-row:hover { background: #2C2C2E; }
    .rr-name {
        font-weight: 600;
        font-size: 0.85rem;
        color: #F5F5F7;
        min-width: 32px;
    }
    .rr-tags {
        flex: 1;
        line-height: 1.5;
    }
    .rr-score {
        min-width: 48px;
        text-align: center;
    }

    /* Virality card */
    .virality-card {
        background: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 16px;
        padding: 16px;
        margin: 8px 0;
    }
    .vir-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .vir-title {
        font-size: 1rem;
        font-weight: 600;
        color: #F5F5F7;
    }
    .vir-row {
        margin: 5px 0;
    }
    .vir-label {
        display: flex;
        justify-content: space-between;
        color: #86868B;
        font-size: 0.73rem;
        margin-bottom: 2px;
    }
    .vir-bar {
        background: #2C2C2E;
        border-radius: 3px;
        height: 4px;
        overflow: hidden;
    }
    .vir-fill {
        height: 100%;
        border-radius: 3px;
    }
    .vir-tips {
        margin-top: 10px;
        padding: 8px;
        background: #2C2C2E;
        border-radius: 8px;
        color: #FF9F0A;
        font-size: 0.7rem;
    }

    /* Caption cards */
    .caption-item {
        background: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 8px;
        padding: 8px 10px;
        margin: 3px 0;
        font-size: 0.8rem;
        color: #F5F5F7;
        white-space: pre-wrap;
    }
    .caption-num {
        color: #007AFF;
        font-weight: 700;
        font-size: 0.75rem;
    }

    /* URL platform badge */
    .platform-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .platform-tiktok { background: #1C1C1E; color: #FF004F; border: 1px solid #FF004F; }
    .platform-instagram { background: #1C1C1E; color: #E1306C; border: 1px solid #E1306C; }
    .platform-youtube { background: #1C1C1E; color: #FF0000; border: 1px solid #FF0000; }
    .platform-other { background: #1C1C1E; color: #86868B; border: 1px solid #3A3A3C; }
</style>
""", unsafe_allow_html=True)


# ============ HELPER FUNCTIONS ============

def estimate_uniqueness(modifications):
    """Estime l'unicité basée sur les vrais poids de détection TikTok/Instagram."""
    score = 0
    noise = modifications.get("noise", 0)
    score += min(noise * 3, 18)
    zoom = modifications.get("zoom", 1.0)
    score += min((zoom - 1.0) * 100 * 3.5, 14)
    gamma = abs(modifications.get("gamma", 1.0) - 1.0)
    score += min(gamma * 200, 5)
    hue = abs(modifications.get("hue_shift", 0))
    score += min(hue * 0.15, 2)
    if modifications.get("hflip", False):
        score += 12
    crop = modifications.get("crop_percent", 0)
    score += min(crop * 2, 4)
    speed = modifications.get("speed", 1.0)
    score += min(abs(speed - 1.0) * 40, 3)
    pitch = abs(modifications.get("pitch_semitones", 0))
    score += min(pitch * 35, 20)
    fps = modifications.get("fps", 30)
    score += min(abs(fps - 30) * 50, 5)
    score += 3  # volume
    if modifications.get("metadata_randomized", False):
        score += 5
    score += 8  # re-encoding
    return {'uniqueness': min(round(score), 100)}


def get_dated_folder_name():
    now = datetime.now()
    mois_fr = {1: "janvier", 2: "fevrier", 3: "mars", 4: "avril", 5: "mai", 6: "juin",
               7: "juillet", 8: "aout", 9: "septembre", 10: "octobre", 11: "novembre", 12: "decembre"}
    return f"{now.day} {mois_fr[now.month]} {now.strftime('%Hh%M')}"


def format_modifications_compact(mods):
    """Tags compacts pour la grille de résultats"""
    tags = []
    if mods.get("hflip"):
        tags.append('<span class="tag-sm tag-mirror">🪞 Miroir</span>')
    speed = mods.get("speed", 1.0)
    if abs(speed - 1.0) > 0.005:
        tags.append(f'<span class="tag-sm tag-speed">🔄 x{speed:.2f}</span>')
    hue = mods.get("hue_shift", 0)
    if abs(hue) > 0:
        tags.append(f'<span class="tag-sm tag-hue">🎨 {hue:+d}°</span>')
    crop = mods.get("crop_percent", 0)
    if crop > 0.1:
        tags.append(f'<span class="tag-sm tag-crop">✂️ {crop:.1f}%</span>')
    zoom = mods.get("zoom", 1.0)
    if zoom > 1.005:
        tags.append(f'<span class="tag-sm tag-zoom">🔍 {(zoom-1)*100:.1f}%</span>')
    noise = mods.get("noise", 0)
    if noise > 0:
        tags.append(f'<span class="tag-sm tag-noise">📡 N{noise:.0f}</span>')
    pitch = mods.get("pitch_semitones", 0)
    if abs(pitch) > 0.05:
        tags.append(f'<span class="tag-sm tag-pitch">🎵 {pitch:+.1f}st</span>')
    if mods.get("metadata_randomized"):
        tags.append('<span class="tag-sm tag-meta">🏷️ Meta</span>')
    return " ".join(tags) if tags else '<span style="color:#48484A;font-size:0.7rem">—</span>'


def get_uniqueness_badge(score):
    if score >= 60:
        return 'badge-safe'
    elif score >= 30:
        return 'badge-warning'
    return 'badge-danger'


def extract_thumbnail(video_path):
    """Extract a small square thumbnail from video for inline preview"""
    thumb_path = video_path + ".thumb.jpg"
    if os.path.exists(thumb_path):
        return thumb_path
    try:
        cmd = [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", "thumbnail,scale=120:-1",
            "-frames:v", "1", "-q:v", "5",
            thumb_path
        ]
        subprocess.run(cmd, capture_output=True, timeout=10)
        return thumb_path if os.path.exists(thumb_path) else None
    except:
        return None


# ============ NEW: URL DOWNLOAD ============

def detect_platform(url):
    """Detect social media platform from URL"""
    if not url:
        return None
    url_lower = url.lower()
    if "tiktok.com" in url_lower:
        return "tiktok"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    return "other"


def download_from_url(url):
    """Download video from TikTok/Instagram/YouTube URL using yt-dlp"""
    try:
        tmpdir = tempfile.mkdtemp()
        output_template = os.path.join(tmpdir, "video.%(ext)s")

        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--no-playlist",
            "--merge-output-format", "mp4",
            "-o", output_template,
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

        if result.returncode != 0:
            shutil.rmtree(tmpdir, ignore_errors=True)
            err = result.stderr.strip().split('\n')[-1] if result.stderr else "Erreur inconnue"
            return None, err[:300]

        # Find downloaded file
        files = [f for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir, f))]
        if not files:
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None, "Aucun fichier téléchargé"

        src = os.path.join(tmpdir, files[0])
        final = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        final.close()

        if src.endswith('.mp4'):
            shutil.move(src, final.name)
        else:
            conv = subprocess.run(
                ["ffmpeg", "-y", "-i", src, "-c:v", "libx264", "-c:a", "aac", "-preset", "ultrafast", final.name],
                capture_output=True, timeout=120
            )
            if conv.returncode != 0:
                shutil.rmtree(tmpdir, ignore_errors=True)
                return None, "Conversion MP4 échouée"

        shutil.rmtree(tmpdir, ignore_errors=True)

        if os.path.exists(final.name) and os.path.getsize(final.name) > 0:
            return final.name, None
        return None, "Fichier vide"

    except subprocess.TimeoutExpired:
        return None, "Timeout — vidéo trop longue ou serveur lent"
    except Exception as e:
        return None, str(e)


# ============ NEW: VIRALITY ANALYSIS ============

def analyze_virality(video_path):
    """Analyze video's virality potential based on technical properties"""
    # Get video info via ffprobe
    info = {}
    try:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        info = json.loads(r.stdout) if r.returncode == 0 else {}
    except:
        pass

    score = 0
    breakdown = []
    tips = []

    # Duration (max 25 pts)
    try:
        duration = float(info.get('format', {}).get('duration', 0))
    except:
        duration = 0

    if 7 <= duration <= 15:
        pts = 25
        breakdown.append(("⏱️ Durée", f"{duration:.0f}s — hook court parfait", pts, 25))
    elif 15 < duration <= 30:
        pts = 22
        breakdown.append(("⏱️ Durée", f"{duration:.0f}s — optimal TikTok", pts, 25))
    elif 30 < duration <= 60:
        pts = 18
        breakdown.append(("⏱️ Durée", f"{duration:.0f}s — ok Reels", pts, 25))
    elif duration > 60:
        pts = 8
        breakdown.append(("⏱️ Durée", f"{duration:.0f}s — trop long", pts, 25))
        tips.append("Couper à <30s pour maximiser la rétention")
    else:
        pts = 5
        breakdown.append(("⏱️ Durée", "Inconnue", pts, 25))
    score += pts

    # Format (max 20 pts)
    video_stream = None
    audio_stream = None
    for s in info.get('streams', []):
        if s.get('codec_type') == 'video' and not video_stream:
            video_stream = s
        if s.get('codec_type') == 'audio' and not audio_stream:
            audio_stream = s

    if video_stream:
        w = int(video_stream.get('width', 0))
        h = int(video_stream.get('height', 0))
        if h > w and h >= 1920:
            pts = 20
            breakdown.append(("📐 Format", f"{w}x{h} — vertical HD", pts, 20))
        elif h > w:
            pts = 15
            breakdown.append(("📐 Format", f"{w}x{h} — vertical", pts, 20))
            tips.append("Passer en 1080x1920 pour qualité max")
        elif w == h:
            pts = 10
            breakdown.append(("📐 Format", f"{w}x{h} — carré", pts, 20))
            tips.append("Format vertical (9:16) recommandé")
        else:
            pts = 5
            breakdown.append(("📐 Format", f"{w}x{h} — horizontal", pts, 20))
            tips.append("Recadrer en vertical pour Reels/TikTok")
        score += pts
    else:
        score += 5
        breakdown.append(("📐 Format", "Non détecté", 5, 20))

    # Audio (max 20 pts)
    if audio_stream:
        pts = 20
        breakdown.append(("🔊 Audio", "Présent — essentiel", pts, 20))
    else:
        pts = 2
        breakdown.append(("🔊 Audio", "Absent — -70% engagement", pts, 20))
        tips.append("Ajouter de l'audio (musique trending ou voiceover)")
    score += pts

    # Bitrate (max 15 pts)
    try:
        bitrate = int(info.get('format', {}).get('bit_rate', 0)) / 1000
        if bitrate >= 5000:
            pts = 15
            breakdown.append(("🎬 Qualité", f"{bitrate:.0f}kbps — excellente", pts, 15))
        elif bitrate >= 2000:
            pts = 12
            breakdown.append(("🎬 Qualité", f"{bitrate:.0f}kbps — bonne", pts, 15))
        elif bitrate >= 1000:
            pts = 8
            breakdown.append(("🎬 Qualité", f"{bitrate:.0f}kbps — ok", pts, 15))
        else:
            pts = 4
            breakdown.append(("🎬 Qualité", f"{bitrate:.0f}kbps — basse", pts, 15))
            tips.append("Augmenter le bitrate pour plus de netteté")
        score += pts
    except:
        score += 5
        breakdown.append(("🎬 Qualité", "Non détecté", 5, 15))

    # FPS (max 10 pts)
    if video_stream:
        try:
            fps_str = video_stream.get('r_frame_rate', '30/1')
            num, den = fps_str.split('/')
            fps = int(num) / max(int(den), 1)
            if fps >= 30:
                pts = 10
                breakdown.append(("🎞️ FPS", f"{fps:.0f} — fluide", pts, 10))
            elif fps >= 24:
                pts = 7
                breakdown.append(("🎞️ FPS", f"{fps:.0f} — correct", pts, 10))
            else:
                pts = 3
                breakdown.append(("🎞️ FPS", f"{fps:.0f} — saccadé", pts, 10))
                tips.append("Filmer en 30fps minimum")
            score += pts
        except:
            score += 5
            breakdown.append(("🎞️ FPS", "Non détecté", 5, 10))

    # File size (max 10 pts)
    try:
        fsize = os.path.getsize(video_path) / (1024 * 1024)
        if fsize <= 10:
            pts = 10
            breakdown.append(("📦 Taille", f"{fsize:.1f}MB — rapide", pts, 10))
        elif fsize <= 50:
            pts = 7
            breakdown.append(("📦 Taille", f"{fsize:.1f}MB — ok", pts, 10))
        else:
            pts = 3
            breakdown.append(("📦 Taille", f"{fsize:.1f}MB — lourd", pts, 10))
            tips.append("Compresser pour un upload plus rapide")
        score += pts
    except:
        score += 5
        breakdown.append(("📦 Taille", "Non détecté", 5, 10))

    return {
        'score': min(score, 100),
        'breakdown': breakdown,
        'tips': tips,
        'duration': duration,
        'has_audio': audio_stream is not None,
        'resolution': f"{video_stream.get('width', '?')}x{video_stream.get('height', '?')}" if video_stream else "?"
    }


def render_virality_html(analysis):
    """Render virality score as Apple-style HTML card"""
    score = analysis['score']
    badge = get_uniqueness_badge(score)

    rows_html = ""
    for label, desc, pts, max_pts in analysis['breakdown']:
        pct = (pts / max_pts * 100) if max_pts > 0 else 0
        color = "#30D158" if pct >= 70 else "#FF9F0A" if pct >= 40 else "#FF453A"
        rows_html += f"""<div class="vir-row">
            <div class="vir-label"><span>{label} — {desc}</span><span style="color:#F5F5F7;font-weight:500">{pts}/{max_pts}</span></div>
            <div class="vir-bar"><div class="vir-fill" style="background:{color};width:{pct}%"></div></div>
        </div>"""

    tips_html = ""
    if analysis['tips']:
        items = "".join(f"<div>💡 {t}</div>" for t in analysis['tips'])
        tips_html = f'<div class="vir-tips">{items}</div>'

    return f"""<div class="virality-card">
        <div class="vir-header">
            <span class="vir-title">🔥 Score de Viralité</span>
            <span class="{badge}" style="font-size:1.1rem;padding:6px 16px">{score}/100</span>
        </div>
        {rows_html}
        {tips_html}
    </div>"""


# ============ NEW: CAPTION GENERATION ============

def generate_caption_variants(duration=0, has_audio=True):
    """Generate 10 viral caption variants"""
    hooks = [
        "Personne ne parle de ça mais...",
        "J'aurais aimé savoir ça plus tôt",
        "Ce que personne ne te dit sur...",
        "La vérité que tout le monde ignore",
        "Attends de voir la fin...",
        "Tu ne devineras jamais ce qui se passe",
        "Le secret que les pros cachent",
        "Ça va changer ta façon de voir les choses",
        "3 astuces que j'utilise tous les jours",
        "La méthode qui a tout changé pour moi",
        "Voici comment faire en 30 secondes",
        "Fais ça et remercie-moi plus tard",
        "Ça m'a laissé sans voix...",
        "Quand tu réalises que...",
        "POV: tu découvres ça pour la première fois",
        "Avant vs Après — la différence est folle",
        "Sauvegarde avant que ça disparaisse",
        "Stop le scroll — regarde ça",
        "Si tu vois cette vidéo c'est un signe",
        "Ne rate pas la fin surtout",
    ]
    ctas = [
        "Follow pour plus de contenu comme ça",
        "Like si tu veux la partie 2",
        "Commente 🔥 si ça t'a aidé",
        "Enregistre pour plus tard",
        "Partage à quelqu'un qui en a besoin",
        "Abonne-toi pour ne rien manquer",
        "Dis-moi en commentaire ce que tu en penses",
    ]
    hashtag_sets = [
        "#fyp #pourtoi #viral #trending",
        "#foryou #astuce #hack #tips",
        "#trend #viral #mustsee #pourtoi",
        "#fyp #trending #mindblown #viral2026",
        "#reels #explore #trending #content",
    ]

    random.shuffle(hooks)
    variants = []
    for i in range(10):
        hook = hooks[i % len(hooks)]
        cta = random.choice(ctas)
        tags = random.choice(hashtag_sets)
        if duration and duration <= 15:
            v = f"{hook}\n\n{cta}\n\n{tags}"
        elif duration and duration <= 45:
            v = f"{hook}\n\n💡 Regarde jusqu'à la fin\n\n{cta}\n\n{tags}"
        else:
            v = f"{hook}\n\n⬇️ Tout est expliqué dans la vidéo\n\n{cta}\n\n{tags}"
        variants.append(v)
    return variants


# ============ RESULT GRID RENDERER ============

def render_results_grid(analyses, folder_name, key_prefix, virality=None, captions=None):
    """Render results as horizontal grid — everything on one line per variation"""
    if not analyses:
        return

    # Header
    st.markdown(f"<div class='folder-badge'>📁 {folder_name}/</div>", unsafe_allow_html=True)
    st.markdown("""<div class="legend">
    🟢 <b>≥ 60%</b> = Safe TikTok + Instagram &nbsp;|&nbsp;
    🟠 <b>30-59%</b> = Safe TikTok, risqué Insta &nbsp;|&nbsp;
    🔴 <b>< 30%</b> = Risque de détection
    </div>""", unsafe_allow_html=True)

    # Grid: each variation = one horizontal row
    for idx, a in enumerate(analyses):
        u = a['uniqueness']
        badge = get_uniqueness_badge(u)
        mods_html = format_modifications_compact(a.get('modifications', {}))

        # Columns: Name | Tags | Score | Preview | Download
        c_name, c_tags, c_score, c_prev, c_dl = st.columns([0.6, 4.5, 0.8, 1.8, 1.5])

        with c_name:
            st.markdown(f"**{a['name']}**")

        with c_tags:
            st.markdown(mods_html, unsafe_allow_html=True)

        with c_score:
            st.markdown(f'<span class="{badge}">{u:.0f}%</span>', unsafe_allow_html=True)

        with c_prev:
            thumb = a.get('thumbnail')
            if thumb and os.path.exists(thumb):
                st.image(thumb, width=80)
            else:
                # Try to generate thumbnail on the fly
                path = a.get('output_path', '')
                if path and os.path.exists(path):
                    t = extract_thumbnail(path)
                    if t:
                        st.image(t, width=80)

        with c_dl:
            path = a.get('output_path', '')
            if path and os.path.exists(path):
                with open(path, 'rb') as f:
                    st.download_button(
                        "⬇️",
                        f.read(),
                        file_name=f"{a['name']}.mp4",
                        mime="video/mp4",
                        key=f"dl_{key_prefix}_{idx}_{a['name']}"
                    )

    # Summary metrics
    avg_u = sum(a['uniqueness'] for a in analyses) / len(analyses)
    safe = sum(1 for a in analyses if a['uniqueness'] >= 60)
    st.markdown(f"""<div style="background:#1C1C1E;border:1px solid #2C2C2E;border-radius:10px;padding:8px 14px;margin:8px 0;font-size:0.8rem;color:#86868B">
        📊 Moyenne: <b style="color:#F5F5F7">{avg_u:.0f}%</b> &nbsp;|&nbsp;
        ✅ Safe: <b style="color:#30D158">{safe}/{len(analyses)}</b> &nbsp;|&nbsp;
        📹 Total: <b style="color:#F5F5F7">{len(analyses)}</b>
    </div>""", unsafe_allow_html=True)

    # Virality card if available
    if virality:
        with st.expander("🔥 Score de Viralité", expanded=False):
            st.markdown(render_virality_html(virality), unsafe_allow_html=True)

    # Caption variants if available
    if captions:
        with st.expander("📝 10 Variantes de Captions", expanded=False):
            for i, cap in enumerate(captions):
                st.code(cap, language=None)


# ============ GENERATION ENGINE ============

def run_generation(input_path, num_vars, output_dir, intensity, enabled_mods, progress_bar, status_text):
    """Generate variations and return analyses list + folder name"""
    from uniquifier import uniquify_video_ffmpeg

    folder_name = get_dated_folder_name()
    dated_dir = os.path.join(output_dir, folder_name)
    os.makedirs(dated_dir, exist_ok=True)

    analyses = []
    for i in range(num_vars):
        status_text.text(f"⏳ V{i+1:02d}/{num_vars}...")
        out_path = os.path.join(dated_dir, f"V{i+1:02d}.mp4")
        r = uniquify_video_ffmpeg(input_path, out_path, intensity, enabled_mods)

        if r["success"]:
            mods = r.get("modifications", {})
            analysis = estimate_uniqueness(mods)
            analysis['name'] = Path(out_path).stem
            analysis['modifications'] = mods
            analysis['output_path'] = out_path
            analysis['thumbnail'] = extract_thumbnail(out_path)
            analyses.append(analysis)

        progress_bar.progress((i + 1) / num_vars)

    return analyses, folder_name


LEGEND_HTML = """<div class="legend">
🟢 <b>≥ 60%</b> = Safe TikTok + Instagram &nbsp;|&nbsp;
🟠 <b>30-59%</b> = Safe TikTok, risqué Insta &nbsp;|&nbsp;
🔴 <b>< 30%</b> = Risque de détection
</div>"""


# ============ MAIN APP ============

def main():
    # Header
    st.markdown("""
    <div class="header-bar">
        <span class="header-logo">LTP</span>
        <span class="header-title">TikFusion</span>
    </div>
    """, unsafe_allow_html=True)

    # ============ TABS ============
    tab_url, tab_single, tab_bulk, tab_stats, tab_config = st.tabs([
        "🔗 Import", "📤 Single", "📦 Bulk", "📊 Stats", "⚙️ Config"
    ])

    # ========== CONFIG TAB (read first for variables) ==========
    with tab_config:
        st.markdown("### ⚙️ Configuration générale")
        c1, c2 = st.columns(2)
        with c1:
            output_dir = st.text_input("📁 Dossier de sortie", value="outputs", key="cfg_output")
        with c2:
            intensity = st.select_slider("🎚️ Intensité", options=["low", "medium", "high"], value="medium", key="cfg_intensity")

        st.markdown("---")
        st.markdown("### 🎛️ Modifications anti-détection")

        st.markdown("#### 👁️ Anti Hash Visuel")
        st.caption("Poids détection TikTok/Insta : ~30-35%")
        vc1, vc2 = st.columns(2)
        with vc1:
            mod_noise = st.toggle("📡 Pixel Noise", value=True, key="mod_noise",
                help="Bruit invisible par pixel. Le plus efficace contre pHash.")
            mod_zoom = st.toggle("🔍 Zoom aléatoire", value=True, key="mod_zoom",
                help="Zoom léger qui repositionne tous les pixels.")
        with vc2:
            mod_gamma = st.toggle("🌗 Gamma", value=True, key="mod_gamma",
                help="Modifie la courbe de luminosité globale.")
            mod_hue = st.toggle("🎨 Décalage couleur", value=True, key="mod_hue",
                help="Change la teinte. pHash résiste partiellement.")

        st.markdown("---")
        st.markdown("#### 🧠 Anti Deep Learning")
        st.caption("Poids détection : ~25-30%")
        sc1, sc2 = st.columns(2)
        with sc1:
            mod_hflip = st.toggle("🪞 Miroir horizontal", value=True, key="mod_hflip",
                help="Inverse horizontalement. Change toutes les relations spatiales.")
            mod_crop = st.toggle("✂️ Crop aléatoire", value=True, key="mod_crop",
                help="Coupe les bords. Change les limites du frame.")
        with sc2:
            mod_speed = st.toggle("🔄 Changement vitesse", value=True, key="mod_speed",
                help="Accélère ou ralentit. Change le fingerprint temporel.")

        st.markdown("---")
        st.markdown("#### 🔊 Anti Fingerprint Audio")
        st.caption("Poids détection : ~20-25%")
        ac1, ac2 = st.columns(2)
        with ac1:
            mod_pitch = st.toggle("🎵 Pitch shift", value=True, key="mod_pitch",
                help="Décale la fréquence audio. Imperceptible mais casse le fingerprint.")
        with ac2:
            mod_fps = st.toggle("🎞️ FPS shift", value=True, key="mod_fps",
                help="Change le framerate. Modifie le timing audio/vidéo.")

        st.markdown("---")
        st.markdown("#### 🏷️ Metadata")
        mod_meta = st.toggle("🏷️ Metadata aléatoires", value=True, key="mod_meta",
            help="Randomise titre, encodeur, date, UUID, etc.")

        st.markdown("---")

        # Score preview
        preview_score = 0
        details = []
        if mod_noise: preview_score += 14; details.append("📡 +14")
        if mod_zoom: preview_score += 12; details.append("🔍 +12")
        if mod_gamma: preview_score += 4; details.append("🌗 +4")
        if mod_hue: preview_score += 1; details.append("🎨 +1")
        if mod_hflip: preview_score += 5; details.append("🪞 +5")
        if mod_crop: preview_score += 2; details.append("✂️ +2")
        if mod_speed: preview_score += 1; details.append("🔄 +1")
        if mod_pitch: preview_score += 17; details.append("🎵 +17")
        if mod_fps: preview_score += 3; details.append("🎞️ +3")
        preview_score += 3; details.append("🔊 +3")
        if mod_meta: preview_score += 5; details.append("🏷️ +5")
        preview_score += 8; details.append("💾 +8")
        preview_score = min(preview_score, 100)

        badge_class = get_uniqueness_badge(preview_score)
        status_text = "🟢 Safe" if preview_score >= 60 else "🟠 Attention" if preview_score >= 30 else "🔴 Risque"
        st.markdown(f"""
        <div style="background:#1C1C1E;border:1px solid #2C2C2E;border-radius:12px;padding:14px;margin:8px 0">
            <div style="display:flex;align-items:center;justify-content:space-between">
                <span style="font-size:1rem;font-weight:600;color:#F5F5F7">📊 Score estimé moyen</span>
                <span class="{badge_class}" style="font-size:1.1rem;padding:5px 14px">{preview_score}%</span>
            </div>
            <div style="color:#86868B;font-size:0.75rem;margin-top:6px">{" • ".join(details)}</div>
            <div style="margin-top:6px;color:#48484A;font-size:0.7rem">{status_text}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        if os.path.exists(output_dir):
            st.markdown("**📁 Sessions récentes**")
            folders = sorted([f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))], reverse=True)
            for folder in folders[:5]:
                count = len(list(Path(os.path.join(output_dir, folder)).rglob("*.mp4")))
                st.text(f"  📁 {folder} ({count} vidéos)")

    # ========== GET CONFIG VALUES ==========
    output_dir = st.session_state.get('cfg_output', 'outputs')
    intensity = st.session_state.get('cfg_intensity', 'medium')
    enabled_mods = {
        "noise": st.session_state.get("mod_noise", True),
        "zoom": st.session_state.get("mod_zoom", True),
        "gamma": st.session_state.get("mod_gamma", True),
        "hue": st.session_state.get("mod_hue", True),
        "hflip": st.session_state.get("mod_hflip", True),
        "crop": st.session_state.get("mod_crop", True),
        "speed": st.session_state.get("mod_speed", True),
        "pitch": st.session_state.get("mod_pitch", True),
        "fps": st.session_state.get("mod_fps", True),
        "meta": st.session_state.get("mod_meta", True),
    }

    # ========== TAB: IMPORT URL ==========
    with tab_url:
        st.markdown("### 🔗 Importer depuis une URL")

        url = st.text_input(
            "Colle un lien TikTok, Instagram Reel ou YouTube Short",
            placeholder="https://www.tiktok.com/@user/video/123...",
            key="url_input"
        )

        if url:
            platform = detect_platform(url)
            platform_labels = {
                "tiktok": ("TikTok", "platform-tiktok"),
                "instagram": ("Instagram", "platform-instagram"),
                "youtube": ("YouTube", "platform-youtube"),
                "other": ("Autre", "platform-other"),
            }
            label, css_class = platform_labels.get(platform, ("Autre", "platform-other"))
            st.markdown(f'<span class="platform-badge {css_class}">{label}</span>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 3])

        with col_left:
            if url and st.button("📥 Télécharger", type="primary", key="url_dl_btn", use_container_width=True):
                with st.spinner("Téléchargement en cours..."):
                    path, error = download_from_url(url)
                    if error:
                        st.error(f"Erreur: {error}")
                    else:
                        st.session_state['url_video_path'] = path
                        st.session_state.pop('url_analyses', None)
                        st.session_state.pop('url_virality', None)
                        st.session_state.pop('url_captions', None)
                        st.rerun()

            if 'url_video_path' in st.session_state:
                vpath = st.session_state['url_video_path']
                if os.path.exists(vpath):
                    st.markdown('<div class="compact-video">', unsafe_allow_html=True)
                    st.video(vpath)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Virality analysis (auto)
                    if 'url_virality' not in st.session_state:
                        st.session_state['url_virality'] = analyze_virality(vpath)
                    st.markdown(render_virality_html(st.session_state['url_virality']), unsafe_allow_html=True)

                    num_vars = st.slider("Variations", 1, 15, 5, key="url_vars")

                    if st.button("Générer", type="primary", key="url_gen_btn", use_container_width=True):
                        progress = st.progress(0)
                        status = st.empty()
                        try:
                            analyses, folder = run_generation(vpath, num_vars, output_dir, intensity, enabled_mods, progress, status)
                            st.session_state['url_analyses'] = analyses
                            st.session_state['url_folder'] = folder
                            # Generate captions
                            vir = st.session_state.get('url_virality', {})
                            st.session_state['url_captions'] = generate_caption_variants(
                                vir.get('duration', 0), vir.get('has_audio', True)
                            )
                            status.empty()
                            progress.empty()
                            st.success(f"✅ {len(analyses)} variations")
                        except Exception as e:
                            st.error(f"Erreur: {e}")

        with col_right:
            if 'url_analyses' in st.session_state:
                render_results_grid(
                    st.session_state['url_analyses'],
                    st.session_state.get('url_folder', ''),
                    "url",
                    st.session_state.get('url_virality'),
                    st.session_state.get('url_captions')
                )
            else:
                st.markdown("""
                <div style="background:#1C1C1E;border:1px solid #2C2C2E;border-radius:12px;padding:24px;text-align:center;color:#48484A;margin-top:20px">
                    <div style="font-size:2rem;margin-bottom:8px">🔗</div>
                    <div>Colle une URL TikTok, Instagram ou YouTube</div>
                    <div style="font-size:0.75rem;margin-top:4px">La vidéo sera téléchargée automatiquement</div>
                </div>""", unsafe_allow_html=True)

    # ========== TAB: SINGLE UPLOAD ==========
    with tab_single:
        col_upload, col_results = st.columns([1, 3])

        with col_upload:
            uploaded = st.file_uploader("📹 Vidéo source", type=['mp4', 'mov', 'avi'], key="single")

            if uploaded:
                # Save to temp for virality analysis
                if 'single_temp_path' not in st.session_state:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                    tmp.write(uploaded.read())
                    tmp.close()
                    st.session_state['single_temp_path'] = tmp.name
                    uploaded.seek(0)

                st.markdown('<div class="compact-video">', unsafe_allow_html=True)
                st.video(uploaded)
                st.markdown('</div>', unsafe_allow_html=True)

                # Virality analysis (auto)
                temp_path = st.session_state.get('single_temp_path')
                if temp_path and os.path.exists(temp_path):
                    if 'single_virality' not in st.session_state:
                        st.session_state['single_virality'] = analyze_virality(temp_path)
                    st.markdown(render_virality_html(st.session_state['single_virality']), unsafe_allow_html=True)

                num_vars = st.slider("Variations", 1, 15, 5, key="single_vars")

                if st.button("Générer", type="primary", key="single_btn", use_container_width=True):
                    # Use the already saved temp file
                    temp_path = st.session_state.get('single_temp_path')
                    if not temp_path or not os.path.exists(temp_path):
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        tmp.write(uploaded.read())
                        tmp.close()
                        temp_path = tmp.name

                    progress = st.progress(0)
                    status = st.empty()

                    try:
                        analyses, folder = run_generation(temp_path, num_vars, output_dir, intensity, enabled_mods, progress, status)
                        st.session_state['single_analyses'] = analyses
                        st.session_state['single_folder'] = folder
                        vir = st.session_state.get('single_virality', {})
                        st.session_state['single_captions'] = generate_caption_variants(
                            vir.get('duration', 0), vir.get('has_audio', True)
                        )
                        status.empty()
                        progress.empty()
                        st.success(f"✅ {len(analyses)} variations")
                    except Exception as e:
                        st.error(f"Erreur: {e}")
            else:
                # Clear temp path when no file uploaded
                if 'single_temp_path' in st.session_state:
                    try:
                        os.unlink(st.session_state['single_temp_path'])
                    except:
                        pass
                    del st.session_state['single_temp_path']
                st.session_state.pop('single_virality', None)

        with col_results:
            if 'single_analyses' in st.session_state:
                render_results_grid(
                    st.session_state['single_analyses'],
                    st.session_state.get('single_folder', ''),
                    "single",
                    st.session_state.get('single_virality'),
                    st.session_state.get('single_captions')
                )

    # ========== TAB: BULK ==========
    with tab_bulk:
        col_upload, col_results = st.columns([1, 3])

        with col_upload:
            uploaded_files = st.file_uploader(
                "📹 Plusieurs vidéos",
                type=['mp4', 'mov', 'avi'],
                accept_multiple_files=True,
                key="bulk"
            )

            if uploaded_files:
                if len(uploaded_files) > 10:
                    st.warning("⚠️ Max 10 vidéos.")
                    uploaded_files = uploaded_files[:10]
                st.success(f"{len(uploaded_files)} vidéos")

                for f in uploaded_files[:3]:
                    st.caption(f"📹 {f.name}")
                if len(uploaded_files) > 3:
                    st.caption(f"... +{len(uploaded_files) - 3} autres")

                vars_per_video = st.slider("Var / vidéo", 1, 10, 3, key="bulk_vars")
                total = len(uploaded_files) * vars_per_video
                st.info(f"**{total} vidéos** au total")

                if st.button("Lancer", type="primary", key="bulk_btn", use_container_width=True):
                    bulk_folder = get_dated_folder_name() + " - BULK"
                    bulk_path = os.path.join(output_dir, bulk_folder)
                    os.makedirs(bulk_path, exist_ok=True)

                    overall_progress = st.progress(0)
                    status = st.empty()
                    all_results = []

                    try:
                        from uniquifier import uniquify_video_ffmpeg

                        for vid_idx, uploaded_file in enumerate(uploaded_files):
                            video_name = Path(uploaded_file.name).stem
                            status.text(f"⏳ [{vid_idx + 1}/{len(uploaded_files)}] {video_name}")

                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                                tmp.write(uploaded_file.read())
                                original_path = tmp.name

                            video_folder = os.path.join(bulk_path, video_name)
                            os.makedirs(video_folder, exist_ok=True)

                            video_results = {'name': video_name, 'variations': [], 'success_count': 0}

                            for var_idx in range(vars_per_video):
                                output_path = os.path.join(video_folder, f"V{var_idx + 1:02d}.mp4")
                                result = uniquify_video_ffmpeg(original_path, output_path, intensity, enabled_mods)

                                if result["success"]:
                                    mods = result.get("modifications", {})
                                    analysis = estimate_uniqueness(mods)
                                    video_results['variations'].append({
                                        'name': f"V{var_idx + 1:02d}",
                                        'output_path': output_path,
                                        'uniqueness': analysis['uniqueness'],
                                        'modifications': mods,
                                        'thumbnail': extract_thumbnail(output_path)
                                    })
                                    video_results['success_count'] += 1

                            all_results.append(video_results)
                            os.unlink(original_path)
                            overall_progress.progress((vid_idx + 1) / len(uploaded_files))

                        st.session_state['bulk_results'] = all_results
                        st.session_state['bulk_folder'] = bulk_folder

                        status.empty()
                        total_success = sum(r['success_count'] for r in all_results)
                        st.success(f"✅ {total_success} vidéos")

                    except Exception as e:
                        st.error(f"Erreur: {e}")

        with col_results:
            if 'bulk_results' in st.session_state:
                results = st.session_state['bulk_results']
                bulk_folder = st.session_state.get('bulk_folder', '')

                # Summary
                total_videos = sum(r['success_count'] for r in results)
                all_variations = [v for r in results for v in r['variations']]
                avg_u = sum(v['uniqueness'] for v in all_variations) / len(all_variations) if all_variations else 0
                safe_count = sum(1 for v in all_variations if v['uniqueness'] >= 60)

                m1, m2, m3 = st.columns(3)
                m1.metric("📹 Total", total_videos)
                m2.metric("📊 Moy.", f"{avg_u:.0f}%")
                m3.metric("✅ Safe", f"{safe_count}/{len(all_variations)}")

                st.markdown(LEGEND_HTML, unsafe_allow_html=True)

                for r in results:
                    with st.expander(f"📹 {r['name']} — {r['success_count']} var.", expanded=True):
                        for vi, v in enumerate(r['variations']):
                            u = v['uniqueness']
                            badge = get_uniqueness_badge(u)
                            mods_html = format_modifications_compact(v.get('modifications', {}))

                            c_name, c_tags, c_score, c_prev, c_dl = st.columns([0.6, 4.5, 0.8, 1.8, 1.5])

                            with c_name:
                                st.markdown(f"**{v['name']}**")
                            with c_tags:
                                st.markdown(mods_html, unsafe_allow_html=True)
                            with c_score:
                                st.markdown(f'<span class="{badge}">{u:.0f}%</span>', unsafe_allow_html=True)
                            with c_prev:
                                thumb = v.get('thumbnail')
                                if thumb and os.path.exists(thumb):
                                    st.image(thumb, width=80)
                                else:
                                    vpath = v.get('output_path', '')
                                    if vpath and os.path.exists(vpath):
                                        t = extract_thumbnail(vpath)
                                        if t:
                                            st.image(t, width=80)
                            with c_dl:
                                vpath = v.get('output_path', '')
                                if vpath and os.path.exists(vpath):
                                    with open(vpath, 'rb') as f:
                                        st.download_button(
                                            "⬇️",
                                            f.read(),
                                            file_name=f"{r['name']}_{v['name']}.mp4",
                                            mime="video/mp4",
                                            key=f"dl_bulk_{r['name']}_{v['name']}"
                                        )
            else:
                st.info("👈 Upload plusieurs vidéos et lance le traitement")

    # ========== TAB: STATS ==========
    with tab_stats:
        st.markdown("### 📊 Statistiques")

        if os.path.exists(output_dir):
            all_videos = list(Path(output_dir).rglob("*.mp4"))
            all_folders = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]
            total_size = sum(f.stat().st_size for f in all_videos) / (1024 * 1024)

            col1, col2, col3 = st.columns(3)
            col1.metric("📁 Sessions", len(all_folders))
            col2.metric("📹 Total vidéos", len(all_videos))
            col3.metric("💾 Espace", f"{total_size:.1f} MB")

            st.markdown("---")
            st.markdown("**📁 Toutes les sessions**")
            for folder in sorted(all_folders, reverse=True):
                folder_path = os.path.join(output_dir, folder)
                videos = list(Path(folder_path).rglob("*.mp4"))
                st.text(f"  📁 {folder} — {len(videos)} vidéos")


if __name__ == "__main__":
    main()
