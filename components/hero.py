import streamlit as st

def render_hero():
    st.markdown(
        """
        <h1 style='text-align:center;
                   font-size:55px;
                   color:white;
                   margin-bottom:0px;'>
            🤖 AI Resume Analyzer Pro
        </h1>

        <p style='text-align:center;
                  font-size:22px;
                  color:#9CA3AF;
                  margin-top:10px;'>
            Land Your Dream Job with AI
        </p>
        """,
        unsafe_allow_html=True,
    )