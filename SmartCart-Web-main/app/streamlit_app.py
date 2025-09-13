import os
import pickle
import math
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from typing import Optional

from data_loader import (
    ensure_dirs, load_csvs, build_items_and_tags, build_normalized_comatrix,
    save_artifact, load_artifact
)
from recommender import enhanced_recommend, batch_predict, normalize_user_items
from ui_components import (
    icon_for_item, TYPE_EMOJI, chip, card, header, topbar_badges, reco_card
)

APP_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
ART_DIR = os.path.join(BASE_DIR, "artifacts")

st.set_page_config(
    page_title="SmartCart Web — Menu Recommender",
    page_icon="🍗",
    layout="wide"
)

# ===== Load base CSS =====
with open(os.path.join(APP_DIR, "styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== Theme toggle (Light / Dark) =====
if "theme_dark" not in st.session_state:
    st.session_state.theme_dark = False

st.sidebar.title("🍟 SmartCart Web")
st.sidebar.markdown("### Theme")
st.session_state.theme_dark = st.sidebar.checkbox("🌙 Dark mode", value=st.session_state.theme_dark)

def inject_dark_theme(is_dark: bool) -> None:
    """Inject CSS variable overrides for dark mode (matches styles.css variables)."""
    if not is_dark:
        return
    dark_css = """
    <style>
    :root{
      --bg: #0f1115;
      --text: #f5f7fa;
      --muted: #cbd5e1;

      --card-bg: #151922;
      --card-border: rgba(255,255,255,0.10);
      --card-shadow: 0 8px 24px rgba(0,0,0,0.6);
      --card-shadow-hover: 0 12px 28px rgba(0,0,0,0.7);

      --chip-bg: #2a2f3a;
      --chip-border: #566076;
      --chip-text: #e5e7eb;

      --badge-bg: #1f2a44;
      --badge-border: #395b9b;
      --badge-text: #c6ddff;

      --gold: #f59f00;
      --silver: #adb5bd;
      --bronze: #cc8e52;

      --rank-text: #000000; /* medal digits remain black for contrast */
      --header-bg: #1e293b;
      --header-text: #ffffff;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)

inject_dark_theme(st.session_state.theme_dark)

# ===== Sidebar (site nav) =====
page = st.sidebar.radio("Navigate", [
    "🏁 Start",
    "🧱 Build Model (first run)",
    "🛒 Menu & Recommendations",
    "📦 Batch Predict (CSV)",
    "📊 Metrics & Explore",
    "ℹ️ About"
])

@st.cache_data(show_spinner=False)
def load_all_csvs():
    return load_csvs()

@st.cache_data(show_spinner=True)
def prepare_artifacts(sample_n: Optional[int]):
    dfs = load_all_csvs()
    order = dfs["order"].copy()

    # Parse & clean items
    from data_loader import extract_item_names, clean_item_list
    order["ITEM_LIST"] = order["ORDERS"].apply(extract_item_names).apply(clean_item_list)

    # Build artifacts (same logic as before)
    item_type, item_feat, top_by_type, all_items = build_items_and_tags(order)
    co_norm = build_normalized_comatrix(order, sample_n=sample_n)

    known_lower = {itm.lower(): itm for itm in all_items}
    known_items_lower = list(known_lower.keys())

    art = {
        "item_type": item_type,
        "item_feat": item_feat,
        "top_by_type": top_by_type,
        "co_norm": co_norm,
        "known_items_lower": known_items_lower,
        "lower_to_orig": known_lower
    }
    save_artifact("artifacts.pkl", art)
    return art

def load_or_build_artifacts():
    art = load_artifact("artifacts.pkl")
    if art is None:
        st.warning("Artifacts not found. Go to **Build Model (first run)**.")
        return None
    return art

def start_page():
    st.markdown("<div class='dark-header'>🍗 SmartCart Web — Menu Recommender</div>", unsafe_allow_html=True)
    st.write("Select **up to 3 items** from a **menu**, get **top-3 recommendations**. All logic identical to the previous system.")
    st.info("Put your CSVs under `data/`, then build the model once. Recommendations are purely cart-based (no user identity).")

    try:
        dfs = load_all_csvs()
    except Exception as e:
        st.error(f"CSV load error: {e}")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Orders", f"{len(dfs['order']):,}")
    col2.metric("Customers", f"{len(dfs['customer']):,}")
    col3.metric("Stores", f"{len(dfs['store']):,}")
    col4.metric("Test Rows", f"{len(dfs['test']):,}")

    st.markdown("---")
    header("Quick steps", "🧭")
    st.markdown("1) **Build Model** → 2) **Menu & Recommendations** → 3) (Optional) **Batch Predict**")

def build_model_page():
    st.markdown("<div class='dark-header'>🧱 Build Model (first run)</div>", unsafe_allow_html=True)
    st.write("Computes normalized co-occurrence + item tagging. Cached to disk for fast reuse.")

    sample = st.slider(
        "Sample N orders (speed vs quality)",
        100_000, 1_414_410, 250_000, step=50_000,
        help="Use 200–300k for fast dev. Full dataset if you have RAM/Time."
    )
    if st.button("🚀 Build now"):
        with st.spinner("Crunching pairs & normalizing..."):
            _ = prepare_artifacts(sample_n=sample)
        st.success("Artifacts built and cached to `artifacts/artifacts.pkl`")

def menu_reco_page():
    st.markdown("<div class='dark-header'>🛒 Menu & Recommendations</div>", unsafe_allow_html=True)
    art = load_or_build_artifacts()
    if art is None:
        return

    item_type, item_feat = art["item_type"], art["item_feat"]
    top_by_type, co_norm = art["top_by_type"], art["co_norm"]
    known_items_lower, lower_to_orig = art["known_items_lower"], art["lower_to_orig"]

    all_items = list(lower_to_orig.values())

    # MENU BAR: multiselect (limit 3)
    st.caption("Menu (pick up to 3 items):")
    selected = st.multiselect(
        "Select items",
        options=all_items,
        default=[],
        help="Start typing to search. You can choose at most 3."
    )

    # Hard cap: enforce up to 3
    if len(selected) > 3:
        st.error("You selected more than 3 items. Only the first 3 will be used.")
        selected = selected[:3]

    # Display top bar badges (pretty)
    topbar_badges(selected, limit=3)

    if st.button("🍽️ Recommend", disabled=(len(selected) == 0)):
        # Normalize (same logic)
        cart = normalize_user_items(selected, known_items_lower, lower_to_orig)
        recs = enhanced_recommend(cart, co_norm, item_type, top_by_type, item_feat)

        if not recs:
            st.warning("No recommendations found. Try different items or rebuild the model.")
            return

        # White header on dark bar (visible in light & dark themes)
        st.markdown("<div class='top3-header'>Top 3 Recommendations</div>", unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        cols = [col_a, col_b, col_c]
        for idx, (it, score) in enumerate(recs, start=1):
            t = item_type.get(it, "other")
            with cols[idx - 1]:
                reco_card(idx, it, score, t)

def batch_page():
    st.markdown("<div class='dark-header'>📦 Batch Predict (CSV)</div>", unsafe_allow_html=True)
    art = load_or_build_artifacts()
    if art is None:
        return

    st.caption("Reads `data/test_data_question.csv` and writes output under `artifacts/`")
    if st.button("Run batch on test_data_question.csv"):
        try:
            test_path = os.path.join(DATA_DIR, "test_data_question.csv")
            test_df = pd.read_csv(test_path)
        except Exception as e:
            st.error(f"Cannot read test_data_question.csv: {e}")
            return

        out = batch_predict(
            test_df,
            art["co_norm"], art["item_type"], art["top_by_type"], art["item_feat"],
            art["known_items_lower"], art["lower_to_orig"]
        )
        out_path = os.path.join(ART_DIR, "SmartCart_Recommendation_Output.csv")
        out.to_csv(out_path, index=False)
        st.success(f"Saved: {out_path}")
        st.dataframe(out.head(20))
        with open(out_path, "rb") as f:
            st.download_button(
                "Download CSV", f,
                file_name="SmartCart_Recommendation_Output.csv",
                mime="text/csv"
            )

def metrics_page():
    st.markdown("<div class='dark-header'>📊 Metrics & Explore</div>", unsafe_allow_html=True)
    art = load_or_build_artifacts()
    if art is None:
        return

    # Category distribution
    item_type = art["item_type"]
    counts = Counter(item_type.values())
    st.bar_chart(pd.DataFrame.from_dict(counts, orient="index", columns=["Count"]))

    # Top items by type
    st.markdown("#### Top Items by Type")
    cols = st.columns(4)
    for t, col in zip(["main", "side", "dip", "drink"], cols):
        with col:
            st.markdown(f"**{t.title()}** {TYPE_EMOJI.get(t, '🍽️')}")
            for it, cnt in art["top_by_type"].get(t, [])[:10]:
                st.write(f"{icon_for_item(it)} {it} — {cnt}")

def about_page():
    st.markdown("<div class='dark-header'>ℹ️ About</div>", unsafe_allow_html=True)
    st.write(
"SmartCart – AI-powered upsells that boost revenue & delight customers. "
"Wings R Us guests love speed and variety, but static upsell suggestions feel generic and leave money on the table.\n"
"👉 Customers feel understood.\n"
"👉 Orders get bigger and more satisfying.\n"
"👉 Businesses see higher AOV and happier, loyal guests.\n"
"SmartCart makes upselling smarter, faster, and effortless.\n"
    )

# ===== Routing =====
if page.startswith("🏁"):
    start_page()
elif page.startswith("🧱"):
    build_model_page()
elif page.startswith("🛒"):
    menu_reco_page()
elif page.startswith("📦"):
    batch_page()
elif page.startswith("📊"):
    metrics_page()
else:
    about_page()