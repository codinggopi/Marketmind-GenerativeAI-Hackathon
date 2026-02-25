import streamlit as st
import requests
import re
import json
import base64
import os
import time
from urllib.parse import quote_plus
from io import BytesIO

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MarketAI Suite",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & Base ─────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0d0d1a;
    color: #e8e8f0;
}

/* Ensure Streamlit main area uses the same dark theme on all pages */
[data-testid="stAppViewContainer"],
.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 40%, #0d1a2e 100%) !important;
}
[data-testid="stMain"],
section.main {
    background: transparent !important;
}
[data-testid="stAppViewBlockContainer"] {
    background: transparent !important;
    padding-top: 0 !important;
}

/* ── Hide Streamlit chrome ───────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] > div { background: #12122a !important; }

/* ── Sidebar ──────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12122a 0%, #1a1a35 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.2);
}
[data-testid="stSidebar"] .stRadio label {
    color: #c4b5fd !important;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 10px 14px;
    border-radius: 10px;
    display: block;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(139,92,246,0.15);
    color: #fff !important;
}

/* ── Main wrapper ─────────────────────────── */
.main-wrapper {
    min-height: 100vh;
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 40%, #0d1a2e 100%);
    padding: 0;
}

/* ── Top nav bar ─────────────────────────── */
.topbar {
    background: rgba(18,18,42,0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(139,92,246,0.25);
    padding: 14px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.02em;
}
.topbar-brand .brand-icon {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    border-radius: 10px;
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.topbar-nav { display: flex; gap: 8px; }
.nav-pill {
    padding: 7px 18px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #a78bfa;
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.2);
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
}
.nav-pill-link {
    display: inline-block;
    text-decoration: none !important;
    color: #a78bfa !important;
}
.nav-pill-link:hover,
.nav-pill-link:focus,
.nav-pill-link:active,
.nav-pill-link:visited {
    text-decoration: none !important;
    color: #a78bfa !important;
}
.nav-pill-link.active { color: #fff !important; }
.nav-pill:hover, .nav-pill.active {
    background: rgba(139,92,246,0.3);
    color: #fff;
    border-color: rgba(139,92,246,0.5);
}

/* ── Hero ─────────────────────────────────── */
.hero {
    text-align: center;
    padding: 80px 40px 60px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(124,58,237,0.18) 0%, transparent 65%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.3);
    color: #c4b5fd;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 24px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 540px;
    margin: 0 auto 36px;
    line-height: 1.7;
}
.hero-cta {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: #fff;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 14px 32px;
    border-radius: 14px;
    border: none;
    cursor: pointer;
    box-shadow: 0 8px 32px rgba(124,58,237,0.4);
    transition: all 0.2s;
    text-decoration: none;
}
.hero-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(124,58,237,0.55);
}

/* ── Feature cards (home) ─────────────────── */
.cards-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    padding: 0 40px 50px;
    max-width: 1200px;
    margin: 0 auto;
}
.feature-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 20px;
    padding: 28px 24px;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}
.feature-card-link {
    display: block;
    text-decoration: none !important;
    color: inherit;
}
.feature-card-link:hover,
.feature-card-link:focus,
.feature-card-link:active,
.feature-card-link:visited {
    text-decoration: none !important;
}
.feature-card-link h3,
.feature-card-link h3:visited {
    color: #e2e8f0 !important;
}
.feature-card-link p,
.feature-card-link p:visited {
    color: #94a3b8 !important;
}
.feature-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(124,58,237,0.05) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
}
.feature-card:hover { transform: translateY(-4px); border-color: rgba(139,92,246,0.5); }
.feature-card:hover::before { opacity: 1; }
.card-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(79,70,229,0.25));
    border: 1px solid rgba(139,92,246,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 16px;
}
.feature-card h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 8px;
}
.feature-card p { font-size: 0.85rem; color: #6b7280; line-height: 1.6; }

/* ── Platforms section ───────────────────── */
.platforms-section {
    background: rgba(255,255,255,0.02);
    border-top: 1px solid rgba(139,92,246,0.15);
    border-bottom: 1px solid rgba(139,92,246,0.15);
    padding: 50px 40px;
    text-align: center;
    margin-bottom: 20px;
}
.platforms-section h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 30px;
}
.platforms-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    justify-content: center;
    max-width: 700px;
    margin: 0 auto;
}
.platform-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.2);
    padding: 10px 20px;
    border-radius: 12px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #c4b5fd;
    transition: all 0.2s;
}
.platform-chip:hover {
    background: rgba(139,92,246,0.15);
    border-color: rgba(139,92,246,0.45);
    transform: translateY(-2px);
}

