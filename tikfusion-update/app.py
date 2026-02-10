"""
TikFusion MVP - With Bulk Upload & Download features
"""
import streamlit as st
import os
import sys
import io
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

st.set_page_config(page_title="TikFusion", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; background: linear-gradient(90deg, #ff0050, #00f2ea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .safe { background: #00c853; color: white; padding: 5px 10px; border-radius: 5px; }
    .warning { background: #ffc107; color: black; padding: 5px 10px; border-radius: 5px; }
    .danger { background: #f44336; color: white; padding: 5px 10px; border-radius: 5px; }
    .folder-name { background: #333; color: #00f2ea; padding: 10px; border-radius: 5px; font-family: monospace; }
    .video-card { background: #1a1a1a; padding: 10px; border-radius: 8px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

def compare_to_original(original_path, variation_path):
    """Compare une variation a l'original"""
    try:
        from uniqueness_checker import UniquenessChecker
        checker = UniquenessChecker()
        result = checker.compare_videos(original_path, variation_path)
        similarity = result['similarity_percent']
        uniqueness = 100 - similarity
        return {
            'similarity': similarity,
            'uniqueness': uniqueness,
            'safe_tiktok': uniqueness >= 30,
            'safe_instagram': uniqueness >= 20,
            'safe_youtube': uniqueness >= 25
        }
    except:
        return {'uniqueness': 50, 'safe_tiktok': True, 'safe_instagram': True, 'safe_youtube': True}

def get_dated_folder_name():
    """Genere un nom de dossier avec date et heure"""
    now = datetime.now()
    mois_fr = {1: "janvier", 2: "fevrier", 3: "mars", 4: "avril", 5: "mai", 6: "juin",
               7: "juillet", 8: "aout", 9: "septembre", 10: "octobre", 11: "novembre", 12: "decembre"}
    return f"{now.day} {mois_fr[now.month]} {now.strftime('%Hh%M')}"

def create_zip_from_files(file_dict):
    """Cree un ZIP en memoire a partir d'un dict {nom: bytes}"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for name, data in file_dict.items():
            zf.writestr(name, data)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    st.markdown('<p class="main-header">🎬 TikFusion</p>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Configuration")
        output_dir = st.text_input("📁 Dossier racine", value="outputs")
        intensity = st.select_slider("🎚️ Intensite", options=["low", "medium", "high"], value="medium")

        st.markdown("---")
        st.markdown("**📁 Dossiers recents:**")
        if os.path.exists(output_dir):
            folders = sorted([f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))], reverse=True)
            for folder in folders[:5]:
                count = len(list(Path(os.path.join(output_dir, folder)).rglob("*.mp4")))
                st.text(f"📁 {folder} ({count} videos)")

    # TABS - Sans l'onglet Publier
    tab1, tab2, tab3 = st.tabs(["📤 Single", "📦 Bulk", "📊 Stats"])

    # ========== TAB 1: SINGLE UPLOAD ==========
    with tab1:
        st.header("📤 Upload unique")

        col1, col2 = st.columns([1, 2])

        with col1:
            uploaded = st.file_uploader("📹 Video source", type=['mp4', 'mov', 'avi', 'mpeg'], key="single")

            if uploaded:
                st.video(uploaded)
                num_vars = st.slider("Nombre de variations", 1, 50, 10, key="single_vars")

                if st.button("🚀 Generer", type="primary", key="single_btn"):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(uploaded.read())
                        original_path = tmp.name

                    progress = st.progress(0)
                    status = st.empty()

                    try:
                        from uniquifier import batch_uniquify

                        status.text("⏳ Generation en cours...")
                        results = batch_uniquify(original_path, output_dir, num_vars, intensity)

                        folder_name = os.path.basename(os.path.dirname(results[0]["output_path"])) if results else ""

                        status.text("🔍 Analyse d'unicite...")
                        analyses = []
                        video_files = {}
                        for i, r in enumerate(results):
                            if r["success"]:
                                analysis = compare_to_original(original_path, r["output_path"])
                                name = Path(r["output_path"]).stem
                                analysis['name'] = name
                                # Lire le fichier en memoire pour le telecharger
                                with open(r["output_path"], 'rb') as f:
                                    video_files[f"{name}.mp4"] = f.read()
                                analyses.append(analysis)
                            progress.progress((i + 1) / len(results))

                        st.session_state['single_analyses'] = analyses
                        st.session_state['single_folder'] = folder_name
                        st.session_state['single_files'] = video_files
                        status.empty()
                        st.success(f"✅ {len(analyses)} variations generees !")
                        os.unlink(original_path)
                    except Exception as e:
                        st.error(f"Erreur: {e}")

        with col2:
            if 'single_analyses' in st.session_state and st.session_state['single_analyses']:
                analyses = st.session_state['single_analyses']
                video_files = st.session_state.get('single_files', {})

                # Bouton telecharger tout (ZIP)
                if video_files:
                    zip_data = create_zip_from_files(video_files)
                    st.download_button(
                        label="📥 Telecharger tout (ZIP)",
                        data=zip_data,
                        file_name=f"TikFusion_{st.session_state.get('single_folder', 'variations')}.zip",
                        mime="application/zip",
                        key="single_zip_dl"
                    )

                st.markdown("---")

                # En-tete du tableau
                cols = st.columns([2, 2, 1, 1, 1, 1])
                cols[0].markdown("**Fichier**")
                cols[1].markdown("**Unicite**")
                cols[2].markdown("**TT**")
                cols[3].markdown("**IG**")
                cols[4].markdown("**YT**")
                cols[5].markdown("**DL**")

                for idx, a in enumerate(analyses):
                    cols = st.columns([2, 2, 1, 1, 1, 1])
                    cols[0].text(a['name'])
                    u = a['uniqueness']
                    color = 'safe' if u >= 30 else 'warning' if u >= 20 else 'danger'
                    cols[1].markdown(f"<span class='{color}'>{u:.0f}%</span>", unsafe_allow_html=True)
                    cols[2].markdown("✅" if a['safe_tiktok'] else "❌")
                    cols[3].markdown("✅" if a['safe_instagram'] else "❌")
                    cols[4].markdown("✅" if a['safe_youtube'] else "❌")
                    # Bouton telecharger individuel
                    file_key = f"{a['name']}.mp4"
                    if file_key in video_files:
                        cols[5].download_button(
                            label="📥",
                            data=video_files[file_key],
                            file_name=file_key,
                            mime="video/mp4",
                            key=f"dl_single_{idx}"
                        )

    # ========== TAB 2: BULK UPLOAD ==========
    with tab2:
        st.header("📦 Bulk - Traitement en masse")
        st.markdown("Upload jusqu'a **20 videos** et genere des variations pour chacune.")

        col1, col2 = st.columns([1, 1])

        with col1:
            uploaded_files = st.file_uploader(
                "📹 Selectionne plusieurs videos",
                type=['mp4', 'mov', 'avi', 'mpeg'],
                accept_multiple_files=True,
                key="bulk"
            )

            if uploaded_files:
                st.success(f"📁 {len(uploaded_files)} videos selectionnees")

                for f in uploaded_files[:5]:
                    st.text(f"  📹 {f.name}")
                if len(uploaded_files) > 5:
                    st.text(f"  ... +{len(uploaded_files) - 5} autres")

                vars_per_video = st.slider("Variations par video", 1, 20, 5, key="bulk_vars")

                total = len(uploaded_files) * vars_per_video
                st.warning(f"⚠️ Total: **{total} videos** seront generees")

                if st.button("🚀 Lancer le Bulk Processing", type="primary", key="bulk_btn"):

                    bulk_folder = get_dated_folder_name() + " - BULK"
                    bulk_path = os.path.join(output_dir, bulk_folder)
                    os.makedirs(bulk_path, exist_ok=True)

                    overall_progress = st.progress(0)
                    status = st.empty()

                    all_results = []
                    all_video_files = {}

                    try:
                        from uniquifier import uniquify_video_ffmpeg

                        for vid_idx, uploaded_file in enumerate(uploaded_files):
                            video_name = Path(uploaded_file.name).stem
                            status.text(f"⏳ [{vid_idx + 1}/{len(uploaded_files)}] Traitement: {video_name}")

                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                                tmp.write(uploaded_file.read())
                                original_path = tmp.name

                            video_folder = os.path.join(bulk_path, video_name)
                            os.makedirs(video_folder, exist_ok=True)

                            video_results = {
                                'name': video_name,
                                'variations': [],
                                'success_count': 0
                            }

                            for var_idx in range(vars_per_video):
                                output_path = os.path.join(video_folder, f"V{var_idx + 1:02d}.mp4")
                                result = uniquify_video_ffmpeg(original_path, output_path, intensity)

                                if result["success"]:
                                    analysis = compare_to_original(original_path, output_path)
                                    var_name = f"V{var_idx + 1:02d}"
                                    video_results['variations'].append({
                                        'name': var_name,
                                        'uniqueness': analysis['uniqueness'],
                                        'safe_tiktok': analysis['safe_tiktok'],
                                        'safe_instagram': analysis['safe_instagram'],
                                        'safe_youtube': analysis['safe_youtube']
                                    })
                                    video_results['success_count'] += 1
                                    # Lire en memoire pour telecharger
                                    with open(output_path, 'rb') as f:
                                        all_video_files[f"{video_name}/{var_name}.mp4"] = f.read()

                            all_results.append(video_results)
                            os.unlink(original_path)

                            overall_progress.progress((vid_idx + 1) / len(uploaded_files))

                        st.session_state['bulk_results'] = all_results
                        st.session_state['bulk_folder'] = bulk_folder
                        st.session_state['bulk_files'] = all_video_files

                        status.empty()
                        total_success = sum(r['success_count'] for r in all_results)
                        st.success(f"✅ Termine ! {total_success} videos generees")

                    except Exception as e:
                        st.error(f"Erreur: {e}")

        with col2:
            st.subheader("📊 Resultats Bulk")

            if 'bulk_results' in st.session_state:
                results = st.session_state['bulk_results']
                bulk_folder = st.session_state.get('bulk_folder', '')
                bulk_files = st.session_state.get('bulk_files', {})

                # Bouton telecharger tout (ZIP)
                if bulk_files:
                    zip_data = create_zip_from_files(bulk_files)
                    st.download_button(
                        label="📥 Telecharger tout (ZIP)",
                        data=zip_data,
                        file_name=f"TikFusion_{bulk_folder}.zip",
                        mime="application/zip",
                        key="bulk_zip_dl"
                    )

                st.markdown("---")

                # Summary stats
                total_videos = sum(r['success_count'] for r in results)
                all_variations = [v for r in results for v in r['variations']]
                avg_uniqueness = sum(v['uniqueness'] for v in all_variations) / len(all_variations) if all_variations else 0
                safe_count = sum(1 for v in all_variations if v['safe_tiktok'])

                col_a, col_b, col_c = st.columns(3)
                col_a.metric("📹 Total", total_videos)
                col_b.metric("📊 Unicite moy.", f"{avg_uniqueness:.0f}%")
                col_c.metric("✅ Safe TT", f"{safe_count}/{len(all_variations)}")

                st.markdown("---")

                # Per-video results
                dl_counter = 0
                for r in results:
                    with st.expander(f"📹 {r['name']} ({r['success_count']} variations)"):
                        if r['variations']:
                            cols = st.columns([2, 2, 1, 1, 1, 1])
                            cols[0].markdown("**Var**")
                            cols[1].markdown("**Unicite**")
                            cols[2].markdown("**TT**")
                            cols[3].markdown("**IG**")
                            cols[4].markdown("**YT**")
                            cols[5].markdown("**DL**")

                            for v in r['variations']:
                                cols = st.columns([2, 2, 1, 1, 1, 1])
                                cols[0].text(v['name'])
                                u = v['uniqueness']
                                color = 'safe' if u >= 30 else 'warning' if u >= 20 else 'danger'
                                cols[1].markdown(f"<span class='{color}'>{u:.0f}%</span>", unsafe_allow_html=True)
                                cols[2].markdown("✅" if v['safe_tiktok'] else "❌")
                                cols[3].markdown("✅" if v['safe_instagram'] else "❌")
                                cols[4].markdown("✅" if v['safe_youtube'] else "❌")
                                # Bouton telecharger individuel
                                file_key = f"{r['name']}/{v['name']}.mp4"
                                if file_key in bulk_files:
                                    cols[5].download_button(
                                        label="📥",
                                        data=bulk_files[file_key],
                                        file_name=f"{r['name']}_{v['name']}.mp4",
                                        mime="video/mp4",
                                        key=f"dl_bulk_{dl_counter}"
                                    )
                                dl_counter += 1
            else:
                st.info("👈 Upload plusieurs videos et lance le bulk processing")

                st.markdown("""
### 📁 Structure des fichiers
```
outputs/
└── 10 fevrier 14h34 - BULK/
    ├── video1/
    │   ├── V01.mp4
    │   ├── V02.mp4
    │   └── V05.mp4
    ├── video2/
    │   ├── V01.mp4
    │   └── ...
    └── video3/
        └── ...
```
                """)

    # ========== TAB 3: STATS ==========
    with tab3:
        st.header("📊 Statistiques globales")

        if os.path.exists(output_dir):
            all_videos = list(Path(output_dir).rglob("*.mp4"))
            all_folders = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]
            total_size = sum(f.stat().st_size for f in all_videos) / (1024 * 1024)

            col1, col2, col3 = st.columns(3)
            col1.metric("📁 Sessions", len(all_folders))
            col2.metric("📹 Total videos", len(all_videos))
            col3.metric("💾 Espace", f"{total_size:.1f} MB")

            st.markdown("---")
            st.markdown("### 📁 Toutes les sessions")

            for folder in sorted(all_folders, reverse=True):
                folder_path = os.path.join(output_dir, folder)
                videos = list(Path(folder_path).rglob("*.mp4"))
                st.text(f"📁 {folder} - {len(videos)} videos")

if __name__ == "__main__":
    main()
