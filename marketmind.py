import streamlit as st
import os
from groq import Groq
import re

# '''=================API_KEY session==================='''
# Replace with your actual Groq API Key
# ================= API SESSION (GROQ) =================
from groq import Groq

GROQ_API_KEY = "Replace with API key"  # ← paste your real key

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"
# =======================================================
# '''=================API_KEY session==================='''

# Define the model (equivalent speed/type to flash)
MODEL = "llama-3.3-70b-versatile" 

# Define system prompt
SYSTEM_PROMPT = "You are a helpful assistant."

def get_groq_response(user_prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model=MODEL,
        temperature=0.7, # Optional: controls randomness
    )
    return chat_completion.choices[0].message.content

# Usage
# response = get_groq_response("Explain how AI works")
# print(response)
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MarketAI Suite Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Mono', monospace; }

.stApp { background: #07070f; color: #e0e0f0; }

[data-testid="stSidebar"] {
    background: #0d0d1f !important;
    border-right: 1px solid #1a1a3a;
}
[data-testid="stSidebar"] * { color: #b0b0d0 !important; }

.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #1a1a3a;
    margin-bottom: 2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #7b61ff 0%, #00d4aa 45%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero p {
    color: #555580;
    font-size: 0.78rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7b61ff;
    margin-bottom: 0.3rem;
}

.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background: #0f0f22 !important;
    border: 1px solid #252550 !important;
    border-radius: 6px !important;
    color: #e0e0f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7b61ff !important;
    box-shadow: 0 0 0 2px rgba(123,97,255,0.12) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #7b61ff !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7b61ff, #00d4aa) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.8rem 2rem !important;
    letter-spacing: 0.05em !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Part tabs */
.part-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    padding: 0.4rem 0.9rem;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 1rem;
}
.part-1 { background: rgba(123,97,255,0.15); color: #7b61ff; border: 1px solid rgba(123,97,255,0.3); }
.part-2 { background: rgba(0,212,170,0.12); color: #00d4aa; border: 1px solid rgba(0,212,170,0.3); }
.part-3 { background: rgba(255,107,107,0.12); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }

.card {
    background: #0f0f22;
    border: 1px solid #1a1a3a;
    border-radius: 10px;
    padding: 1.4rem 1.7rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7b61ff;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1a1a3a;
}
.card-body {
    color: #b8b8d8;
    font-size: 0.86rem;
    line-height: 1.85;
    white-space: pre-wrap;
}

/* Score widget */
.score-box {
    text-align: center;
    padding: 2rem;
    background: #0f0f22;
    border: 1px solid #1a1a3a;
    border-radius: 12px;
    margin-bottom: 1rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
}
.score-hot   { color: #ff4444; }
.score-warm  { color: #ff9944; }
.score-luke  { color: #ffcc44; }
.score-cold  { color: #4488ff; }
.score-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555580;
    margin-top: 0.4rem;
}

.badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.2rem 0.7rem;
    border-radius: 4px;
}
.badge-green { background: rgba(0,212,170,0.1); color: #00d4aa; border: 1px solid rgba(0,212,170,0.3); }
.badge-purple { background: rgba(123,97,255,0.1); color: #7b61ff; border: 1px solid rgba(123,97,255,0.3); }

hr { border-color: #1a1a3a !important; margin: 1.5rem 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #07070f; }
::-webkit-scrollbar-thumb { background: #252550; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #7b61ff; }
</style>
""", unsafe_allow_html=True)

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are the AI Core Engine of MarketAI Suite — an AI-powered Sales & Marketing Intelligence Platform.
Your role is to generate:
1. AI-Driven Marketing Campaign Strategy
2. Intelligent Enterprise Sales Pitch
3. Quantified Lead Scoring & Qualification Analysis

STRICT GLOBAL CONDITIONS:
1. Follow the structure EXACTLY as defined below.
2. No generic marketing or sales advice.
3. All recommendations must be data-driven and business-focused.
4. Use quantified reasoning wherever possible.
5. Maintain professional B2B enterprise tone.
6. Avoid repetition.
7. Do not hallucinate unrealistic metrics.
8. Include Innovation Layer in every section.
9. Output must be cleanly structured with headings.
10. All scoring must follow logical evaluation.

OUTPUT STRUCTURE (STRICT FORMAT):

==============================
PART 1: AI MARKETING CAMPAIGN STRATEGY
==============================
1. Campaign Objective
   - SMART goal
   - Business KPIs
   - ROI reasoning
2. Audience Intelligence Analysis
   - Pain points
   - Buying triggers
   - Platform behavior insights
3. 5 High-Impact Content Ideas
   - Hook
   - Format
   - Strategic purpose
4. 3 Ad Copy Variations
   - Emotion-driven
   - Logic-driven
   - Data-driven
5. Platform-Specific CTA Strategy
6. Innovation Layer
   - AI automation
   - Predictive analytics
   - Optimization strategy

==============================
PART 2: ENTERPRISE SALES PITCH
==============================
1. 30-Second Elevator Pitch
2. Strategic Value Proposition
   - Business impact
   - ROI logic
   - Cost-benefit reasoning
3. Key Differentiators
   - Competitive positioning
   - Scalability
   - Risk reduction
4. Pain Point Mapping
   Problem → Solution → Outcome
5. Objection Handling Strategy
   - Budget
   - Integration
   - Risk
6. Strategic Call-To-Action
7. Innovation Layer
   - AI-driven personalization
   - Automation advantage

==============================
PART 3: INTELLIGENT LEAD SCORING
==============================
1. Lead Qualification Score (0-100)
2. Category Classification
   - 90-100: Hot
   - 75-89: Warm
   - 60-74: Lukewarm
   - Below 60: Cold
3. Scoring Breakdown
   - Budget Score
   - Need Score
   - Urgency Score
   - Authority Score
4. Detailed Justification
5. Probability of Conversion (%)
6. Recommended Sales Action Plan
7. Innovation Layer
   - Predictive conversion logic
   - CRM automation recommendation

FINAL INSTRUCTION:
Ensure that all sections are complete, output is executive-ready, analysis is logical and measurable, and innovation elements are practical and modern."""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">⚡ MarketAI Suite Pro</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="section-label">Platform</div>', unsafe_allow_html=True)
    platform = st.selectbox("Platform", [
        "LinkedIn", "Google Ads", "Meta (Facebook/Instagram)",
        "YouTube", "Twitter / X", "TikTok", "Email Marketing", "Content / SEO"
    ], label_visibility="collapsed")

    st.markdown('<div class="section-label">Industry</div>', unsafe_allow_html=True)
    industry = st.selectbox("Industry", [
        "SaaS / Software", "FinTech", "HealthTech", "E-Commerce",
        "Manufacturing", "Consulting", "Real Estate", "EdTech", "Logistics", "Other"
    ], label_visibility="collapsed")

    st.markdown('<div class="section-label">Company Size</div>', unsafe_allow_html=True)
    company_size = st.selectbox("Company Size", [
        "1–10 (Startup)", "11–50 (Small)", "51–200 (Mid-Market)",
        "201–1000 (Growth)", "1000+ (Enterprise)"
    ], label_visibility="collapsed")

    st.markdown('<div class="section-label">Budget Range</div>', unsafe_allow_html=True)
    budget_range = st.selectbox("Budget Range", [
        "Under $5K/mo", "$5K–$20K/mo", "$20K–$50K/mo",
        "$50K–$100K/mo", "$100K+/mo"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div style="color:#333360; font-size:0.68rem; line-height:1.7;">AI-generated outputs.<br>Validate before deployment.</div>', unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>MarketAI Suite Pro</h1>
    <p>Campaign Strategy · Sales Pitch · Lead Scoring · All-in-One Intelligence Engine</p>
</div>
""", unsafe_allow_html=True)

# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown("### 📋 Campaign & Product Inputs")
col1, col2 = st.columns(2, gap="large")
with col1:
    product  = st.text_area("Product Details", placeholder="e.g. AI-powered B2B CRM at $499/mo with predictive sales forecasting…", height=120)
    audience = st.text_area("Target Audience", placeholder="e.g. VP of Sales at SaaS companies, 50–500 employees, Series B+…", height=120)
with col2:
    persona  = st.text_area("Customer Persona", placeholder="e.g. Decision-maker, tech-savvy, data-driven, 35–50 age range, LinkedIn active…", height=120)
    campaign_goal = st.text_area("Campaign Goal (optional)", placeholder="e.g. Generate 50 qualified demo requests in 30 days…", height=120)

st.markdown("---")
st.markdown("### 🎯 Lead Information")
col3, col4 = st.columns(2, gap="large")
with col3:
    lead_name      = st.text_input("Lead Name / Company", placeholder="e.g. John Smith / Acme Corp")
    lead_budget    = st.text_input("Lead Budget", placeholder="e.g. $30K/quarter allocated")
    lead_need      = st.text_area("Business Need", placeholder="e.g. Needs to reduce sales cycle by 30% before Q3…", height=90)
with col4:
    lead_urgency   = st.selectbox("Urgency Level", ["Critical (immediate)", "High (within 1 month)", "Medium (1–3 months)", "Low (3–6 months)", "Exploratory"])
    lead_authority = st.selectbox("Authority Level", ["Final Decision Maker", "Strong Influencer", "Committee Member", "Recommender Only", "Unknown"])

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("⚡ Generate Full Intelligence Report")

# ── Helpers ───────────────────────────────────────────────────────────────────
PART_PATTERNS = {
    "PART 1": r"PART 1[:\s]+AI MARKETING CAMPAIGN STRATEGY",
    "PART 2": r"PART 2[:\s]+ENTERPRISE SALES PITCH",
    "PART 3": r"PART 3[:\s]+INTELLIGENT LEAD SCORING",
}

PART1_SECTIONS = [
    ("1. Campaign Objective", "🎯"),
    ("2. Audience Intelligence Analysis", "🧠"),
    ("3. 5 High-Impact Content Ideas", "💡"),
    ("4. 3 Ad Copy Variations", "✍️"),
    ("5. Platform-Specific CTA Strategy", "📣"),
    ("6. Innovation Layer", "🤖"),
]
PART2_SECTIONS = [
    ("1. 30-Second Elevator Pitch", "🚀"),
    ("2. Strategic Value Proposition", "💎"),
    ("3. Key Differentiators", "🏆"),
    ("4. Pain Point Mapping", "🗺️"),
    ("5. Objection Handling Strategy", "🛡️"),
    ("6. Strategic Call-To-Action", "📞"),
    ("7. Innovation Layer", "🤖"),
]
PART3_SECTIONS = [
    ("1. Lead Qualification Score", "📊"),
    ("2. Category Classification", "🏷️"),
    ("3. Scoring Breakdown", "📈"),
    ("4. Detailed Justification", "📝"),
    ("5. Probability of Conversion", "🎰"),
    ("6. Recommended Sales Action Plan", "📋"),
    ("7. Innovation Layer", "🤖"),
]


def split_parts(text: str):
    """Split full output into 3 part strings."""
    p1 = p2 = p3 = ""
    m1 = re.search(r"PART 1", text)
    m2 = re.search(r"PART 2", text)
    m3 = re.search(r"PART 3", text)
    if m1 and m2:
        p1 = text[m1.start():m2.start()]
    if m2 and m3:
        p2 = text[m2.start():m3.start()]
    if m3:
        p3 = text[m3.start():]
    if not p1:
        p1 = text
    return p1, p2, p3


def parse_numbered_sections(text: str, sections: list) -> dict:
    """Extract numbered subsections from a part."""
    result = {}
    for i, (title, _) in enumerate(sections):
        num = title.split(".")[0].strip()
        next_num = sections[i+1][0].split(".")[0].strip() if i+1 < len(sections) else None
        pattern = rf"{re.escape(num)}\.\s+.+?\n(.*?)" + (rf"(?={re.escape(next_num)}\.\s)" if next_num else r"$")
        m = re.search(pattern, text, re.DOTALL)
        if m:
            result[title] = m.group(1).strip()
        else:
            # fallback: just grab text between headings
            result[title] = ""
    return result


def extract_score(text: str) -> int:
    """Pull numeric score from part 3 text."""
    m = re.search(r"(?:score|total)[^\d]*(\d{1,3})", text, re.IGNORECASE)
    if m:
        val = int(m.group(1))
        if 0 <= val <= 100:
            return val
    nums = re.findall(r"\b([6-9]\d|100)\b", text)
    return int(nums[0]) if nums else 0


def score_class(score: int) -> tuple:
    if score >= 90: return "score-hot",   "🔥 HOT LEAD"
    if score >= 75: return "score-warm",  "🌡️ WARM LEAD"
    if score >= 60: return "score-luke",  "⚡ LUKEWARM"
    return "score-cold", "❄️ COLD LEAD"


def render_part(part_text: str, sections: list, part_num: int):
    parsed = parse_numbered_sections(part_text, sections)
    part_cls = f"part-{part_num}"
    labels = {1: "📊 Part 1 · AI Marketing Campaign Strategy",
              2: "💼 Part 2 · Enterprise Sales Pitch",
              3: "🎯 Part 3 · Intelligent Lead Scoring"}
    st.markdown(f'<div class="part-header {part_cls}">{labels[part_num]}</div>', unsafe_allow_html=True)

    if part_num == 3:
        score = extract_score(part_text)
        cls, label = score_class(score)
        sc1, sc2, sc3 = st.columns([1, 2, 1])
        with sc2:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-number {cls}">{score}</div>
                <div class="score-label">{label} · Lead Score / 100</div>
            </div>""", unsafe_allow_html=True)

    for title, icon in sections:
        content = parsed.get(title, "").strip()
        if not content:
            # Try grabbing any block with matching number
            num = title.split(".")[0]
            m = re.search(rf"{num}\.\s+[^\n]+\n(.*?)(?=\n\d+\.|\Z)", part_text, re.DOTALL)
            content = m.group(1).strip() if m else ""
        if not content:
            continue
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{icon} &nbsp; {title}</div>
            <div class="card-body">{content}</div>
        </div>""", unsafe_allow_html=True)


# ── Generation ────────────────────────────────────────────────────────────────
if run:
    missing = []
    if not product.strip():  missing.append("Product Details")
    if not audience.strip(): missing.append("Target Audience")
    if not persona.strip():  missing.append("Customer Persona")
    if not lead_name.strip(): missing.append("Lead Name")

    if missing:
        st.warning(f"Please fill in: **{', '.join(missing)}**")
    else:
        user_message = f"""Generate the full 3-part intelligence report for:

Product Details: {product.strip()}
Target Audience: {audience.strip()}
Marketing Platform: {platform}
Customer Persona: {persona.strip()}
Industry: {industry}
Company Size: {company_size}
Budget Range: {budget_range}
Campaign Goal: {campaign_goal.strip() or 'Not specified'}

Lead Information:
- Lead Name: {lead_name.strip()}
- Budget Info: {lead_budget.strip() or 'Not specified'}
- Business Need: {lead_need.strip() or 'Not specified'}
- Urgency Level: {lead_urgency}
- Authority Level: {lead_authority}

Follow the mandatory output structure exactly. Include all 3 parts completely."""

        st.markdown("---")
        st.markdown('<span style="font-family:Syne,sans-serif;font-size:0.7rem;font-weight:700;letter-spacing:0.15em;color:#00d4aa;">⚡ GENERATING INTELLIGENCE REPORT…</span>', unsafe_allow_html=True)



        # ================= GROQ GENERATION =================
        full_text = ""
        stream_ph = st.empty()

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                stream=True
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_text += content
                    stream_ph.markdown(
                        f'<div class="card"><div class="card-body">{full_text[-2000:]}▌</div></div>',
                        unsafe_allow_html=True,
                    )
        except Exception as e:
            st.error(f"❌ Groq API error: {e}")
            st.stop()
        
# ===================================================

        stream_ph.empty()
        st.markdown('<span style="font-family:Syne,sans-serif;font-size:0.7rem;font-weight:700;letter-spacing:0.15em;color:#00d4aa;">✓ REPORT READY</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Split and render 3 parts
        p1, p2, p3 = split_parts(full_text)

        tab1, tab2, tab3 = st.tabs([
            "📊 Campaign Strategy",
            "💼 Sales Pitch",
            "🎯 Lead Scoring"
        ])
        with tab1:
            if p1:
                render_part(p1, PART1_SECTIONS, 1)
            else:
                st.markdown(f'<div class="card"><div class="card-body">{full_text}</div></div>', unsafe_allow_html=True)
        with tab2:
            if p2:
                render_part(p2, PART2_SECTIONS, 2)
            else:
                st.info("Part 2 not found in output. Try regenerating.")
        with tab3:
            if p3:
                render_part(p3, PART3_SECTIONS, 3)
            else:
                st.info("Part 3 not found in output. Try regenerating.")

        # Download
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "⬇ Download Full Report (.txt)",
            data=full_text,
            file_name=f"marketai_report_{lead_name.strip().replace(' ','_').lower()}.txt",
            mime="text/plain",
        )