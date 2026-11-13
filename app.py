import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="StartupMateAI - Your AI Co-Founder",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Theme State Management
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    bg_color = "#0b0f19"
    text_color = "#f8fafc"
    muted_text = "#94a3b8"
    card_bg = "rgba(30, 41, 59, 0.75)"
    card_border = "rgba(148, 163, 184, 0.18)"
    input_bg = "rgba(15, 23, 42, 0.90)"
    pill_bg = "rgba(30, 41, 59, 0.80)"
    footer_bg = "rgba(11, 15, 25, 0.85)"
    brand_border = "#818cf8"
    placeholder_color = "#64748b"
    scheme = "dark"
    input_border = "rgba(129, 140, 248, 0.30)"
    grid_color = "rgba(255, 255, 255, 0.04)"
else:
    bg_color = "#f8f9fc"
    text_color = "#0f172a"
    muted_text = "#64748b"
    card_bg = "rgba(255, 255, 255, 0.85)"
    card_border = "rgba(226, 232, 240, 0.95)"
    input_bg = "rgba(255, 255, 255, 0.95)"
    pill_bg = "rgba(255, 255, 255, 0.85)"
    footer_bg = "rgba(248, 249, 252, 0.85)"
    brand_border = "#1e293b"
    placeholder_color = "#94a3b8"
    scheme = "light"
    input_border = "rgba(99, 102, 241, 0.25)"
    grid_color = "rgba(15, 23, 42, 0.04)"

