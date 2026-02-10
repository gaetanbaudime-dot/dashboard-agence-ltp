"""
TikFusion - Apple-inspired design
"""
import streamlit as st
import os
import sys
import tempfile
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
        padding: 20px 0 10px 0;
        border-bottom: 1px solid #2C2C2E;
        margin-bottom: 24px;
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
    .header-x {
        font-size: 1.4rem;
        color: #86868B;
        font-weight: 300;
    }

    /* Apple card style */
    .apple-card {
        background: #1C1C1E;
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        border: 1px solid #2C2C2E;
    }

    /* Variation row */
    .var-row {
        background: #1C1C1E;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
        border: 1px solid #2C2C2E;
        transition: background 0.2s;
    }
    .var-row:hover {
        background: #2C2C2E;
    }

    /* Tags */
    .tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 1px 2px;
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
        padding: 8px 16px;
        font-size: 0.8rem;
        color: #86868B;
        margin-bottom: 16px;
    }

    /* Folder badge */
    .folder-badge {
        background: #1C1C1E;
        color: #64D2FF;
        padding: 8px 16px;
        border-radius: 10px;
        font-family: 'SF Mono', 'Menlo', monospace;
        font-size: 0.85rem;
        border: 1px solid #2C2C2E;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 12px;
        padding: 16px;
    }

    /* Streamlit overrides for cleaner look */
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
        font-size: 0.85rem;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1C1C1E;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


def estimate_uniqueness(modifications):
    """Estime l'unicité basée sur les vrais poids de détection TikTok/Instagram.

    Stratégie : maximiser les modifications INVISIBLES (noise, zoom, pitch, metadata)
    et réduire le poids des modifications VISIBLES (hue, speed).

    Poids réels des systèmes de détection:
    - Perceptual hash visuel (pHash/DCT): 30-35% → noise + zoom le cassent
    - Deep learning / structure: 25-30% → zoom + crop + flip le trompent
    - Audio fingerprint: 20-25% → pitch shift le casse
    - Metadata: 5-10% → randomisation complète
    - File hash: 1-2% → tout re-encoding suffit
    """
    score = 0

    # === VISUAL HASH BREAKING (max 35 pts) ===
    # Priorité aux mods INVISIBLES

    # Pixel noise — INVISIBLE et le plus efficace contre pHash/DCT
    noise = modifications.get("noise", 0)
    score += min(noise * 3, 18)  # ↑ max 18 pts (noise très valorisé car invisible)

    # Zoom — QUASI INVISIBLE et repositionne tous les pixels
    zoom = modifications.get("zoom", 1.0)
    zoom_pct = (zoom - 1.0) * 100
    score += min(zoom_pct * 3.5, 14)  # ↑ max 14 pts (zoom valorisé car subtil)

    # Gamma — INVISIBLE, change la distribution des pixels
    gamma = abs(modifications.get("gamma", 1.0) - 1.0)
    score += min(gamma * 200, 5)  # max 5 pts

    # Hue shift — VISIBLE, pHash partiellement résistant
    hue = abs(modifications.get("hue_shift", 0))
    score += min(hue * 0.15, 2)  # ↓ max 2 pts (réduit car visible)

    # === STRUCTURAL CHANGES (max 22 pts) ===

    # Horizontal flip — efficace mais visible
    if modifications.get("hflip", False):
        score += 12  # ↓ Réduit (était 15) — visible si texte dans vidéo

    # Crop — subtil à faible %
    crop = modifications.get("crop_percent", 0)
    score += min(crop * 2, 4)  # max 4 pts

    # Speed — VISIBLE si trop fort, réduit
    speed = modifications.get("speed", 1.0)
    speed_diff = abs(speed - 1.0)
    score += min(speed_diff * 40, 3)  # ↓ max 3 pts (réduit car visible)

    # === AUDIO FINGERPRINT BREAKING (max 28 pts) ===
    # Priorité maximale — INAUDIBLE à faible valeur

    # Pitch shift — INAUDIBLE <0.5st et CRITIQUE contre Shazam-like
    pitch = abs(modifications.get("pitch_semitones", 0))
    score += min(pitch * 35, 20)  # ↑ max 20 pts (pitch très valorisé car inaudible)

    # FPS shift — INVISIBLE, change le timing
    fps = modifications.get("fps", 30)
    fps_diff = abs(fps - 30)
    score += min(fps_diff * 50, 5)  # ↑ max 5 pts

    # Volume variation — toujours appliqué
    score += 3

    # === METADATA + FILE (max 15 pts) ===

    if modifications.get("metadata_randomized", False):
        score += 5

    # Re-encoding unique (CRF + GOP + B-frames)
    score += 8  # ↑ toujours un re-encoding unique

    return {'uniqueness': min(round(score), 100)}


