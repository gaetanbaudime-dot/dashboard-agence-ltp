"""
TikFusion MVP — Video uniquifier anti-detection
Single | Bulk | Stats | Config
"""
import streamlit as st
import os
import sys
import subprocess
import shutil
import tempfile
import base64
import zipfile
import io
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from uniquifier import uniquify_video_ffmpeg, _find_ffmpeg, FFMPEG_BIN

st.set_page_config(page_title="TikFusion x LTP", layout="wide", initial_sidebar_state="collapsed")

# ============ CSS ============
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    * { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif; }
    .header-bar {
        display: flex; align-items: center; justify-content: center; gap: 16px;
        padding: 12px 0 8px 0; border-bottom: 1px solid #2C2C2E; margin-bottom: 16px;
    }
    .header-logo {
        background: #F5F5F7; color: #000; font-weight: 800; font-size: 1.3rem;
        padding: 6px 14px; border-radius: 8px; letter-spacing: 2px;
    }
    .header-title { font-size: 2rem; font-weight: 700; color: #F5F5F7; letter-spacing: -0.5px; }
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: #1C1C1E; border-radius: 12px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 20px; font-weight: 500; color: #86868B !important; }
    .stTabs [aria-selected="true"] { background: #007AFF !important; color: #FFF !important; }
    .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span { color: inherit !important; }
    .stButton > button[kind="primary"] { background: #007AFF; border: none; border-radius: 10px; font-weight: 600; }
    .stButton > button[kind="primary"]:hover { background: #0056CC; }
    .stDownloadButton > button { background: #2C2C2E; border: 1px solid #3A3A3C; border-radius: 8px; font-size: 0.75rem; }
    .compact-video video { max-height: 180px !important; border-radius: 10px; }
    .tag-sm {
        display: inline-block; padding: 2px 5px; border-radius: 4px;
        font-size: 0.62rem; font-weight: 500; margin: 1px;
    }
    .tag-mirror { background: #FF453A; color: white; }
    .tag-speed { background: #1C1C1E; color: #64D2FF; border: 1px solid #3A3A3C; }
    .tag-hue { background: #1C1C1E; color: #FF9F0A; border: 1px solid #3A3A3C; }
    .tag-crop { background: #1C1C1E; color: #30D158; border: 1px solid #3A3A3C; }
    .tag-zoom { background: #1C1C1E; color: #FFD60A; border: 1px solid #3A3A3C; }
    .tag-noise { background: #1C1C1E; color: #FF6482; border: 1px solid #3A3A3C; }
    .tag-pitch { background: #1C1C1E; color: #5E5CE6; border: 1px solid #3A3A3C; }
    .tag-meta { background: #1C1C1E; color: #BF5AF2; border: 1px solid #3A3A3C; }
    .badge-safe { background: #30D158; color: white; padding: 3px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .badge-warning { background: #FF9F0A; color: white; padding: 3px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .badge-danger { background: #FF453A; color: white; padding: 3px 10px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .rg-table { width: 100%; border-collapse: separate; border-spacing: 0 3px; }
    .rg-head td { padding: 4px 10px; font-size: 0.68rem; font-weight: 600; color: #48484A; text-transform: uppercase; letter-spacing: 0.5px; }
    .rg-row td { background: #1C1C1E; padding: 5px 10px; vertical-align: middle; }
    .rg-row td:first-child { border-radius: 10px 0 0 10px; }
    .rg-row td:last-child { border-radius: 0 10px 10px 0; }
    .rg-row:hover td { background: #232325; }
    .rg-name { font-weight: 700; font-size: 0.85rem; color: #F5F5F7; white-space: nowrap; }
    .rg-tags { line-height: 1.6; }
    .rg-score { text-align: center; white-space: nowrap; }
    .rg-thumb { height: 80px; border-radius: 6px; object-fit: cover; }
    .legend {
        background: #1C1C1E; border: 1px solid #2C2C2E; border-radius: 8px;
        padding: 5px 12px; font-size: 0.7rem; color: #86868B; margin-bottom: 8px;
    }
    .folder-badge {
        background: #1C1C1E; color: #64D2FF; padding: 5px 12px; border-radius: 8px;
        font-family: 'SF Mono', monospace; font-size: 0.78rem;
        border: 1px solid #2C2C2E; display: inline-block; margin-bottom: 6px;
    }
    [data-testid="stMetric"] { background: #1C1C1E; border: 1px solid #2C2C2E; border-radius: 12px; padding: 10px; }
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] { margin-bottom: -6px; }
    .preview-grid video { border-radius: 10px; max-height: 200px; }
</style>
""", unsafe_allow_html=True)


# ============ HELPERS ============

def _ffmpeg():
    return _find_ffmpeg()

def _ffprobe():
    from uniquifier import FFPROBE_BIN
    _find_ffmpeg()
    return FFPROBE_BIN or "ffprobe"


def estimate_uniqueness(modifications):
    score = 0
    score += min(modifications.get("noise", 0) * 3, 18)
    score += min((modifications.get("zoom", 1.0) - 1.0) * 350, 14)
    score += min(abs(modifications.get("gamma", 1.0) - 1.0) * 200, 5)
    score += min(abs(modifications.get("hue_shift", 0)) * 0.15, 2)
    if modifications.get("hflip", False): score += 12
    score += min(modifications.get("crop_percent", 0) * 2, 4)
    score += min(abs(modifications.get("speed", 1.0) - 1.0) * 40, 3)
    score += min(abs(modifications.get("pitch_semitones", 0)) * 35, 20)
    score += min(abs(modifications.get("fps", 30) - 30) * 50, 5)
    score += 3  # volume
    if modifications.get("metadata_randomized", False): score += 5
    score += 8  # re-encoding
    return min(round(score), 100)


def get_dated_folder():
    now = datetime.now()
    m = {1:"janvier",2:"fevrier",3:"mars",4:"avril",5:"mai",6:"juin",
         7:"juillet",8:"aout",9:"septembre",10:"octobre",11:"novembre",12:"decembre"}
    return f"{now.day} {m[now.month]} {now.strftime('%Hh%M')}"


def format_tags(mods):
    t = []
    if mods.get("hflip"): t.append('<span class="tag-sm tag-mirror">Miroir</span>')
    s = mods.get("speed", 1.0)
    if abs(s-1) > .005: t.append(f'<span class="tag-sm tag-speed">x{s:.2f}</span>')
    h = mods.get("hue_shift", 0)
    if abs(h) > 0: t.append(f'<span class="tag-sm tag-hue">{h:+d}deg</span>')
    c = mods.get("crop_percent", 0)
    if c > .1: t.append(f'<span class="tag-sm tag-crop">{c:.1f}%</span>')
    z = mods.get("zoom", 1.0)
    if z > 1.005: t.append(f'<span class="tag-sm tag-zoom">+{(z-1)*100:.1f}%</span>')
    n = mods.get("noise", 0)
    if n > 0: t.append(f'<span class="tag-sm tag-noise">N{n:.0f}</span>')
    p = mods.get("pitch_semitones", 0)
    if abs(p) > .05: t.append(f'<span class="tag-sm tag-pitch">{p:+.1f}st</span>')
    if mods.get("metadata_randomized"): t.append('<span class="tag-sm tag-meta">Meta</span>')
    return " ".join(t) if t else '<span style="color:#48484A;font-size:.7rem">-</span>'


def get_badge(score):
    if score >= 60: return 'badge-safe'
    if score >= 30: return 'badge-warning'
    return 'badge-danger'


def extract_thumbnail(video_path):
    thumb = video_path + ".thumb.jpg"
    if os.path.exists(thumb): return thumb
    try:
        subprocess.run([_ffmpeg(), "-y", "-i", video_path, "-vf", "thumbnail,scale=120:-1",
                        "-frames:v", "1", "-q:v", "5", thumb], capture_output=True, timeout=10)
        return thumb if os.path.exists(thumb) else None
    except:
        return None


def thumb_b64(path):
    thumb = extract_thumbnail(path) if not path.endswith('.thumb.jpg') else path
    if thumb and os.path.exists(thumb):
        with open(thumb, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None


# ============ GENERATION ============

def run_generation(input_path, num_vars, output_dir, intensity, enabled_mods, progress_bar, status_el):
    ffmpeg = _ffmpeg()
    if not ffmpeg or not shutil.which(ffmpeg) and not os.path.isfile(ffmpeg):
        st.error("FFmpeg non trouve. Verifiez l'installation.")
        return [], ""

    folder = get_dated_folder()
    out_dir = os.path.join(output_dir, folder)
    os.makedirs(out_dir, exist_ok=True)

    results = []
    for i in range(num_vars):
        status_el.text(f"V{i+1:02d}/{num_vars}...")
        out = os.path.join(out_dir, f"V{i+1:02d}.mp4")
        r = uniquify_video_ffmpeg(input_path, out, intensity, enabled_mods)
        if r["success"]:
            mods = r.get("modifications", {})
            u = estimate_uniqueness(mods)
            results.append({
                'name': Path(out).stem,
                'uniqueness': u,
                'modifications': mods,
                'output_path': out,
                'thumbnail': extract_thumbnail(out),
            })
        progress_bar.progress((i+1) / num_vars)

    if not results:
        st.error("0 variations generees. FFmpeg a echoue sur toutes les tentatives.")
    return results, folder


# ============ RESULTS DISPLAY ============

def build_zip(analyses, folder):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for a in analyses:
            p = a.get('output_path', '')
            if p and os.path.exists(p):
                zf.write(p, f"{a['name']}.mp4")
    buf.seek(0)
    return buf.getvalue()


def build_safe_zip(analyses, folder):
    safe = [a for a in analyses if a['uniqueness'] >= 60]
    if not safe:
        return None, 0
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for a in safe:
            p = a.get('output_path', '')
            if p and os.path.exists(p):
                zf.write(p, f"{a['name']}.mp4")
    buf.seek(0)
    return buf.getvalue(), len(safe)


def render_results(analyses, folder, prefix):
    if not analyses:
        return

    avg = sum(a['uniqueness'] for a in analyses) / len(analyses)
    safe = sum(1 for a in analyses if a['uniqueness'] >= 60)

    # Top bar
    t1, t2, t3, t4 = st.columns([2, 1.2, 1, 1.2])
    with t1:
        st.markdown(f"<div class='folder-badge'>{folder}/</div>", unsafe_allow_html=True)
    with t2:
        st.markdown(f"""<div style="background:#1C1C1E;border:1px solid #2C2C2E;border-radius:8px;padding:6px 10px;
            font-size:0.78rem;color:#86868B;text-align:center">
            Moy. <b style="color:#F5F5F7">{avg:.0f}%</b> | <b style="color:#30D158">{safe}/{len(analyses)}</b> safe
        </div>""", unsafe_allow_html=True)
    with t3:
        st.download_button("ZIP Tout", build_zip(analyses, folder),
                           file_name=f"{folder}.zip", mime="application/zip",
                           key=f"zip_{prefix}", use_container_width=True)
    with t4:
        safe_zip, safe_count = build_safe_zip(analyses, folder)
        if safe_zip:
            st.download_button(f"ZIP Safe IG ({safe_count})", safe_zip,
                               file_name=f"{folder}_safe.zip", mime="application/zip",
                               key=f"zipsafe_{prefix}", use_container_width=True)

    st.markdown("""<div class="legend">Safe IG = score >= 60%</div>""", unsafe_allow_html=True)

    # Grid table
    grid = '<table class="rg-table"><tr class="rg-head"><td style="width:36px">#</td><td>Modifications</td><td style="width:56px">Score</td><td style="width:90px">Apercu</td></tr>'
    for a in analyses:
        u = a['uniqueness']
        badge = get_badge(u)
        tags = format_tags(a.get('modifications', {}))
        t_img = '<span style="color:#48484A;font-size:.7rem">-</span>'
        t = a.get('thumbnail')
        if not t or not os.path.exists(t):
            tp = a.get('output_path', '')
            if tp and os.path.exists(tp):
                t = extract_thumbnail(tp)
        if t and os.path.exists(t):
            b64 = thumb_b64(t)
            if b64:
                t_img = f'<img src="data:image/jpeg;base64,{b64}" class="rg-thumb" />'
        grid += f"""<tr class="rg-row">
            <td><span class="rg-name">{a['name']}</span></td>
            <td><span class="rg-tags">{tags}</span></td>
            <td class="rg-score"><span class="{badge}">{u}%</span></td>
            <td style="text-align:center">{t_img}</td>
        </tr>\n"""
    grid += '</table>'
    st.markdown(grid, unsafe_allow_html=True)

    # Download buttons
    per_row = 5
    for start in range(0, len(analyses), per_row):
        chunk = analyses[start:start+per_row]
        cols = st.columns(per_row)
        for i, a in enumerate(chunk):
            p = a.get('output_path', '')
            if p and os.path.exists(p):
                with cols[i]:
                    with open(p, 'rb') as f:
                        st.download_button(f"V{a['name']}", f.read(),
                                           file_name=f"{a['name']}.mp4", mime="video/mp4",
                                           key=f"dl_{prefix}_{start}_{i}", use_container_width=True)

    # Video previews - 3 per row
    st.markdown("##### Apercu des variations")
    for start in range(0, len(analyses), 3):
        chunk = analyses[start:start+3]
        pcols = st.columns(3)
        for i, a in enumerate(chunk):
            p = a.get('output_path', '')
            if p and os.path.exists(p):
                with pcols[i]:
                    st.video(p)
                    u = a['uniqueness']
                    badge = get_badge(u)
                    st.markdown(f'<div style="text-align:center;margin-top:-6px"><span class="rg-name">{a["name"]}</span> <span class="{badge}" style="font-size:.72rem;padding:2px 8px">{u}%</span></div>', unsafe_allow_html=True)


# ============ MAIN ============

def main():
    st.markdown("""<div class="header-bar">
        <span class="header-logo">LTP</span>
        <span class="header-title">TikFusion</span>
    </div>""", unsafe_allow_html=True)

    tab_single, tab_bulk, tab_stats, tab_config = st.tabs([
        "Single", "Bulk", "Stats", "Config"
    ])

    # ===== CONFIG =====
    with tab_config:
        st.markdown("### Configuration")
        c1, c2 = st.columns(2)
        with c1: output_dir = st.text_input("Dossier de sortie", value="outputs", key="cfg_output")
        with c2: intensity = st.select_slider("Intensite", options=["low","medium","high"], value="medium", key="cfg_intensity")

        st.markdown("---")
        st.markdown("### Modifications anti-detection")

        st.markdown("#### Anti Hash Visuel")
        v1, v2 = st.columns(2)
        with v1:
            mod_noise = st.toggle("Pixel Noise", value=True, key="mod_noise", help="Bruit invisible. Le plus efficace contre pHash.")
            mod_zoom = st.toggle("Zoom", value=True, key="mod_zoom", help="Zoom leger. Repositionne les pixels.")
        with v2:
            mod_gamma = st.toggle("Gamma", value=True, key="mod_gamma", help="Modifie la luminosite globale.")
            mod_hue = st.toggle("Couleur", value=True, key="mod_hue", help="Decale la teinte.")

        st.markdown("#### Anti Deep Learning")
        s1, s2 = st.columns(2)
        with s1:
            mod_hflip = st.toggle("Miroir", value=True, key="mod_hflip", help="Inverse horizontalement.")
            mod_crop = st.toggle("Crop", value=True, key="mod_crop", help="Coupe les bords.")
        with s2:
            mod_speed = st.toggle("Vitesse", value=True, key="mod_speed", help="Change la vitesse.")

        st.markdown("#### Anti Fingerprint Audio")
        a1, a2 = st.columns(2)
        with a1: mod_pitch = st.toggle("Pitch", value=True, key="mod_pitch", help="Decale la frequence audio.")
        with a2: mod_fps = st.toggle("FPS", value=True, key="mod_fps", help="Change le framerate.")

        st.markdown("#### Metadata")
        mod_meta = st.toggle("Metadata aleatoires", value=True, key="mod_meta", help="Randomise les metadonnees.")

        st.markdown("---")
        ps = 0
        d = []
        if mod_noise: ps += 14; d.append("+14 noise")
        if mod_zoom: ps += 12; d.append("+12 zoom")
        if mod_gamma: ps += 4; d.append("+4 gamma")
        if mod_hue: ps += 1; d.append("+1 hue")
        if mod_hflip: ps += 5; d.append("+5 flip")
        if mod_crop: ps += 2; d.append("+2 crop")
        if mod_speed: ps += 1; d.append("+1 speed")
        if mod_pitch: ps += 17; d.append("+17 pitch")
        if mod_fps: ps += 3; d.append("+3 fps")
        ps += 3; d.append("+3 vol")
        if mod_meta: ps += 5; d.append("+5 meta")
        ps += 8; d.append("+8 encode")
        ps = min(ps, 100)
        bc = get_badge(ps)
        st.markdown(f"""<div style="background:#1C1C1E;border:1px solid #2C2C2E;border-radius:12px;padding:14px;margin:8px 0">
            <div style="display:flex;align-items:center;justify-content:space-between">
                <span style="font-size:1rem;font-weight:600;color:#F5F5F7">Score estime moyen</span>
                <span class="{bc}" style="font-size:1.1rem;padding:5px 14px">{ps}%</span>
            </div>
            <div style="color:#86868B;font-size:.72rem;margin-top:6px">{" | ".join(d)}</div>
        </div>""", unsafe_allow_html=True)

    # Read config values
    output_dir = st.session_state.get('cfg_output', 'outputs')
    intensity = st.session_state.get('cfg_intensity', 'medium')
    enabled_mods = {k: st.session_state.get(f"mod_{k}", True)
                    for k in ["noise","zoom","gamma","hue","hflip","crop","speed","pitch","fps","meta"]}

    # ===== SINGLE =====
    with tab_single:
        col_l, col_r = st.columns([1, 3])

        with col_l:
            uploaded = st.file_uploader("Video source", type=['mp4','mov','avi'], key="single_file")

            if uploaded:
                if 'single_temp' not in st.session_state:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                    tmp.write(uploaded.read()); tmp.close()
                    st.session_state['single_temp'] = tmp.name
                    uploaded.seek(0)

                st.markdown('<div class="compact-video">', unsafe_allow_html=True)
                st.video(uploaded)
                st.markdown('</div>', unsafe_allow_html=True)

                nv = st.slider("Variations", 1, 15, 5, key="single_vars")
                if st.button("Generer", type="primary", key="single_gen", use_container_width=True):
                    tp = st.session_state.get('single_temp')
                    if not tp or not os.path.exists(tp):
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        tmp.write(uploaded.read()); tmp.close()
                        tp = tmp.name

                    prog = st.progress(0); stat = st.empty()
                    analyses, folder = run_generation(tp, nv, output_dir, intensity, enabled_mods, prog, stat)
                    if analyses:
                        st.session_state['single_analyses'] = analyses
                        st.session_state['single_folder'] = folder
                    stat.empty(); prog.empty()
                    if analyses:
                        st.success(f"{len(analyses)} variations generees")
            else:
                if 'single_temp' in st.session_state:
                    try: os.unlink(st.session_state['single_temp'])
                    except: pass
                    del st.session_state['single_temp']

        with col_r:
            if 'single_analyses' in st.session_state:
                render_results(st.session_state['single_analyses'],
                               st.session_state.get('single_folder', ''), "single")

    # ===== BULK =====
    with tab_bulk:
        col_l, col_r = st.columns([1, 3])

        with col_l:
            files = st.file_uploader("Plusieurs videos", type=['mp4','mov','avi'],
                                     accept_multiple_files=True, key="bulk_files")
            if files:
                if len(files) > 10:
                    st.warning("Max 10 videos.")
                    files = files[:10]
                st.success(f"{len(files)} videos selectionnees")
                for f in files[:3]: st.caption(f"{f.name}")
                if len(files) > 3: st.caption(f"... +{len(files)-3} autres")

                vpv = st.slider("Variations / video", 1, 10, 3, key="bulk_vars")
                st.info(f"**{len(files) * vpv} videos** au total")

                if st.button("Lancer", type="primary", key="bulk_gen", use_container_width=True):
                    bf = get_dated_folder() + " BULK"
                    bp = os.path.join(output_dir, bf)
                    os.makedirs(bp, exist_ok=True)
                    prog = st.progress(0); stat = st.empty()
                    all_res = []
                    for vi, uf in enumerate(files):
                        vname = Path(uf.name).stem
                        stat.text(f"[{vi+1}/{len(files)}] {vname}")
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        tmp.write(uf.read()); tmp.close()

                        vfolder = os.path.join(bp, vname)
                        os.makedirs(vfolder, exist_ok=True)
                        vr = {'name': vname, 'variations': [], 'success_count': 0}

                        for j in range(vpv):
                            op = os.path.join(vfolder, f"V{j+1:02d}.mp4")
                            r = uniquify_video_ffmpeg(tmp.name, op, intensity, enabled_mods)
                            if r["success"]:
                                mods = r.get("modifications", {})
                                u = estimate_uniqueness(mods)
                                vr['variations'].append({
                                    'name': f"V{j+1:02d}", 'output_path': op,
                                    'uniqueness': u, 'modifications': mods,
                                    'thumbnail': extract_thumbnail(op)
                                })
                                vr['success_count'] += 1

                        all_res.append(vr)
                        os.unlink(tmp.name)
                        prog.progress((vi+1)/len(files))

                    st.session_state['bulk_results'] = all_res
                    st.session_state['bulk_folder'] = bf
                    stat.empty()
                    total = sum(r['success_count'] for r in all_res)
                    if total:
                        st.success(f"{total} videos generees")
                    else:
                        st.error("0 variations. FFmpeg a echoue.")

        with col_r:
            if 'bulk_results' in st.session_state:
                results = st.session_state['bulk_results']
                bf = st.session_state.get('bulk_folder', '')

                allv = [v for r in results for v in r['variations']]
                total = len(allv)
                avg = sum(v['uniqueness'] for v in allv) / len(allv) if allv else 0
                safe = sum(1 for v in allv if v['uniqueness'] >= 60)

                m1, m2, m3 = st.columns(3)
                m1.metric("Total", total)
                m2.metric("Moy.", f"{avg:.0f}%")
                m3.metric("Safe IG", f"{safe}/{total}")

                # ZIP all
                b1, b2 = st.columns(2)
                with b1:
                    buf = io.BytesIO()
                    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for r in results:
                            for v in r['variations']:
                                p = v.get('output_path', '')
                                if p and os.path.exists(p):
                                    zf.write(p, f"{r['name']}/{v['name']}.mp4")
                    buf.seek(0)
                    st.download_button("ZIP Tout", buf.getvalue(),
                                       file_name=f"{bf}.zip", mime="application/zip",
                                       key="zip_bulk", use_container_width=True)
                with b2:
                    safe_vids = [v for r in results for v in r['variations'] if v['uniqueness'] >= 60]
                    if safe_vids:
                        buf2 = io.BytesIO()
                        with zipfile.ZipFile(buf2, 'w', zipfile.ZIP_DEFLATED) as zf:
                            for r in results:
                                for v in r['variations']:
                                    if v['uniqueness'] >= 60:
                                        p = v.get('output_path', '')
                                        if p and os.path.exists(p):
                                            zf.write(p, f"{r['name']}/{v['name']}.mp4")
                        buf2.seek(0)
                        st.download_button(f"ZIP Safe IG ({len(safe_vids)})", buf2.getvalue(),
                                           file_name=f"{bf}_safe.zip", mime="application/zip",
                                           key="zip_safe_bulk", use_container_width=True)

                st.markdown("""<div class="legend">Safe IG = score >= 60%</div>""", unsafe_allow_html=True)

                for r in results:
                    with st.expander(f"{r['name']} - {r['success_count']} variations", expanded=True):
                        grid = '<table class="rg-table"><tr class="rg-head"><td style="width:36px">#</td><td>Modifications</td><td style="width:56px">Score</td><td style="width:90px">Apercu</td></tr>'
                        for v in r['variations']:
                            u = v['uniqueness']
                            badge = get_badge(u)
                            tags = format_tags(v.get('modifications', {}))
                            t_img = '<span style="color:#48484A;font-size:.7rem">-</span>'
                            t = v.get('thumbnail')
                            if t and os.path.exists(t):
                                b = thumb_b64(t)
                                if b: t_img = f'<img src="data:image/jpeg;base64,{b}" class="rg-thumb" />'
                            grid += f"""<tr class="rg-row">
                                <td><span class="rg-name">{v['name']}</span></td>
                                <td><span class="rg-tags">{tags}</span></td>
                                <td class="rg-score"><span class="{badge}">{u}%</span></td>
                                <td style="text-align:center">{t_img}</td>
                            </tr>\n"""
                        grid += '</table>'
                        st.markdown(grid, unsafe_allow_html=True)

                        cols = st.columns(min(5, max(1, len(r['variations']))))
                        for i, v in enumerate(r['variations']):
                            p = v.get('output_path', '')
                            if p and os.path.exists(p):
                                with cols[i % 5]:
                                    with open(p, 'rb') as f:
                                        st.download_button(f"{v['name']}", f.read(),
                                            file_name=f"{r['name']}_{v['name']}.mp4",
                                            mime="video/mp4", key=f"dlb_{r['name']}_{v['name']}",
                                            use_container_width=True)

                        pcols = st.columns(min(3, max(1, len(r['variations']))))
                        for i, v in enumerate(r['variations']):
                            p = v.get('output_path', '')
                            if p and os.path.exists(p):
                                with pcols[i % 3]:
                                    st.video(p)
            else:
                st.info("Upload plusieurs videos et lance le traitement")

    # ===== STATS =====
    with tab_stats:
        st.markdown("### Statistiques")
        if os.path.exists(output_dir):
            vids = list(Path(output_dir).rglob("*.mp4"))
            folders = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]
            sz = sum(f.stat().st_size for f in vids) / (1024*1024)
            c1, c2, c3 = st.columns(3)
            c1.metric("Sessions", len(folders))
            c2.metric("Videos", len(vids))
            c3.metric("Espace", f"{sz:.1f} MB")
            st.markdown("---")
            for f in sorted(folders, reverse=True):
                n = len(list(Path(os.path.join(output_dir, f)).rglob("*.mp4")))
                st.text(f"  {f} - {n} videos")
        else:
            st.info("Aucune session. Genere des variations pour commencer.")


if __name__ == "__main__":
    main()