# 3. Dynamic Custom CSS & Modern Animations (No triple quotes used)
css_lines = [
    "<style>",
    "@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');",
    "#MainMenu, header, footer {visibility: hidden;}",
    "[data-testid='stToolbar'] {display: none;}",
    f".stApp {{ background-color: {bg_color} !important; background-image: radial-gradient({grid_color} 1px, transparent 1px) !important; background-size: 24px 24px !important; color: {text_color} !important; font-family: 'Plus Jakarta Sans', sans-serif; overflow-x: hidden; color-scheme: {scheme}; transition: background-color 0.35s ease, color 0.35s ease; }}",
    ".aurora-container { position: fixed; inset: 0; overflow: hidden; z-index: 0; pointer-events: none; }",
    ".orb { position: absolute; border-radius: 50%; filter: blur(60px); opacity: 0.65; }",
    ".orb-1 { width: 42vw; height: 42vw; max-width: 500px; max-height: 500px; bottom: -12vh; left: 16%; background: radial-gradient(circle, rgba(168,85,247,0.55) 0%, rgba(99,102,241,0.25) 60%, transparent 80%); animation: floatOrb1 9s ease-in-out infinite alternate; }",
    ".orb-2 { width: 38vw; height: 38vw; max-width: 460px; max-height: 460px; bottom: -14vh; right: 14%; background: radial-gradient(circle, rgba(251,146,60,0.50) 0%, rgba(236,72,153,0.35) 55%, transparent 80%); animation: floatOrb2 11s ease-in-out infinite alternate; }",
    ".orb-3 { width: 28vw; height: 28vw; max-width: 340px; max-height: 340px; top: 12vh; left: 50%; transform: translateX(-50%); background: radial-gradient(circle, rgba(56,189,248,0.25) 0%, rgba(129,140,248,0.15) 60%, transparent 80%); animation: floatOrb3 8s ease-in-out infinite alternate; }",
    "@keyframes floatOrb1 { 0% { transform: translate(0, 0) scale(0.95); } 100% { transform: translate(-28px, -22px) scale(1.08); } }",
    "@keyframes floatOrb2 { 0% { transform: translate(0, 0) scale(1.05); } 100% { transform: translate(32px, -26px) scale(0.92); } }",
    "@keyframes floatOrb3 { 0% { transform: translateX(-50%) translateY(0) scale(0.9); } 100% { transform: translateX(-45%) translateY(18px) scale(1.1); } }",
    "@keyframes fadeUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }",
    "@keyframes gradientFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }",
    "@keyframes pulseDot { 0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); } 50% { transform: scale(1.15); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); } }",
    ".block-container { position: relative; z-index: 2; padding-top: 6.2rem !important; padding-bottom: 5.5rem !important; max-width: 760px !important; }",
    ".fixed-top-nav { position: fixed; top: 20px; left: 28px; right: 28px; display: flex; justify-content: space-between; align-items: center; z-index: 99999; pointer-events: none; }",
    ".pointer-events-auto { pointer-events: auto; }",
    f".logo-badge {{ display: flex; align-items: center; gap: 9px; border: 1.5px solid {brand_border}; border-radius: 999px; padding: 6px 16px 6px 10px; font-size: 0.95rem; font-weight: 700; color: {text_color}; background: {input_bg}; backdrop-filter: blur(12px); box-shadow: 3px 3px 0px #6366f1; transition: all 0.25s ease; cursor: pointer; }}",
    ".logo-badge:hover { transform: translate(-2px, -2px) scale(1.03); box-shadow: 5px 5px 0px #ec4899; }",
    ".logo-icon-circle { width: 22px; height: 22px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #ec4899); display: inline-flex; align-items: center; justify-content: center; color: white; }",
    f"div.stButton > button {{ background: {pill_bg} !important; backdrop-filter: blur(12px) !important; color: {text_color} !important; border: 1px solid {card_border} !important; border-radius: 999px !important; padding: 0.42rem 1.05rem !important; font-size: 0.85rem !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(0,0,0,0.06) !important; transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important; }}",
    "div.stButton > button:hover { transform: translateY(-3px) scale(1.02) !important; box-shadow: 0 10px 24px rgba(99,102,241,0.22) !important; border-color: #818cf8 !important; }",
    ".hero-badge-wrap { display: flex; justify-content: center; margin-top: 5vh; margin-bottom: 0.8rem; animation: fadeUp 0.55s ease-out both; }",
    ".hero-badge { display: inline-flex; align-items: center; gap: 8px; padding: 5px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; background: rgba(99,102,241,0.12); border: 1px solid rgba(129,140,248,0.35); color: #818cf8; }",
    ".live-dot { width: 7px; height: 7px; border-radius: 50%; background: #10b981; animation: pulseDot 2s infinite; }",
    f".hero-heading {{ font-family: 'Instrument Serif', Georgia, serif; font-size: clamp(2.4rem, 9vw, 3.8rem); line-height: 1.08; font-weight: 400; color: {text_color}; text-align: center; margin-bottom: 0.65rem; letter-spacing: -0.02em; animation: fadeUp 0.65s ease-out 0.08s both; }}",
    ".gradient-word { font-style: italic; background: linear-gradient(90deg, #6366f1, #ec4899, #f59e0b, #6366f1); background-size: 250% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradientFlow 5s linear infinite; padding-right: 4px; }",
    f".hero-subtitle {{ text-align: center; font-size: 0.96rem; color: {muted_text}; margin-bottom: 1.8rem; animation: fadeUp 0.7s ease-out 0.14s both; }}",
    f"[data-testid='stChatInput'] {{ background: {input_bg} !important; backdrop-filter: blur(16px) !important; border-radius: 999px !important; border: 1.5px solid {input_border} !important; box-shadow: 0 14px 36px rgba(99,102,241,0.12), 0 2px 6px rgba(0,0,0,0.04) !important; padding: 6px 58px 6px 22px !important; position: relative !important; transition: all 0.25s ease !important; animation: fadeUp 0.75s ease-out 0.18s both; }}",
    "[data-testid='stChatInput']:focus-within { border-color: #818cf8 !important; box-shadow: 0 18px 44px rgba(99,102,241,0.22), 0 0 0 4px rgba(129,140,248,0.18) !important; transform: translateY(-2px); }",
    "[data-testid='stChatInput'] > div, [data-testid='stChatInput'] [data-baseweb='textarea'], [data-testid='stChatInput'] [data-baseweb='base-input'] { background: transparent !important; border: none !important; box-shadow: none !important; border-radius: 999px !important; }",
    f"[data-testid='stChatInput'] textarea {{ background: transparent !important; color: {text_color} !important; font-size: 1rem !important; font-family: 'Plus Jakarta Sans', sans-serif !important; padding: 0.65rem 0 !important; caret-color: #ec4899; }}",
    f"[data-testid='stChatInput'] textarea::placeholder {{ color: {placeholder_color} !important; opacity: 1 !important; }}",
    "[data-testid='stChatInputSubmitButton'] { background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important; color: #ffffff !important; border: none !important; border-radius: 50% !important; width: 40px !important; height: 40px !important; padding: 0 !important; position: absolute !important; top: 50% !important; bottom: auto !important; right: 8px !important; transform: translateY(-50%); box-shadow: 0 4px 14px rgba(168,85,247,0.4) !important; transition: all 0.25s ease !important; }",
    "[data-testid='stChatInputSubmitButton']:hover { transform: translateY(-50%) scale(1.1) !important; box-shadow: 0 6px 20px rgba(236,72,153,0.55) !important; }",
    "[data-testid='stChatInputSubmitButton'] svg { fill: #ffffff !important; }",
    f"[data-testid='stChatMessage'] {{ background: {card_bg} !important; backdrop-filter: blur(16px) !important; border: 1px solid {card_border} !important; border-radius: 20px !important; padding: 16px 20px !important; margin-bottom: 14px !important; box-shadow: 0 8px 26px rgba(0,0,0,0.05) !important; color: {text_color} !important; animation: fadeUp 0.35s ease-out both; }}",
    f"[data-testid='stChatMessage'] p, [data-testid='stChatMessage'] li, [data-testid='stChatMessage'] span {{ color: {text_color} !important; }}",
    "div.stButton > button p { font-size: inherit !important; line-height: 1.25 !important; margin: 0 !important; }",
    "div[data-testid='stHorizontalBlock']:has(.qa-marker) { flex-wrap: nowrap !important; justify-content: safe center; gap: 0.65rem !important; overflow-x: auto; padding: 8px 4px 12px 4px; scrollbar-width: none; animation: fadeUp 0.8s ease-out 0.24s both; }",
    "div[data-testid='stHorizontalBlock']:has(.qa-marker)::-webkit-scrollbar { display: none; }",
    "div[data-testid='stHorizontalBlock']:has(.qa-marker) > div { flex: 0 0 auto !important; width: auto !important; min-width: 0 !important; }",
    "div[data-testid='stElementContainer']:has(.qa-marker), div.element-container:has(.qa-marker) { display: none !important; }",
    f"div[data-testid='stHorizontalBlock']:has(.qa-marker) button {{ background: {pill_bg} !important; border: 1px solid {input_border} !important; color: {text_color} !important; padding: 0.5rem 1.15rem !important; font-size: 0.85rem !important; font-weight: 600 !important; white-space: nowrap !important; }}",
    "div[data-testid='stHorizontalBlock']:has(.qa-marker) button:hover { background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(236,72,153,0.14)) !important; border-color: #a855f7 !important; transform: translateY(-3px) scale(1.03) !important; }",
    "div[data-testid='stHorizontalBlock']:has(.topbar-marker) { position: fixed !important; top: 20px; right: 28px; width: 270px !important; max-width: calc(100vw - 200px); gap: 10px !important; flex-wrap: nowrap !important; z-index: 99999; }",
    "div[data-testid='stHorizontalBlock']:has(.topbar-marker) > div { flex: 1 1 0 !important; min-width: 0 !important; width: auto !important; }",
    "div[data-testid='stElementContainer']:has(.topbar-marker), div.element-container:has(.topbar-marker) { display: none !important; }",
    "[data-testid='stBottom'], [data-testid='stBottom'] > div { background: transparent !important; }",
    ".notice-short { display: none; }",
    f".disclaimer-footer {{ position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; font-size: 0.73rem; color: {muted_text}; z-index: 10; pointer-events: none; background: {footer_bg}; backdrop-filter: blur(8px); padding: 5px; }}",
    "@media (max-width: 640px) {",
    "  .block-container { padding-top: 4.8rem !important; padding-left: 1rem !important; padding-right: 1rem !important; padding-bottom: 6rem !important; }",
    "  .fixed-top-nav { top: 14px; left: 12px; right: 12px; }",
    "  .logo-badge { padding: 5px 12px; font-size: 0.8rem; }",
    "  .logo-icon-circle { display: none; }",
    "  div[data-testid='stHorizontalBlock']:has(.topbar-marker) { top: 14px; right: 12px; width: 220px !important; max-width: none; gap: 6px !important; }",
    "  div[data-testid='stHorizontalBlock']:has(.topbar
