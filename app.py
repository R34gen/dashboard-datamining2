"""Jalankan dashboard HTML statis yang sama melalui Streamlit Community Cloud.

Halaman `index.html` menjadi satu sumber tampilan untuk GitHub Pages dan
Streamlit. Pustaka dan dataset JS/CSS digabung ke HTML agar berfungsi di dalam
iframe Streamlit (srcdoc) tanpa URL aset relatif yang rusak.
"""

from pathlib import Path
import re

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Dashboard Pendidikan Jawa Timur",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def bangun_html_dashboard() -> str:
    """Bangun HTML mandiri dari file repositori yang sama dengan GitHub Pages."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    def gabungkan_css(match: re.Match) -> str:
        relative_path = match.group(1)
        css = (ROOT / relative_path).read_text(encoding="utf-8")
        return "<style>\n" + css + "\n</style>"

    def gabungkan_js(match: re.Match) -> str:
        relative_path = match.group(1)
        js = (ROOT / relative_path).read_text(encoding="utf-8")
        # Hindari HTML parser menutup tag <script> saat menemukan teks
        # </script> yang merupakan bagian dari string template peta.
        js = re.sub(r"</script", r"<\/script", js, flags=re.IGNORECASE)
        return "<script>\n" + js + "\n</script>"

    # Masukkan CSS/JS lokal agar URL relatif tidak gagal di srcdoc iframe.
    html, n_css = re.subn(
        r'<link\s+href="(assets/css/[^\"]+\.css)"\s+rel="stylesheet"\s*/?>',
        gabungkan_css,
        html,
    )
    html, n_js = re.subn(
        r'<script\s+src="(assets/js/[^\"]+\.js)"\s*>\s*</script>',
        gabungkan_js,
        html,
    )
    if n_css != 1 or n_js != 6:
        raise RuntimeError(
            f"File HTML tidak sesuai struktur aset: CSS={n_css}; JS={n_js}."
        )
    return html


st.markdown(
    """
    <style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: #f3f6fa; }
    [data-testid="stElementContainer"] { width: 100%; }
    [data-testid="stIFrame"] { width: 100%; border: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    html_dashboard = bangun_html_dashboard()
except (OSError, RuntimeError) as exc:
    st.error(f"Gagal memuat berkas dashboard: {exc}")
    st.stop()

# Konten dashboard mempunyai navigasi, grafik, dan tabel internal yang dapat
# berganti tinggi. scrolling=True menjaga seluruh konten tetap dapat dibuka.
components.html(html_dashboard, height=1550, scrolling=True)