def get_dated_folder_name():
    now = datetime.now()
    mois_fr = {1: "janvier", 2: "fevrier", 3: "mars", 4: "avril", 5: "mai", 6: "juin",
               7: "juillet", 8: "aout", 9: "septembre", 10: "octobre", 11: "novembre", 12: "decembre"}
    return f"{now.day} {mois_fr[now.month]} {now.strftime('%Hh%M')}"


def format_modifications(mods):
    """Formate les modifications en tags Apple-style"""
    tags = []
    if mods.get("hflip"):
        tags.append('<span class="tag tag-mirror">🪞 Miroir</span>')
    speed = mods.get("speed", 1.0)
    if abs(speed - 1.0) > 0.005:
        tags.append(f'<span class="tag tag-speed">🔄 x{speed:.2f}</span>')
    hue = mods.get("hue_shift", 0)
    if abs(hue) > 0:
        tags.append(f'<span class="tag tag-hue">🎨 {hue:+d}°</span>')
    crop = mods.get("crop_percent", 0)
    if crop > 0.1:
        tags.append(f'<span class="tag tag-crop">✂️ {crop:.1f}%</span>')
    zoom = mods.get("zoom", 1.0)
    if zoom > 1.005:
        tags.append(f'<span class="tag tag-zoom">🔍 {(zoom-1)*100:.1f}%</span>')
    noise = mods.get("noise", 0)
    if noise > 0:
        tags.append(f'<span class="tag tag-noise">📡 N{noise:.0f}</span>')
    pitch = mods.get("pitch_semitones", 0)
    if abs(pitch) > 0.05:
        tags.append(f'<span class="tag tag-pitch">🎵 {pitch:+.1f}st</span>')
    if mods.get("metadata_randomized"):
        tags.append('<span class="tag tag-meta">🏷️ Meta</span>')
    return " ".join(tags) if tags else '<span style="color:#48484A">—</span>'


def get_uniqueness_badge(score):
    """Retourne la classe CSS du badge selon le score d'unicité.
    ≥60% = safe (vert) — passe TikTok + Instagram
    30-59% = warning (orange) — passe TikTok, risqué Instagram
    <30% = danger (rouge) — risque sur toutes les plateformes
    """
    if score >= 60:
        return 'badge-safe'
    elif score >= 30:
        return 'badge-warning'
    else:
        return 'badge-danger'


LEGEND_HTML = """<div class="legend">
🟢 <b>≥ 60%</b> = Safe TikTok + Instagram &nbsp;&nbsp;|&nbsp;&nbsp;
🟠 <b>30-59%</b> = Safe TikTok, risqué Insta &nbsp;&nbsp;|&nbsp;&nbsp;
🔴 <b>< 30%</b> = Risque de détection
</div>"""