/* ── Tool page wrapper ───────────────────── */
.tool-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 48px 40px;
    background: rgba(10, 10, 30, 0.45);
    border: 1px solid rgba(139,92,246,0.18);
    border-radius: 20px;
    backdrop-filter: blur(8px);
    margin-top: 18px;
}
.tool-header { margin-bottom: 32px; }
.tool-header h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: none;
    color: #c4b5fd;
    -webkit-text-fill-color: #c4b5fd;
    margin-bottom: 6px;
}
.tool-header p { color: #64748b; font-size: 0.9rem; }

/* ── Form card ────────────────────────────── */
.form-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 24px;
}
.form-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 6px;
    display: block;
}

/* ── Inputs ───────────────────────────────── */
[data-testid="stTextInput"] > div > div,
[data-testid="stTextArea"] > div > div,
[data-testid="stSelectbox"] > div > div,
[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="select"] {
    background: rgba(18, 18, 42, 0.82) !important;
    border: 1px solid rgba(139,92,246,0.28) !important;
    border-radius: 12px !important;
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select,
[data-baseweb="input"] input {
    background: transparent !important;
    border: none !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    -webkit-text-fill-color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-baseweb="input"] input:focus {
    outline: none !important;
}
[data-testid="stTextInput"] > div > div:focus-within,
[data-testid="stTextArea"] > div > div:focus-within,
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: rgba(139,92,246,0.62) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.16) !important;
}
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #7c3aed !important;
}

input::placeholder,
textarea::placeholder {
    color: #a9b9cf !important;
    font-size: 0.84rem !important;
    opacity: 0.7 !important;
}
input::-webkit-input-placeholder,
textarea::-webkit-input-placeholder {
    color: #a9b9cf !important;
    font-size: 0.84rem !important;
    opacity: 0.7 !important;
}
input::-moz-placeholder,
textarea::-moz-placeholder {
    color: #a9b9cf !important;
    font-size: 0.84rem !important;
    opacity: 0.7 !important;
}
input:-ms-input-placeholder,
textarea:-ms-input-placeholder {
    color: #a9b9cf !important;
    font-size: 0.84rem !important;
}

/* Selectbox selected value + caret */
[data-baseweb="select"] div,
[data-baseweb="select"] span,
[data-testid="stSelectbox"] [role="combobox"] {
    color: #f8fafc !important;
}

/* ── Buttons ──────────────────────────────── */
.stButton > button,
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    box-shadow: 0 6px 24px rgba(124,58,237,0.35) !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover,
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(124,58,237,0.5) !important;
}
.stButton > button[kind="secondary"],
[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid rgba(139,92,246,0.35) !important;
    color: #a78bfa !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover,
[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: rgba(139,92,246,0.1) !important;
    border-color: rgba(139,92,246,0.6) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
}

/* Captions and helper text contrast */
[data-testid="stCaptionContainer"] {
    color: #94a3b8 !important;
}

/* ── Result box ───────────────────────────── */
.result-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(139,92,246,0.25);
    border-left: 4px solid #7c3aed;
    border-radius: 16px;
    padding: 28px;
    margin-top: 24px;
    animation: fadeInUp 0.4s ease;
}
.result-box h4 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 16px;
}
.result-box pre, .result-box p {
    font-size: 0.9rem;
    line-height: 1.75;
    color: #e5e7eb !important;
    white-space: pre-wrap;
    word-break: break-word;
}
.result-box,
.result-box * {
    color: #e5e7eb !important;
}
.result-box h1, .result-box h2, .result-box h3, .result-box h5, .result-box h6,
.result-box strong, .result-box b, .result-box li, .result-box span, .result-box div {
    color: #e5e7eb !important;
}

