import streamlit as st
st.set_page_config(page_title="Hall of Fame", page_icon="🏆")

st.markdown("# 🏆 Hall of Fame 🏆")

st.markdown("#### Past Winners of the Data Engineers' Challenge")

# Challenge 7
with st.expander("**#7: Macrodata Refinement** ([repo link](https://github.com/uncultivate/mdr-main/))"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>James C</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Jake P</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Tony R</p>", unsafe_allow_html=True)
st.divider()

# Challenge 6
with st.expander("**#6: The Dollar Auction** ([repo link](https://github.com/uncultivate/dollar-auction/))"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Not a morning strategy</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Sixbids None The Richer</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Low Risk</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>reckless ryan</p>", unsafe_allow_html=True)
st.divider()

# Challenge 5
with st.expander("**#5: The Regifting Challenge** ([repo link](https://github.com/uncultivate/regifting/))"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Avaricious Rapacity</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>The Grinch</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>revelrous ryan</p>", unsafe_allow_html=True)
st.divider()

# Challenge 4
with st.expander("**#4: The Beast from 3 East** ([repo link](https://github.com/uncultivate/monster-hunt/))"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Leprechaun</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>rapid ryan</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Saboteur</p>", unsafe_allow_html=True)
st.divider()

# Challenge 3
with st.expander("**#3: The UpLift Challenge** ([repo link](https://github.com/uncultivate/elevator-master/))"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Michellevator</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>ASR</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>efficient elevator ryan</p>", unsafe_allow_html=True)
st.divider()

# Challenge 2
with st.expander("**#2: Tulip Coin**"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>ASR</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Volatile</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>tulip tycoon ryan</p>", unsafe_allow_html=True)
st.divider()

# Challenge 1
with st.expander("**#1: The Prisoner's Dilemma Game**"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥇</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>grudge holder</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥈</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>wenng</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center; font-size: 24px;'>🥉</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>the punisher</p>", unsafe_allow_html=True)