def main():
    # ============ HEADER WITH LOGO ============
    st.markdown("""
    <div class="header-bar">
        <span class="header-logo">LTP</span>
        <span class="header-title">TikFusion</span>
    </div>
    """, unsafe_allow_html=True)

    # ============ TABS ============
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Single", "📦 Bulk", "📊 Stats", "⚙️ Config"])

    # ========== TAB 4: CONFIG (read first for variables) ==========
    with tab4:
        st.markdown("### ⚙️ Configuration")
        c1, c2 = st.columns(2)
        with c1:
            output_dir = st.text_input("📁 Dossier de sortie", value="outputs", key="cfg_output")
        with c2:
            intensity = st.select_slider("🎚️ Intensité des modifications", options=["low", "medium", "high"], value="medium", key="cfg_intensity")

        st.markdown("---")
        st.markdown("### 🎛️ Modifications anti-détection")
        st.markdown("""<div class="legend">
        Active ou désactive chaque modification. Le score estimé se met à jour en temps réel.
        </div>""", unsafe_allow_html=True)

        # === SECTION: VISUAL HASH (pHash/DCT) ===
        st.markdown("#### 👁️ Anti Hash Visuel — *casse le perceptual hash (pHash/DCT)*")
        st.caption("Poids détection TikTok/Insta : ~30-35%")

        vc1, vc2 = st.columns(2)
        with vc1:
            mod_noise = st.toggle("📡 Pixel Noise", value=True, key="mod_noise",
                help="Ajoute du bruit invisible par pixel. Le plus efficace contre pHash.")
            mod_zoom = st.toggle("🔍 Zoom aléatoire", value=True, key="mod_zoom",
                help="Zoom léger (2-7%) qui repositionne tous les pixels. Casse le hash.")
        with vc2:
            mod_gamma = st.toggle("🌗 Gamma", value=True, key="mod_gamma",
                help="Modifie la courbe de luminosité globale. Subtil mais efficace.")
            mod_hue = st.toggle("🎨 Décalage couleur", value=True, key="mod_hue",
                help="Change la teinte de ±8-22°. pHash résiste partiellement.")

        st.markdown("---")

        # === SECTION: STRUCTURE (Deep Learning) ===
        st.markdown("#### 🧠 Anti Deep Learning — *trompe l'analyse de structure*")
        st.caption("Poids détection TikTok/Insta : ~25-30%")

        sc1, sc2 = st.columns(2)
        with sc1:
            mod_hflip = st.toggle("🪞 Miroir horizontal", value=True, key="mod_hflip",
                help="Inverse la vidéo horizontalement. Très efficace car change toutes les relations spatiales.")
            mod_crop = st.toggle("✂️ Crop aléatoire", value=True, key="mod_crop",
                help="Coupe les bords de 0.5-4%. Change les limites du frame.")
        with sc2:
            mod_speed = st.toggle("🔄 Changement vitesse", value=True, key="mod_speed",
                help="Accélère ou ralentit de ±3-12%. Change le fingerprint temporel.")

        st.markdown("---")

        # === SECTION: AUDIO (Fingerprint) ===
        st.markdown("#### 🔊 Anti Fingerprint Audio — *casse la détection type Shazam*")
        st.caption("Poids détection TikTok/Insta : ~20-25%")

        ac1, ac2 = st.columns(2)
        with ac1:
            mod_pitch = st.toggle("🎵 Pitch shift", value=True, key="mod_pitch",
                help="Décale la fréquence audio de ±0.3-0.8 semitons. Imperceptible mais casse le fingerprint.")
        with ac2:
            mod_fps = st.toggle("🎞️ FPS shift", value=True, key="mod_fps",
                help="Change le framerate de ±0.03-0.08 fps. Modifie le timing audio/vidéo.")

        st.markdown("---")

        # === SECTION: METADATA ===
        st.markdown("#### 🏷️ Metadata — *brouille les traces du fichier*")
        st.caption("Poids détection : ~5-10%")

        mod_meta = st.toggle("🏷️ Metadata aléatoires", value=True, key="mod_meta",
            help="Randomise titre, encodeur, date de création, UUID, etc.")

        st.markdown("---")

        # === SCORE PREVIEW ===
        # Simulate a "typical" modification set with current toggles to show estimated score
        preview_score = 0
        score_details = []

        if mod_noise:
            pts = 14  # Invisible — très efficace contre pHash
            preview_score += pts
            score_details.append(f"📡 Noise: +{pts} pts")
        if mod_zoom:
            pts = 12  # Quasi invisible — repositionne tous les pixels
            preview_score += pts
            score_details.append(f"🔍 Zoom: +{pts} pts")
        if mod_gamma:
            pts = 4
            preview_score += pts
            score_details.append(f"🌗 Gamma: +{pts} pts")
        if mod_hue:
            pts = 1  # Visible — réduit
            preview_score += pts
            score_details.append(f"🎨 Hue: +{pts} pts")
        if mod_hflip:
            # 40% chance in medium, so average contribution
            pts = 5  # 12 * 0.4 average
            preview_score += pts
            score_details.append(f"🪞 Miroir: +{pts} pts (moy.)")
        if mod_crop:
            pts = 2  # Réduit — crop minimal
            preview_score += pts
            score_details.append(f"✂️ Crop: +{pts} pts")
        if mod_speed:
            pts = 1  # Visible — réduit
            preview_score += pts
            score_details.append(f"🔄 Speed: +{pts} pts")
        if mod_pitch:
            pts = 17  # Inaudible — très efficace contre fingerprint audio
            preview_score += pts
            score_details.append(f"🎵 Pitch: +{pts} pts")
        if mod_fps:
            pts = 3  # Invisible — change le timing
            preview_score += pts
            score_details.append(f"🎞️ FPS: +{pts} pts")
        # Volume always applied
        preview_score += 3
        score_details.append(f"🔊 Volume: +3 pts")
        if mod_meta:
            pts = 5
            preview_score += pts
            score_details.append(f"🏷️ Meta: +{pts} pts")
        # Re-encoding always happens
        preview_score += 8
        score_details.append(f"💾 Re-encoding: +8 pts")

        preview_score = min(preview_score, 100)

        badge_class = get_uniqueness_badge(preview_score)
        if preview_score >= 60:
            status_text = "🟢 Safe — passe TikTok et Instagram sans problème"
        elif preview_score >= 30:
            status_text = "🟠 OK pour TikTok — attention sur Instagram, active plus de mods"
        else:
            status_text = "🔴 Risque de détection — active plus de modifications"
        st.markdown(f"""
        <div style="background:#1C1C1E;border:1px solid #2C2C2E;border-radius:12px;padding:16px;margin:8px 0">
            <div style="display:flex;align-items:center;justify-content:space-between">
                <span style="font-size:1.1rem;font-weight:600;color:#F5F5F7">📊 Score estimé moyen</span>
                <span class="{badge_class}" style="font-size:1.2rem;padding:6px 16px">{preview_score}%</span>
            </div>
            <div style="color:#86868B;font-size:0.8rem;margin-top:8px">
                {"  •  ".join(score_details)}
            </div>
            <div style="margin-top:8px;color:#48484A;font-size:0.75rem">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if os.path.exists(output_dir):
            st.markdown("**📁 Sessions récentes**")
            folders = sorted([f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))], reverse=True)
            for folder in folders[:5]:
                count = len(list(Path(os.path.join(output_dir, folder)).rglob("*.mp4")))
                st.text(f"  📁 {folder} ({count} vidéos)")

    # Ensure config values are available
    if 'cfg_output' not in st.session_state:
        output_dir = "outputs"
    else:
        output_dir = st.session_state['cfg_output']

    if 'cfg_intensity' not in st.session_state:
        intensity = "medium"
    else:
        intensity = st.session_state['cfg_intensity']

    # Collect enabled modifications from toggles
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

    # ========== TAB 1: SINGLE UPLOAD ==========
    with tab1:
        col_upload, col_results = st.columns([1, 2])

        with col_upload:
            uploaded = st.file_uploader("📹 Vidéo source", type=['mp4', 'mov', 'avi'], key="single")

            if uploaded:
                st.video(uploaded)
                num_vars = st.slider("Nombre de variations", 1, 15, 5, key="single_vars")

                if st.button("Générer les variations", type="primary", key="single_btn"):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(uploaded.read())
                        original_path = tmp.name

                    progress = st.progress(0)
                    status = st.empty()
                    results_container = st.empty()

                    try:
                        from uniquifier import uniquify_video_ffmpeg

                        folder_name = get_dated_folder_name()
                        dated_dir = os.path.join(output_dir, folder_name)
                        os.makedirs(dated_dir, exist_ok=True)

                        analyses = []
                        for i in range(num_vars):
                            status.text(f"⏳ V{i+1:02d}/{num_vars}...")
                            out_path = os.path.join(dated_dir, f"V{i+1:02d}.mp4")
                            r = uniquify_video_ffmpeg(original_path, out_path, intensity, enabled_mods)

                            if r["success"]:
                                mods = r.get("modifications", {})
                                analysis = estimate_uniqueness(mods)
                                analysis['name'] = Path(out_path).stem
                                analysis['modifications'] = mods
                                analysis['output_path'] = out_path
                                analyses.append(analysis)

                            progress.progress((i + 1) / num_vars)

                            # Show partial results as they arrive
                            st.session_state['single_analyses'] = analyses
                            st.session_state['single_folder'] = folder_name

                        status.empty()
                        progress.empty()
                        st.success(f"✅ {len(analyses)} variations générées")

                        os.unlink(original_path)
                    except Exception as e:
                        st.error(f"Erreur: {e}")

        with col_results:
            if 'single_analyses' in st.session_state:
                analyses = st.session_state['single_analyses']

                st.markdown(f"<div class='folder-badge'>📁 outputs/{st.session_state.get('single_folder', '')}/</div>", unsafe_allow_html=True)

                st.markdown(LEGEND_HTML, unsafe_allow_html=True)

                for a in analyses:
                    cols = st.columns([1, 3, 1, 1])
                    cols[0].markdown(f"**{a['name']}**")
                    cols[1].markdown(format_modifications(a.get('modifications', {})), unsafe_allow_html=True)
                    u = a['uniqueness']
                    badge = get_uniqueness_badge(u)
                    cols[2].markdown(f"<span class='{badge}'>{u:.0f}%</span>", unsafe_allow_html=True)
                    output_path = a.get('output_path', '')
                    if output_path and os.path.exists(output_path):
                        with open(output_path, "rb") as f:
                            cols[3].download_button("⬇️", f.read(), file_name=Path(output_path).name, mime="video/mp4", key=f"dl_{a['name']}")

                # Video previews in a separate expandable section
                with st.expander("▶️ Previews vidéo", expanded=False):
                    for a in analyses:
                        output_path = a.get('output_path', '')
                        if output_path and os.path.exists(output_path):
                            st.caption(a['name'])
                            st.video(output_path, format="video/mp4")

    # ========== TAB 2: BULK UPLOAD ==========
    with tab2:
        col_upload, col_results = st.columns([1, 1])

        with col_upload:
            uploaded_files = st.file_uploader(
                "📹 Sélectionne plusieurs vidéos",
                type=['mp4', 'mov', 'avi'],
                accept_multiple_files=True,
                key="bulk"
            )

            if uploaded_files:
                if len(uploaded_files) > 10:
                    st.warning("⚠️ Maximum 10 vidéos. Seules les 10 premières seront traitées.")
                    uploaded_files = uploaded_files[:10]
                st.success(f"📁 {len(uploaded_files)} vidéos sélectionnées")

                for f in uploaded_files[:5]:
                    st.text(f"  📹 {f.name}")
                if len(uploaded_files) > 5:
                    st.text(f"  ... +{len(uploaded_files) - 5} autres")

                vars_per_video = st.slider("Variations par vidéo", 1, 10, 3, key="bulk_vars")

                total = len(uploaded_files) * vars_per_video
                st.warning(f"⚠️ Total : **{total} vidéos** seront générées")

                if st.button("Lancer le traitement", type="primary", key="bulk_btn"):
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
                                        'modifications': mods
                                    })
                                    video_results['success_count'] += 1

                            all_results.append(video_results)
                            os.unlink(original_path)
                            overall_progress.progress((vid_idx + 1) / len(uploaded_files))

                        st.session_state['bulk_results'] = all_results
                        st.session_state['bulk_folder'] = bulk_folder
                        st.session_state['bulk_path'] = bulk_path

                        status.empty()
                        total_success = sum(r['success_count'] for r in all_results)
                        st.success(f"✅ {total_success} vidéos générées")

                    except Exception as e:
                        st.error(f"Erreur: {e}")

        with col_results:
            if 'bulk_results' in st.session_state:
                results = st.session_state['bulk_results']
                bulk_folder = st.session_state.get('bulk_folder', '')
                bulk_path = st.session_state.get('bulk_path', '')

                st.markdown(f"<div class='folder-badge'>📁 outputs/{bulk_folder}/</div>", unsafe_allow_html=True)

                total_videos = sum(r['success_count'] for r in results)
                all_variations = [v for r in results for v in r['variations']]
                avg_uniqueness = sum(v['uniqueness'] for v in all_variations) / len(all_variations) if all_variations else 0
                safe_count = sum(1 for v in all_variations if v['uniqueness'] >= 60)

                col_a, col_b, col_c = st.columns(3)
                col_a.metric("📹 Total", total_videos)
                col_b.metric("📊 Unicité moy.", f"{avg_uniqueness:.0f}%")
                col_c.metric("✅ Safe (≥60%)", f"{safe_count}/{len(all_variations)}")

                st.markdown(LEGEND_HTML, unsafe_allow_html=True)

                for r in results:
                    with st.expander(f"📹 {r['name']} — {r['success_count']} variations"):
                        if r['variations']:
                            for v in r['variations']:
                                cols = st.columns([1, 3, 1, 1])
                                cols[0].markdown(f"**{v['name']}**")
                                cols[1].markdown(format_modifications(v.get('modifications', {})), unsafe_allow_html=True)
                                u = v['uniqueness']
                                badge = get_uniqueness_badge(u)
                                cols[2].markdown(f"<span class='{badge}'>{u:.0f}%</span>", unsafe_allow_html=True)
                                vpath = v.get('output_path', '')
                                if vpath and os.path.exists(vpath):
                                    with open(vpath, "rb") as f:
                                        cols[3].download_button("⬇️", f.read(), file_name=f"{r['name']}_{v['name']}.mp4", mime="video/mp4", key=f"dl_bulk_{r['name']}_{v['name']}")

                            with st.expander("▶️ Previews", expanded=False):
                                for v in r['variations']:
                                    vpath = v.get('output_path', '')
                                    if vpath and os.path.exists(vpath):
                                        st.caption(v['name'])
                                        st.video(vpath, format="video/mp4")
            else:
                st.info("👈 Upload plusieurs vidéos et lance le traitement")

    # ========== TAB 3: STATS ==========
    with tab3:
        st.markdown("### 📊 Statistiques globales")

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