/* ── Score badge ──────────────────────────── */
.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 90px; height: 90px;
    border-radius: 50%;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 auto 20px;
    border: 3px solid;
}
.score-hot { background: rgba(16,185,129,0.15); border-color: #10b981; color: #10b981; }
.score-warm { background: rgba(245,158,11,0.15); border-color: #f59e0b; color: #f59e0b; }
.score-lukewarm { background: rgba(59,130,246,0.15); border-color: #3b82f6; color: #3b82f6; }
.score-cold { background: rgba(239,68,68,0.15); border-color: #ef4444; color: #ef4444; }

/* ── Progress bar ─────────────────────────── */
.prog-wrap { margin: 12px 0; }
.prog-label { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 0.78rem; color: #94a3b8; }
.prog-bar { height: 8px; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 99px; transition: width 0.8s ease; }

/* ── Spinner ──────────────────────────────── */
.stSpinner { color: #7c3aed !important; }

/* ── Info / warning ───────────────────────── */
.stAlert { border-radius: 12px !important; }

/* ── Divider ──────────────────────────────── */
hr { border-color: rgba(139,92,246,0.15) !important; }

/* ── Animation ────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-glow {
    0%,100% { box-shadow: 0 0 12px rgba(124,58,237,0.3); }
    50%      { box-shadow: 0 0 28px rgba(124,58,237,0.6); }
}

/* ── Image gen ────────────────────────────── */
.img-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 16px;
    overflow: hidden;
    animation: fadeInUp 0.4s ease;
}
.img-card img { width: 100%; border-radius: 0; }

/* ── Stats row ────────────────────────────── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.stat-card .stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-card .stat-label { font-size: 0.78rem; color: #64748b; margin-top: 2px; }

/* ── Copy hint ────────────────────────────── */
.copy-hint { font-size: 0.75rem; color: #4b5563; text-align: right; margin-top: 8px; }

/* ── Footer ───────────────────────────────── */
.footer {
    text-align: center;
    padding: 28px;
    color: #374151;
    font-size: 0.78rem;
    border-top: 1px solid rgba(139,92,246,0.1);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"

# Set your Groq API key here if you don't want it in the UI.
# You can also set an environment variable GROQ_API_KEY instead.
DEFAULT_API_KEY = "REPLACE_WITH_GROQ_KEY"

# Set your Stability API key here for image generation.
# This is used when STABILITY_API_KEY env var is not set.
STABILITY_API_KEY = "REPLACE_WITH_STABILITY_KEY_FOR_IMAGE_GEN"

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key in ["campaign_result","pitch_result","lead_result","image_result","api_key","image_bytes","image_error"]:
    if key not in st.session_state:
        st.session_state[key] = ""

if not st.session_state.api_key:
    st.session_state.api_key = os.getenv("GROQ_API_KEY", DEFAULT_API_KEY).strip()

PAGE_OPTIONS = [
    "🏠  Home",
    "📣  Campaign Generator",
    "🎤  Sales Pitch Creator",
    "⭐  Lead Qualifier",
    "🎨  AI Image Generator",
]
QUERY_TO_PAGE = {
    "home": PAGE_OPTIONS[0],
    "campaign": PAGE_OPTIONS[1],
    "pitch": PAGE_OPTIONS[2],
    "lead": PAGE_OPTIONS[3],
    "image": PAGE_OPTIONS[4],
}
PAGE_TO_QUERY = {v: k for k, v in QUERY_TO_PAGE.items()}


def get_query_page() -> str:
    try:
        qp = st.query_params.get("page", "home")
        slug = qp[0] if isinstance(qp, list) and qp else qp
    except Exception:
        qp = st.experimental_get_query_params()
        slug = qp.get("page", ["home"])[0]
    return QUERY_TO_PAGE.get(str(slug).lower(), PAGE_OPTIONS[0])


def set_query_page(page_name: str) -> None:
    slug = PAGE_TO_QUERY.get(page_name, "home")
    try:
        st.query_params["page"] = slug
    except Exception:
        st.experimental_set_query_params(page=slug)


def render_topbar(current_page: str) -> None:
    home_cls = "active" if "Home" in current_page else ""
    campaign_cls = "active" if "Campaign" in current_page else ""
    pitch_cls = "active" if "Pitch" in current_page else ""
    lead_cls = "active" if "Lead" in current_page else ""
    image_cls = "active" if "Image" in current_page else ""

    st.markdown(f"""
    <div class='topbar'>
        <div class='topbar-brand'>
            <div class='brand-icon'>📈</div>
            MarketAI Suite
        </div>
        <div class='topbar-nav'>
            <a class='nav-pill nav-pill-link {home_cls}' href='?page=home' target='_self'>Home</a>
            <a class='nav-pill nav-pill-link {campaign_cls}' href='?page=campaign' target='_self'>Campaign</a>
            <a class='nav-pill nav-pill-link {pitch_cls}' href='?page=pitch' target='_self'>Pitch</a>
            <a class='nav-pill nav-pill-link {lead_cls}' href='?page=lead' target='_self'>Lead Score</a>
            <a class='nav-pill nav-pill-link {image_cls}' href='?page=image' target='_self'>Image</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def call_groq(prompt: str, api_key: str) -> str:
    if not api_key:
        return "⚠️ Groq API key not configured. Set DEFAULT_API_KEY in code or use GROQ_API_KEY environment variable."
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model":    GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.75,
        "max_tokens":  2048
    }
    try:
        r = requests.post(GROQ_URL, json=body, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"]
        text = re.sub(r'\*{1,3}(.+?)\*{1,3}', r'\1', text)
        text = re.sub(r'_{1,3}(.+?)_{1,3}', r'\1', text)
        return text.strip()
    except requests.exceptions.HTTPError as e:
        return f"❌ API Error: {e.response.status_code} — {e.response.text[:200]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def extract_score(text: str) -> int:
    patterns = [
        r'(?:Lead Qualification Score|Total Score|Score)[:\s]+(\d{1,3})',
        r'(\d{1,3})\s*/\s*100',
        r'score[:\s]+(\d{1,3})',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            v = int(m.group(1))
            if 0 <= v <= 100:
                return v
    return -1


def score_color(s: int) -> str:
    if s >= 90: return "#10b981"
    if s >= 75: return "#f59e0b"
    if s >= 60: return "#3b82f6"
    return "#ef4444"


def score_class(s: int) -> str:
    if s >= 90: return "score-hot"
    if s >= 75: return "score-warm"
    if s >= 60: return "score-lukewarm"
    return "score-cold"


def score_label(s: int) -> str:
    if s >= 90: return "🔥 HOT LEAD"
    if s >= 75: return "⚡ WARM LEAD"
    if s >= 60: return "💧 LUKEWARM LEAD"
    return "❄️ COLD LEAD"


def generate_placeholder_image(prompt: str) -> str:
    """
    Calls Groq to get an image description, then returns an SVG placeholder
    styled to match the described scene.  (Replace with a real image API
    such as Stability AI / DALL-E when you have a key.)
    """
    desc_prompt = (
        f"Describe in 2-3 vivid sentences the ideal marketing image for: '{prompt}'. "
        "Focus on colors, mood, composition, and visual elements. Be concise."
    )
    return desc_prompt   # caller will use this as the prompt text


def generate_image_bytes(prompt: str, style: str, tone: str) -> bytes:
    """
    Generate an actual image from prompt.
    Provider order:
    1) Stability AI (if STABILITY_API_KEY set)
    2) OpenAI Images (if OPENAI_API_KEY set)
    3) Pollinations public endpoint fallback
    Returns raw image bytes for display in Streamlit.
    """
    # Keep prompt short and URL-safe.
    clean_prompt = " ".join(prompt.split()).strip()
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.:;()/%&+- ")
    clean_prompt = "".join(ch for ch in clean_prompt if ch in allowed_chars)[:220]

    combined_prompt = (
        f"{clean_prompt}, style {style}, tone {tone}, "
        "marketing hero image, clean composition, high detail, cinematic light, 16:9"
    )
    short_prompt = combined_prompt[:700]

    # 1) Stability AI
    stability_key = os.getenv("STABILITY_API_KEY", STABILITY_API_KEY).strip()
    if stability_key:
        try:
            stability_url = "https://api.stability.ai/v2beta/stable-image/generate/core"
            headers = {
                "Authorization": f"Bearer {stability_key}",
                "Accept": "image/*",
            }
            files = {
                "prompt": (None, short_prompt),
                "aspect_ratio": (None, "16:9"),
                "output_format": (None, "png"),
            }
            response = requests.post(stability_url, headers=headers, files=files, timeout=90)
            response.raise_for_status()
            if len(response.content) > 1024:
                return response.content
        except Exception:
            pass

    # 2) OpenAI Images
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        try:
            openai_url = "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json",
            }
            body = {
                "model": "gpt-image-1",
                "prompt": short_prompt,
                "size": "1536x1024",
            }
            response = requests.post(openai_url, headers=headers, json=body, timeout=90)
            response.raise_for_status()
            data = response.json()
            b64 = data["data"][0]["b64_json"]
            return base64.b64decode(b64)
        except Exception:
            pass

    # 3) Public fallback (less reliable)
    encoded_prompt = quote_plus(combined_prompt[:320])
    candidate_urls = [
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&enhance=true&model=flux",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&enhance=true",
    ]

    last_error = None
    for image_url in candidate_urls:
        for attempt in range(3):
            try:
                response = requests.get(image_url, timeout=60)
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "image" not in content_type.lower() or len(response.content) < 1024:
                    raise RuntimeError("Provider returned non-image content.")
                return response.content
            except Exception as e:
                last_error = e
                time.sleep(1.0 + attempt * 1.2)

    raise RuntimeError(
        "Image generation failed. Set STABILITY_API_KEY or OPENAI_API_KEY for reliable image output. "
        f"Fallback provider error: {last_error}"
    )


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 10px 10px;'>
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:24px;'>
            <div style='background:linear-gradient(135deg,#7c3aed,#3b82f6);
                        border-radius:10px;width:38px;height:38px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.2rem;'>📈</div>
            <div>
                <div style='font-family:"Space Grotesk",sans-serif;font-weight:700;
                            font-size:1.05rem;color:#fff;'>MarketAI Suite</div>
                <div style='font-size:0.7rem;color:#6b7280;'>AI marketing workspace</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;font-weight:700;letter-spacing:0.1em;color:#4b5563;text-transform:uppercase;padding:0 10px 6px;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "",
        PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(get_query_page()),
        label_visibility="collapsed"
    )
    set_query_page(page)

    st.markdown("<hr style='margin:20px 0;border-color:rgba(139,92,246,0.15);'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding:10px;background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.2);
                border-radius:12px;font-size:0.75rem;color:#6b7280;line-height:1.6;'>
        <strong style='color:#a78bfa;'>Model:</strong> Configured in backend<br>
        <strong style='color:#a78bfa;'>Provider:</strong> Groq Cloud<br>
        <strong style='color:#a78bfa;'>Speed:</strong> Ultra-fast inference
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
render_topbar(page)

if "Home" in page:
    st.markdown("""
    <div class='main-wrapper'>
        <div class='hero'>
            <div class='hero-badge'>✨ AI-Powered Marketing Tools</div>
            <h1>AI-Powered Marketing Suite</h1>
            <p>Generate high-performing campaigns, craft compelling pitches, and qualify leads with advanced AI technology — all in seconds.</p>
        </div>
        <div class='cards-row'>
            <a class='feature-card feature-card-link' href='?page=campaign' target='_self'>
                <div class='card-icon'>📣</div>
                <h3>Campaign Generator</h3>
                <p>Create data-driven marketing campaigns tailored to your specific audience and platform with AI-powered insights.</p>
            </a>
            <a class='feature-card feature-card-link' href='?page=pitch' target='_self'>
                <div class='card-icon'>🎤</div>
                <h3>Sales Pitch Creator</h3>
                <p>Craft compelling, personalized sales pitches that resonate with your target customers and drive conversions.</p>
            </a>
            <a class='feature-card feature-card-link' href='?page=lead' target='_self'>
                <div class='card-icon'>⭐</div>
                <h3>Lead Qualifier</h3>
                <p>Identify and prioritize high-value leads using intelligent scoring to maximize your sales efficiency.</p>
            </a>
            <a class='feature-card feature-card-link' href='?page=image' target='_self'>
                <div class='card-icon'>🎨</div>
                <h3>AI Image Generator</h3>
                <p>Generate stunning marketing visuals and campaign images using AI to make your brand stand out.</p>
            </a>
        </div>
        <div class='platforms-section'>
            <h2>Supported Platforms</h2>
            <div class='platforms-grid'>
                <div class='platform-chip'>💼 LinkedIn</div>
                <div class='platform-chip'>📘 Facebook</div>
                <div class='platform-chip'>📸 Instagram</div>
                <div class='platform-chip'>🐦 Twitter/X</div>
                <div class='platform-chip'>▶️ YouTube</div>
                <div class='platform-chip'>📧 Email</div>
                <div class='platform-chip'>🎵 TikTok</div>
                <div class='platform-chip'>💬 WhatsApp</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-num'>10x</div>
            <div class='stat-label'>Faster Campaign Creation</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-num'>3</div>
            <div class='stat-label'>AI-Powered Tools</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-num'>70B</div>
            <div class='stat-label'>Parameter AI Model</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='footer'>MarketAI Suite · SmartBridge</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CAMPAIGN GENERATOR
# ─────────────────────────────────────────────
elif "Campaign" in page:
    st.markdown("""
    <div class='tool-page'>
        <div class='tool-header'>
            <h2>📣 Campaign Generator</h2>
            <p>Create data-driven marketing campaigns tailored to your audience</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        product  = st.text_input("PRODUCT NAME", placeholder="e.g., AI Analytics Platform, Dairy Milk Silk")

        audience_options = [
            "Select target audience",
            "Health-conscious millennials",
            "Enterprise IT managers",
            "Small business owners",
            "College students (18-24)",
            "Working professionals (25-40)",
            "Parents with young children",
            "Startup founders",
            "B2B decision-makers",
            "Freelancers and creators",
            "Custom...",
        ]
        audience_choice = st.selectbox("TARGET AUDIENCE", audience_options, index=0)
        audience_custom = ""
        if audience_choice == "Custom...":
            audience_custom = st.text_input("CUSTOM TARGET AUDIENCE", placeholder="Enter your target audience")

        platform_options = [
            "Select marketing platform",
            "LinkedIn",
            "Instagram",
            "Facebook",
            "Twitter/X",
            "YouTube",
            "Email",
            "TikTok",
            "WhatsApp",
            "Google Ads",
            "Multi-channel Campaign",
            "Custom...",
        ]
        platform_choice = st.selectbox("MARKETING PLATFORM", platform_options, index=0)
        platform_custom = ""
        if platform_choice == "Custom...":
            platform_custom = st.text_input("CUSTOM MARKETING PLATFORM", placeholder="Enter your marketing platform")

        audience = audience_custom.strip() if audience_choice == "Custom..." else ("" if audience_choice == "Select target audience" else audience_choice)
        platform = platform_custom.strip() if platform_choice == "Custom..." else ("" if platform_choice == "Select marketing platform" else platform_choice)

        col1, col2 = st.columns(2)
        with col1:
            generate = st.button("🚀 GENERATE CAMPAIGN", use_container_width=True)
        with col2:
            clear = st.button("CLEAR", use_container_width=True, type="secondary")

        if clear:
            st.session_state.campaign_result = ""
            st.rerun()

        st.caption("💡 AI will generate objectives, 5 content ideas, 3 ad copies, CTA suggestions & tracking plan")

    if generate:
        if not product or not audience or not platform:
            st.warning("Please fill in all fields before generating.")
        else:
            with st.spinner("✨ Crafting your campaign strategy..."):
                prompt = f"""You are an expert marketing strategist. Create a comprehensive, detailed marketing campaign strategy.

Product: {product}
Target Audience: {audience}
Platform: {platform}

Structure your response with these exact sections:

CAMPAIGN OBJECTIVE
Write 2-3 clear sentences about the campaign goal and success metrics.

5 CONTENT IDEAS
Number each idea 1-5. Give each a catchy title followed by a 2-sentence description.

3 AD COPY VARIATIONS
Label each: Variation 1 (Problem-Agitate-Solve), Variation 2 (Social Proof), Variation 3 (Limited-Time Offer).
Write the full ad copy for each.

CALL-TO-ACTION SUGGESTIONS
List 5 specific, compelling CTAs numbered 1-5.

TRACKING & MEASUREMENT
List 4 specific metrics and tools to track campaign performance.

Be specific, creative and actionable. No generic advice."""

                result = call_groq(prompt, st.session_state.api_key)
                st.session_state.campaign_result = result

    if st.session_state.campaign_result:
        st.markdown(f"""
        <div class='result-box'>
            <h4>YOUR CAMPAIGN STRATEGY</h4>
            <pre>{st.session_state.campaign_result}</pre>
        </div>
        <div class='copy-hint'>Select text to copy · Tip: Use Ctrl+A inside the box to select all</div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SALES PITCH CREATOR
# ─────────────────────────────────────────────
elif "Pitch" in page:
    st.markdown("""
    <div class='tool-page'>
        <div class='tool-header'>
            <h2>🎤 Sales Pitch Creator</h2>
            <p>Craft compelling, personalized sales pitches for your target customers</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    product  = st.text_input("PRODUCT NAME", placeholder="e.g., Cloud-based inventory management system")
    customer = st.text_input("CUSTOMER PERSONA", placeholder="e.g., CTO at Fortune 500, Operations Director scaling 500 stores")

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("🎯 GENERATE PITCH", use_container_width=True)
    with col2:
        clear = st.button("CLEAR", use_container_width=True, type="secondary")

    if clear:
        st.session_state.pitch_result = ""
        st.rerun()

    st.caption("💡 Generates 30-second pitch, value proposition, differentiators & strategic CTA")

    if generate:
        if not product or not customer:
            st.warning("Please fill in all fields before generating.")
        else:
            with st.spinner("✨ Crafting your personalized pitch..."):
                prompt = f"""You are an elite B2B sales strategist. Create a highly persuasive, personalized sales pitch.

Product: {product}
Customer Persona: {customer}

Structure your response with these exact sections:

30-SECOND ELEVATOR PITCH
Write a concise, punchy pitch (max 80 words) that grabs attention immediately. Start with the pain point.

VALUE PROPOSITION
List 3-4 specific business benefits with measurable outcomes where possible.

KEY DIFFERENTIATORS
List 4-5 competitive advantages that specifically address this persona's concerns.

CALL-TO-ACTION
Write one strong, specific CTA to move the deal forward (demo, pilot, meeting). Include 3 bullet points showing what they'll gain.

OBJECTION HANDLING
Anticipate 2 likely objections and provide sharp responses.

Be highly specific to the customer persona. Sound confident, not salesy."""

                result = call_groq(prompt, st.session_state.api_key)
                st.session_state.pitch_result = result

    if st.session_state.pitch_result:
        st.markdown(f"""
        <div class='result-box'>
            <h4>YOUR SALES PITCH</h4>
            <pre>{st.session_state.pitch_result}</pre>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LEAD QUALIFIER
# ─────────────────────────────────────────────
elif "Lead" in page:
    st.markdown("""
    <div class='tool-page'>
        <div class='tool-header'>
            <h2>⭐ Lead Qualifier</h2>
            <p>Identify and prioritize high-value leads using AI-powered scoring</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    lead_name = st.text_input("LEAD NAME", placeholder="e.g., Rajesh Kumar, John Smith")
    budget    = st.text_input("BUDGET QUALITY", placeholder="e.g., High — $150,000 annual budget, can approve $50K deals")

    need_options = [
        "Select business need",
        "Critical - customer retention / churn reduction",
        "Revenue growth and lead generation",
        "Cost reduction and process efficiency",
        "Market expansion and brand awareness",
        "Product launch support",
        "Customer support improvement",
        "Data-driven decision making",
        "Custom...",
    ]
    need_choice = st.selectbox("BUSINESS NEED", need_options, index=0)
    need_custom = ""
    if need_choice == "Custom...":
        need_custom = st.text_input("CUSTOM BUSINESS NEED", placeholder="Enter business need")

    urgency_options = [
        "Select urgency level",
        "Immediate (0-30 days)",
        "High (1-3 months)",
        "Medium (3-6 months)",
        "Low (6+ months)",
        "Exploratory / no fixed timeline",
        "Custom...",
    ]
    urgency_choice = st.selectbox("URGENCY LEVEL", urgency_options, index=0)
    urgency_custom = ""
    if urgency_choice == "Custom...":
        urgency_custom = st.text_input("CUSTOM URGENCY LEVEL", placeholder="Enter urgency level")

    need = need_custom.strip() if need_choice == "Custom..." else ("" if need_choice == "Select business need" else need_choice)
    urgency = urgency_custom.strip() if urgency_choice == "Custom..." else ("" if urgency_choice == "Select urgency level" else urgency_choice)

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("⭐ SCORE LEAD", use_container_width=True)
    with col2:
        clear = st.button("CLEAR", use_container_width=True, type="secondary")

    if clear:
        st.session_state.lead_result = ""
        st.rerun()

    st.caption("💡 Scores help prioritize your sales efforts and maximize efficiency")

    if generate:
        if not lead_name or not budget or not need or not urgency:
            st.warning("Please fill in all fields before scoring.")
        else:
            with st.spinner("🔍 Analysing lead qualification..."):
                prompt = f"""You are a senior sales qualification expert. Evaluate this lead using the BANT framework.

Lead Name: {lead_name}
Budget: {budget}
Business Need: {need}
Urgency: {urgency}

Provide a structured assessment:

LEAD QUALIFICATION SCORE
State a single numeric score out of 100. Format: "Lead Qualification Score: XX/100"

SCORING BREAKDOWN
- Budget Score: X/30 — explain
- Need Score: X/30 — explain
- Urgency Score: X/40 — explain
- Total Score: XX/100

PROBABILITY OF CONVERSION
State as: "Probability of Conversion: XX%"
Explain the key factors driving this estimate in 3-4 sentences.

RECOMMENDED NEXT ACTIONS
List 3 specific, immediate actions the sales team should take.

RISK FACTORS
List 2 potential risks or blockers to watch for.

Be analytical, specific and data-driven."""

                result = call_groq(prompt, st.session_state.api_key)
                st.session_state.lead_result = result

    if st.session_state.lead_result:
        score = extract_score(st.session_state.lead_result)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        if score >= 0:
            col_score, col_info = st.columns([1, 2])
            with col_score:
                sc = score_class(score)
                col = score_color(score)
                st.markdown(f"""
                <div style='text-align:center;padding:24px;
                            background:rgba(255,255,255,0.03);
                            border:1px solid rgba(139,92,246,0.2);
                            border-radius:16px;'>
                    <div class='score-badge {sc}'>{score}</div>
                    <div style='font-family:"Space Grotesk",sans-serif;
                                font-size:0.85rem;font-weight:700;
                                color:{col};margin-bottom:8px;'>{score_label(score)}</div>
                    <div style='font-size:0.75rem;color:#6b7280;'>out of 100</div>
                </div>
                """, unsafe_allow_html=True)
            with col_info:
                st.markdown(f"""
                <div style='padding:20px;background:rgba(255,255,255,0.03);
                            border:1px solid rgba(139,92,246,0.2);border-radius:16px;'>
                    <div style='font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                                text-transform:uppercase;color:#7c3aed;margin-bottom:14px;'>
                        Score Breakdown
                    </div>
                    <div class='prog-wrap'>
                        <div class='prog-label'><span>Budget</span><span>30/30</span></div>
                        <div class='prog-bar'>
                            <div class='prog-fill' style='width:{min(score,30)/30*100:.0f}%;
                                background:linear-gradient(90deg,#7c3aed,#a78bfa);'></div>
                        </div>
                    </div>
                    <div class='prog-wrap'>
                        <div class='prog-label'><span>Need</span><span>30/30</span></div>
                        <div class='prog-bar'>
                            <div class='prog-fill' style='width:{min(score,30)/30*100:.0f}%;
                                background:linear-gradient(90deg,#3b82f6,#60a5fa);'></div>
                        </div>
                    </div>
                    <div class='prog-wrap'>
                        <div class='prog-label'><span>Urgency</span><span>40/40</span></div>
                        <div class='prog-bar'>
                            <div class='prog-fill' style='width:{score:.0f}%;
                                background:linear-gradient(90deg,#10b981,#34d399);'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='result-box'>
            <h4>LEAD QUALIFICATION ANALYSIS</h4>
            <pre>{st.session_state.lead_result}</pre>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AI IMAGE GENERATOR
# ─────────────────────────────────────────────
elif "Image" in page:
    st.markdown("""
    <div class='tool-page'>
        <div class='tool-header'>
            <h2>🎨 AI Image Generator</h2>
            <p>Generate creative marketing image concepts and visual briefs using AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **How it works:** Enter your marketing scenario and the AI will generate a detailed visual brief + creative direction that you can use with image tools like Midjourney, DALL-E, or Stable Diffusion.", icon="ℹ️")

    prompt_input = st.text_area(
        "IMAGE CONCEPT / MARKETING BRIEF",
        placeholder="e.g., A luxury SaaS dashboard for enterprise clients showing real-time analytics with a dark theme...\nor: Hero image for a health-tech app targeting millennials with a vibrant, energetic feel...",
        height=120
    )

    style = st.selectbox(
        "VISUAL STYLE",
        ["Professional / Corporate", "Modern / Minimalist", "Bold / Vibrant",
         "Luxury / Premium", "Playful / Creative", "Tech / Futuristic",
         "Nature / Organic", "Editorial / Magazine"]
    )

    tone = st.selectbox(
        "BRAND TONE",
        ["Trustworthy & Authoritative", "Energetic & Dynamic",
         "Elegant & Sophisticated", "Friendly & Approachable",
         "Innovative & Cutting-edge", "Warm & Emotional"]
    )

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("🎨 GENERATE VISUAL BRIEF", use_container_width=True)
    with col2:
        clear = st.button("CLEAR", use_container_width=True, type="secondary")

    if clear:
        st.session_state.image_result = ""
        st.session_state.image_bytes = b""
        st.session_state.image_error = ""
        st.rerun()

    if generate:
        if not prompt_input:
            st.warning("Please describe the image concept you want to generate.")
        else:
            with st.spinner("🎨 Crafting your visual concept..."):
                full_prompt = f"""You are a world-class creative director and visual designer. Create a comprehensive AI image generation brief.

Marketing Brief: {prompt_input}
Visual Style: {style}
Brand Tone: {tone}

Generate a complete creative brief with these sections:

IMAGE DESCRIPTION
Write a vivid, detailed scene description (4-5 sentences) for an AI image generator. Include lighting, composition, atmosphere, colors, and key elements.

MIDJOURNEY PROMPT
Write a ready-to-use Midjourney prompt with style parameters. Format:
/imagine [detailed description] --style [style] --ar 16:9 --v 6

DALL-E PROMPT
Write a clear DALL-E 3 prompt (2-3 sentences).

STABLE DIFFUSION PROMPT
Write positive prompt + negative prompt.

COLOR PALETTE
List 5 specific hex color codes with names that match this visual.

VISUAL COMPOSITION
Describe the layout, focal point, foreground/background elements, and camera angle.

USAGE RECOMMENDATIONS
List 3 specific marketing contexts where this image works best (social post, banner, landing hero, etc.)

Be extremely specific and creative. Make it production-ready."""

                result = call_groq(full_prompt, st.session_state.api_key)
                st.session_state.image_result = result
                try:
                    st.session_state.image_bytes = generate_image_bytes(prompt_input, style, tone)
                    st.session_state.image_error = ""
                except Exception as e:
                    st.session_state.image_bytes = b""
                    st.session_state.image_error = f"Image generation failed: {str(e)}"

    if st.session_state.image_result:
        # Extract hex colors if present
        hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', st.session_state.image_result)

        if hex_colors:
            st.markdown("<div style='margin:16px 0 8px;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#7c3aed;'>SUGGESTED COLOR PALETTE</div>", unsafe_allow_html=True)
            cols = st.columns(min(len(hex_colors), 6))
            for i, (col, hx) in enumerate(zip(cols, hex_colors[:6])):
                with col:
                    st.markdown(f"""
                    <div style='background:{hx};height:48px;border-radius:10px;
                                margin-bottom:4px;border:1px solid rgba(255,255,255,0.1);'></div>
                    <div style='font-size:0.7rem;color:#6b7280;text-align:center;'>{hx}</div>
                    """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='result-box'>
            <h4>🎨 YOUR VISUAL BRIEF</h4>
            <pre>{st.session_state.image_result}</pre>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:20px;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#7c3aed;margin-bottom:10px;'>GENERATED IMAGE PREVIEW</div>", unsafe_allow_html=True)

        if st.session_state.image_bytes:
            st.image(st.session_state.image_bytes, use_container_width=True)
            st.success("✅ Visual brief and AI-generated image are ready.")
        else:
            if st.session_state.image_error:
                st.warning(f"⚠ {st.session_state.image_error}")
            st.info("Image preview is currently unavailable. You can still use the generated prompts above.")

# ─────────────────────────────────────────────
# FOOTER (all pages)
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    MarketAI Suite · AI-Powered Sales & Marketing Platform ·
    SmartBridge × SkillWallet
</div>
""", unsafe_allow_html=True)
