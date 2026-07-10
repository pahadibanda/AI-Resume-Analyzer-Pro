import streamlit as st


def render_metric_cards():

    st.markdown("## 📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("🎯 ATS Score", "87%", "Excellent Resume"),
        ("📄 Resume Review", "AI Ready", "Powered by AI"),
        ("💼 JD Match", "82%", "Strong Match"),
        ("🎤 Questions", "20", "Ready to Practice"),
    ]

    for col, card in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(
                f"""
<div class="metric-card">
    <div class="metric-title">{card[0]}</div>
    <div class="metric-value">{card[1]}</div>
    <div class="metric-sub">{card[2]}</div>
</div>
""",
                unsafe_allow_html=True,
            )