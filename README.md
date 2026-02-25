# MarketAI Suite — Setup Guide

## Quick Start (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
Navigate to → http://localhost:8501

---

## Features
| Feature | Description |
|---|---|
| 📣 Campaign Generator | AI marketing campaigns with content ideas, ad copies & CTAs |
| 🎤 Sales Pitch Creator | Personalized pitches with elevator pitch, value prop & differentiators |
| ⭐ Lead Qualifier | BANT-based lead scoring (0–100) with conversion probability |
| 🎨 AI Image Generator | Visual briefs + ready-to-use Midjourney/DALL-E/SD prompts |

## API Key
- Get your free Groq API key at: https://console.groq.com
- Enter it in the sidebar under "API Configuration"
- Key is stored only in your session (never saved to disk)

## Project Structure
```
MarketAI/
├── app.py            ← Main Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

## Notes
- The AI Image Generator creates detailed creative briefs + ready-to-copy prompts for Midjourney, DALL-E 3, and Stable Diffusion
- All AI responses use Groq's ultra-fast LLaMA 3.3 70B model
- Results are shown in-session; refresh clears history
