import streamlit as st
from typing import Optional

EMOJI_MAP = [
    (["wing", "wings", "grilled"], "🍗"),
    (["spicy"], "🌶️"),
    (["fries", "voodoo"], "🍟"),
    (["soda", "punch", "drink", "tea", "lager", "root beer"], "🥤"),
    (["dip", "sauce"], "🥣"),
    (["corn"], "🌽"),
    (["veggie", "celery", "carrot"], "🥕"),
    (["cake", "dessert", "choco"], "🍰"),
    (["combo", "feast", "bundle", "lunch", "box", "platter"], "🍱"),
    (["strip", "strips"], "🍗"),
    (["water"], "💧"),
]

TYPE_EMOJI = {
    "main": "🍱",
    "side": "🍟",
    "dip": "🥣",
    "drink": "🥤",
    "other": "🍽️"
}

def icon_for_item(name: str) -> str:
    n = (name or "").lower()
    for keys, emoji in EMOJI_MAP:
        if any(k in n for k in keys):
            return emoji
    return "🍽️"

def chip(text: str) -> None:
    st.markdown(f'<span class="item-chip">{text}</span>', unsafe_allow_html=True)

def card(title: str, subtitle: Optional[str] = None, body: Optional[str] = None) -> None:
    st.markdown('<div class="reco-card">', unsafe_allow_html=True)
    st.markdown(f"**{title}**")
    if subtitle:
        st.caption(subtitle)
    if body:
        st.write(body)
    st.markdown('</div>', unsafe_allow_html=True)

def header(title: str, emoji: str = "🍔") -> None:
    st.markdown(f"### {emoji} {title}")

def topbar_badges(cart, limit: int = 3) -> None:
    st.markdown('<div class="topbar">', unsafe_allow_html=True)
    st.markdown(f'<span class="badge">Pick up to {limit}</span>', unsafe_allow_html=True)
    if cart:
        for x in cart:
            st.markdown(f'<span class="badge">{icon_for_item(x)} {x}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def reco_card(rank: int, item: str, score: float, item_type: str) -> None:
    """Beautiful ranked recommendation card with medal badge."""
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "⭐️")
    emoji = icon_for_item(item)
    type_emoji = TYPE_EMOJI.get(item_type, "🍽️")
    # rank label text
    rank_label = f"Rec {rank}"
    st.markdown(
        f"""
<div class="reco-card">
  <div class="reco-rank reco-rank-{rank}">{rank}</div>
  <div class="reco-title">{emoji} {item}</div>
  <div class="reco-meta">{medal} <b>{rank_label}</b>
    <span class="reco-pill">{type_emoji} {item_type.title()}</span>
    <span class="reco-pill">Confidence <b>{score:.2f}</b></span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )