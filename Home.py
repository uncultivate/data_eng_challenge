import streamlit as st
import datetime
import time
import pandas as pd
import textwrap
import inspect
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import unittest

st.set_page_config(
    page_title="Data Eng Challenge",
    page_icon="📈",
)

# if 'entrants' not in st.session_state:
# Load credentials from Streamlit secrets
credentials_info = {
    "type": st.secrets["gcp_service_account"]["type"],
    "project_id": st.secrets["gcp_service_account"]["project_id"],
    "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
    "private_key": st.secrets["gcp_service_account"]["private_key"],
    "client_email": st.secrets["gcp_service_account"]["client_email"],
    "client_id": st.secrets["gcp_service_account"]["client_id"],
    "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
    "token_uri": st.secrets["gcp_service_account"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
    "universe_domain": st.secrets["gcp_service_account"]["universe_domain"],
}

# Create the credentials object
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info)

# Connect to Google Sheets
gc = gspread.authorize(credentials)
sh = gc.open("Submissions")
# Change the int depending on what month the competition is up to
worksheet = sh.get_worksheet(6)
entrants = worksheet.col_values(1)
emojis = worksheet.col_values(4)
st.session_state.entrants = entrants
st.session_state.emojis = emojis


st.header("Data Engineers' Coding Challenge #7")
st.title("Macrodata Refinement")
# Use the retro computer monitor HTML and CSS
html_content = '''
<div class="background">
    <div class="scene-container">
      <div class="scene">
        <div class="monitor">
          <div class="monitor__outer-frame"></div>
          <div class="monitor__frame-border"></div>
          <div class="monitor__frame"></div>
          <div class="monitor__bevel"></div>
        </div>
        <div class="screen-frame"></div>
        <div class="screen">
          <div class="reflection-panels">
            <div class="reflection-panel reflection-panel__left reflection-panel__1"></div>
            <div class="reflection-panel reflection-panel__right reflection-panel__2"></div>
            <div class="reflection-panel reflection-panel__left reflection-panel__3"></div>
            <div class="reflection-panel reflection-panel__left reflection-panel__4"></div>
            <div class="reflection-panel reflection-panel__right reflection-panel__5"></div>
            <div class="reflection-panel reflection-panel__right reflection-panel__6"></div>
            <div class="reflection-panel reflection-panel__left reflection-panel__7"></div>
            <div class="reflection-panel reflection-panel__left reflection-panel__8"></div>
            <div class="reflection-panel reflection-panel__right reflection-panel__9"></div>
            <div class="reflection-panel reflection-panel__right reflection-panel__10"></div>
          </div>
          <div class="screen-text">
            <h1>
              <span class="screen-text__spacer"></span>
              <span class="screen-text__spacer"></span>
              <span>W</span>
              <span>E</span>
              <span>L</span>
              <span>C</span>
              <span>O</span>
              <span>M</span>
              <span>E</span>
              <span class="screen-text__spacer"></span>
              <span>A</span>
              <span>B</span>
              <span>S</span>
              <span class="screen-text__spacer"></span>
              <span class="screen-text__spacer"></span>
              <span>D</span>
              <span>A</span>
              <span>T</span>
              <span>A</span>
              <span class="screen-text__spacer"></span>
              <span>E</span>
              <span>N</span>
              <span>G</span>
              <span>I</span>
              <span>N</span>
              <span>E</span>
              <span>E</span>
              <span>R</span>
              <span>S</span>

            </h1>
          </div>
        </div>
        <div class="cam"></div>
        <div class="input-hole"></div>
        <p class="input-text">ON - BRIGHT</p>
        <div class="side-nob side-nob__left"></div>
        <div class="side-nob side-nob__right"></div>
        <div class="base">
          <div class="base__top"></div>
          <div class="base__bottom"></div>
          <div class="base__bottom-shadow"></div>
        </div>
      </div>
    </div>
  </div>
'''

css_content = '''
/*-----------------------------
Approach inspo - https://css-tricks.com/advice-for-complex-css-illustrations/
-----------------------------*/

:root {
    --size: 280;
    --unit: calc((var(--size) / 1000) * 1vmin);
    --w: 1000;
    --h: 514;
  
    /* Colors */
    --color-text: #d4fdff;
    --color-screen: #00203a;
    --color-reflection: #085e8a;
    --color-monitor-frame: #06284e;
    --color-monitor-frame-dark: #104267;
    --color-monitor-outer: #e1ddd2;
    --color-monitor-bevel: #fefefe;
    --color-monitor-shadow: #afa488;
    --color-text-glow: #24e4f2;
    --color-input-text: #9fbde0;
    --color-input-border: #464448;
    --color-base: #a49475;
    --color-base-light: #b0a589;
    --color-base-lighter: #d2cab7;
    --color-base-lightest: #e7ddda;
  }
  
  /* Responsive sizing */
  @media (max-width: 1000px) {
    :root {
      --size: 180;
    }
  }
  
  /*-----------------------------
  Scene
  -----------------------------*/
  
  body {
    margin: 0;
    padding: 0;
  }
  
  .background {
    background: transparent;  
    overflow: hidden;
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    padding: 0;
  }
  
  .scene-container {
    position: relative;
    width: calc(var(--w) * var(--unit));
    height: calc(var(--h) * var(--unit));
    max-width: 100%;
  }
  
  .scene {
    position: absolute;
    z-index: 10;
    width: 100%;
    height: 100%;
  }
  
  .scene *,
  .scene *:after,
  .scene *:before {
    box-sizing: border-box;
    position: absolute;
  }
  
  .scene-container img {
    opacity: 0;
  }
  
  /*-----------------------------
  Monitor
  -----------------------------*/
  
  .monitor__frame {
    width: calc(561 * var(--unit));
    height: calc(276 * var(--unit));
    top: calc(78 * var(--unit));
    left: calc(210 * var(--unit));
    border-top-left-radius: calc(13 * var(--unit)) calc(50 * var(--unit));
    background: linear-gradient(
        180deg,
        rgba(255, 255, 255, 0.1),
        transparent 4%,
        transparent 96%,
        rgba(255, 255, 255, 0.2)
      ),
      linear-gradient(
        180deg,
        var(--color-monitor-frame) 80%,
        var(--color-monitor-frame-dark)
      );
    border-bottom-left-radius: calc(12 * var(--unit)) calc(50 * var(--unit));
    opacity: 1;
    border-top-right-radius: calc(13 * var(--unit)) calc(50 * var(--unit));
    border-bottom-right-radius: calc(13 * var(--unit)) calc(50 * var(--unit));
  }
  
  .monitor__frame-border {
    width: calc(595 * var(--unit));
    height: calc(313 * var(--unit));
    top: calc(60 * var(--unit));
    left: calc(193 * var(--unit));
    border-top-left-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
    background: black;
    border-bottom-left-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
    opacity: 1;
    border-top-right-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
    border-bottom-right-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
  }
  
  .monitor__outer-frame {
    width: calc(614 * var(--unit));
    height: calc(352 * var(--unit));
    top: calc(51 * var(--unit));
    left: calc(183 * var(--unit));
    border-top-left-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
    background: var(--color-monitor-outer);
    border-bottom-left-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
    opacity: 1;
    border-top-right-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
    border-bottom-right-radius: calc(22 * var(--unit)) calc(60 * var(--unit));
  }
  
  .monitor__bevel {
    width: calc(558 * var(--unit));
    height: calc(19 * var(--unit));
    top: calc(373 * var(--unit));
    left: calc(211 * var(--unit));
    border-top-left-radius: 0;
    background: var(--color-monitor-bevel);
    border-bottom-left-radius: calc(45 * var(--unit)) calc(60 * var(--unit));
    opacity: 1;
    border-top-right-radius: 0;
    border-bottom-right-radius: calc(45 * var(--unit)) calc(60 * var(--unit));
    box-shadow: 1px 1px 3px var(--color-monitor-shadow);
  }
  
  /*-----------------------------
  Screen
  -----------------------------*/
  
  .screen-frame {
    width: calc(363 * var(--unit));
    height: calc(255 * var(--unit));
    top: calc(86 * var(--unit));
    left: calc(230 * var(--unit));
    border-top-left-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    background: black;
    border-bottom-left-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    opacity: 1;
    border-top-right-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    border-bottom-right-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    box-shadow: #ffffff 0 0.9px 3px inset;
  }
  
  .screen {
    width: calc(340 * var(--unit));
    height: calc(235 * var(--unit));
    top: calc(95 * var(--unit));
    left: calc(243 * var(--unit));
    border-top-left-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    background: var(--color-screen);
    border-bottom-left-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    opacity: 1;
    border-top-right-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    border-bottom-right-radius: calc(40 * var(--unit)) calc(64 * var(--unit));
    box-shadow: black -7px 9px 22px 1px inset;
  }
  
  /*-----------------------------
  Reflection Panels
  -----------------------------*/
  
  .reflection-panel {
    background: linear-gradient(
      180deg,
      transparent 10%,
      var(--color-reflection) 30%,
      var(--color-reflection) 70%,
      transparent
    );
    --left-side-transform: rotate(-20deg) skew(0, 20deg);
    --right-side-transform: rotate(20deg) skew(0, -20deg);
  
    /* Top row (1,2) */
    --top-row-width: calc(80 * var(--unit));
    --top-row-height: calc(67 * var(--unit));
    --top-row-top: calc(-19 * var(--unit));
    --top-row-opacity: 0.5;
  
    /* Middle row (3,4,5,6) */
    --mid-row-top: calc(48 * var(--unit));
    --mid-row-height: calc(52 * var(--unit));
    --mid-row-opacity: 0.3;
    --mid-row-blur: 5px;
  
    /* Bottom row (7,8,9,10) */
    --bottom-row-top: calc(105 * var(--unit));
    --bottom-row-height: calc(36 * var(--unit));
    --bottom-row-opacity: 0.2;
    --bottom-row-blur: 7px;
  }
  
  /* Sides */
  .reflection-panel__left {
    transform: var(--left-side-transform);
  }
  
  .reflection-panel__right {
    transform: var(--right-side-transform);
  }
  
  /* Top row panels */
  .reflection-panel__1,
  .reflection-panel__2 {
    width: var(--top-row-width);
    height: var(--top-row-height);
    top: var(--top-row-top);
    opacity: var(--top-row-opacity);
  }
  
  .reflection-panel__1 {
    left: calc(28 * var(--unit));
    filter: blur(5px);
  }
  
  .reflection-panel__2 {
    left: calc(219 * var(--unit));
    filter: blur(3px);
  }
  
  /* Middle row panels */
  .reflection-panel__3,
  .reflection-panel__4,
  .reflection-panel__5,
  .reflection-panel__6 {
    top: var(--mid-row-top);
    height: var(--mid-row-height);
    opacity: var(--mid-row-opacity);
    filter: blur(var(--mid-row-blur));
  }
  
  .reflection-panel__3 {
    width: calc(40 * var(--unit));
    left: calc(-13 * var(--unit));
  }
  
  .reflection-panel__4,
  .reflection-panel__5 {
    width: calc(74 * var(--unit));
  }
  
  .reflection-panel__4 {
    left: calc(54 * var(--unit));
  }
  
  .reflection-panel__5 {
    left: calc(199 * var(--unit));
  }
  
  .reflection-panel__6 {
    width: calc(40 * var(--unit));
    left: calc(305 * var(--unit));
  }
  
  /* Bottom row panels */
  .reflection-panel__7,
  .reflection-panel__8,
  .reflection-panel__9,
  .reflection-panel__10 {
    top: var(--bottom-row-top);
    height: var(--bottom-row-height);
    opacity: var(--bottom-row-opacity);
    filter: blur(var(--bottom-row-blur));
  }
  
  .reflection-panel__7 {
    width: calc(50 * var(--unit));
    left: calc(5 * var(--unit));
  }
  
  .reflection-panel__8,
  .reflection-panel__9,
  .reflection-panel__10 {
    width: calc(65 * var(--unit));
  }
  
  .reflection-panel__8 {
    left: calc(80 * var(--unit));
  }
  
  .reflection-panel__9 {
    left: calc(189 * var(--unit));
  }
  
  .reflection-panel__10 {
    left: calc(280 * var(--unit));
  }
  
  /*-----------------------------
  Screen Text
  -----------------------------*/
  
  .screen-text {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    overflow: hidden;
  }
  
  .screen-text h1 {
    position: relative;
    text-align: center;
    width: 100%;
    text-shadow: 0 0 7px var(--color-text-glow);
    font-size: calc(13 * var(--unit));
    transform: translate(0);
    letter-spacing: 0.3em;
    font-family: 'Orbitron', sans-serif;
    color: var(--color-text);
    font-weight: 700;
  }
  
  .screen-text h1 span {
    display: inline-block;
    position: relative;
    transform: translateX(calc(350 * var(--unit)));
    animation: cobelSlide 10s ease-in-out forwards infinite;
  }
  
  @keyframes cobelSlide {
    0% {
      transform: translateX(calc(350 * var(--unit)));
    }
    30% {
      transform: translateX(0vw);
    }
    70% {
      transform: translateX(0vw);
    }
    100% {
      transform: translateX(calc(-350 * var(--unit)));
    }
  }
  
  .screen-text h1 span:nth-child(1) {
    animation-delay: 0s;
  }
  
  .screen-text h1 span:nth-child(2) {
    animation-delay: 0.1s;
  }
  
  .screen-text h1 span:nth-child(3) {
    animation-delay: 0.2s;
  }
  
  .screen-text h1 span:nth-child(4) {
    animation-delay: 0.3s;
  }
  
  .screen-text h1 span:nth-child(5) {
    animation-delay: 0.4s;
  }
  
  .screen-text h1 span:nth-child(6) {
    animation-delay: 0.5s;
  }
  
  .screen-text h1 span:nth-child(7) {
    animation-delay: 0.6s;
  }
  
  .screen-text h1 span:nth-child(8) {
    animation-delay: 0.7s;
  }
  
  .screen-text h1 span:nth-child(9) {
    animation-delay: 0.8s;
  }
  
  .screen-text h1 span:nth-child(10) {
    animation-delay: 0.9s;
  }
  
  .screen-text h1 span:nth-child(11) {
    animation-delay: 1.0s;
  }
  
  .screen-text h1 span:nth-child(12) {
    animation-delay: 1.1s;
  }
  
  .screen-text h1 span:nth-child(13) {
    animation-delay: 1.2s;
  }
  
  .screen-text h1 span:nth-child(14) {
    animation-delay: 1.3s;
  }
  
  .screen-text h1 span:nth-child(15) {
    animation-delay: 1.4s;
  }
  
  .screen-text h1 span:nth-child(16) {
    animation-delay: 1.5s;
  }
  
  .screen-text h1 span:nth-child(17) {
    animation-delay: 1.6s;
  }
  
  .screen-text h1 span:nth-child(18) {
    animation-delay: 1.7s;
  }
  
  .screen-text h1 span:nth-child(19) {
    animation-delay: 1.8s;
  }
  
  .screen-text h1 span:nth-child(20) {
    animation-delay: 1.9s;
  }
  
  .screen-text__spacer {
    margin-right: 8px;
  }
  
  /*-----------------------------
  Cam
  -----------------------------*/
  
  .cam {
    width: calc(20 * var(--unit));
    height: calc(20 * var(--unit));
    top: calc(65 * var(--unit));
    left: calc(400 * var(--unit));
    background: #06284e;
    border-radius: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 1px 1px 20px black inset;
    border: 2px solid #06284e;
  }
  
  .cam:after {
    content: '';
    background: linear-gradient(148deg, red 5%, transparent);
    width: 30%;
    height: 30%;
    display: block;
    border-radius: 100%;
    animation: camBlink 2s linear infinite;
  }
  
  @keyframes camBlink {
    0% {
      opacity: 0.3;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.3;
    }
  }
  
  /*-----------------------------
  Base
  -----------------------------*/
  
  .base__top {
    width: calc(200 * var(--unit));
    height: calc(25 * var(--unit));
    top: calc(403 * var(--unit));
    left: calc(392 * var(--unit));
    background: linear-gradient(
        180deg,
        transparent 48%,
        black 48%,
        black 51%,
        transparent 51%,
        transparent
      ),
      radial-gradient(#e9ded9, transparent);
    background-color: var(--color-base);
    opacity: 1;
    overflow: hidden;
  }
  
  .base__top:before {
    content: '';
    background: white;
    width: 100%;
    height: 100%;
    transform: translate(-97%, 0);
    border-radius: calc(5 * var(--unit));
  }
  
  .base__top:after {
    content: '';
    background: white;
    width: 100%;
    height: 100%;
    transform: translate(97%, 0);
    border-radius: calc(5 * var(--unit));
  }
  
  .base__bottom {
    width: calc(580 * var(--unit));
    height: calc(49 * var(--unit));
    top: calc(419 * var(--unit));
    left: calc(194 * var(--unit));
    background-color: var(--color-base-lighter);
    opacity: 1;
    overflow: hidden;
    clip-path: polygon(35% 18%, 68% 18%, 100% 78%, 100% 100%, 0 100%, 0 78%);
  }
  
  .base__bottom-shadow {
    width: calc(580 * var(--unit));
    height: calc(10 * var(--unit));
    top: calc(460 * var(--unit));
    left: calc(194 * var(--unit));
    background: transparent;
    opacity: 1;
    border-radius: 10px;
  }
  
  /*-----------------------------
  Side Nobs
  -----------------------------*/
  
  .side-nob {
    --nob-width: calc(21 * var(--unit));
    --nob-height: calc(89 * var(--unit));
    --nob-top: calc(167 * var(--unit));
    --nob-gradient: linear-gradient(
      180deg,
      black,
      rgba(255, 255, 255, 0.3) 30%,
      transparent 75%,
      black
    );
    --nob-after-width: calc(10 * var(--unit));
    --nob-after-height: calc(42 * var(--unit));
    --nob-after-top: calc(25 * var(--unit));
  
    width: var(--nob-width);
    height: var(--nob-height);
    top: var(--nob-top);
    background: var(--nob-gradient);
    opacity: 1;
    background-color: black;
  }
  
  .side-nob__left {
    left: calc(152 * var(--unit));
    border-radius: 0 0 0 3px / 0 0 0 20px;
  }
  
  .side-nob.side-nob__left:after {
    content: '';
    width: var(--nob-after-width);
    height: var(--nob-after-height);
    left: 100%;
    top: var(--nob-after-top);
    background: var(--nob-gradient);
    background-color: black;
  }
  
  .side-nob__right {
    left: calc(807 * var(--unit));
    border-radius: 0 0 3px 0 / 0 0 20px 0;
  }
  
  .side-nob.side-nob__right:after {
    content: '';
    width: var(--nob-after-width);
    height: var(--nob-after-height);
    right: 100%;
    top: var(--nob-after-top);
    background: var(--nob-gradient);
    background-color: black;
  }
  
  /*-----------------------------
  Input
  -----------------------------*/
  
  .input-hole {
    width: calc(25 * var(--unit));
    height: calc(25 * var(--unit));
    top: calc(307 * var(--unit));
    left: calc(602 * var(--unit));
    background: black;
    opacity: 1;
    border-radius: 100%;
  }
  
  .input-hole:after {
    border: 1px solid var(--color-input-border);
    content: '';
    width: 50%;
    height: 50%;
    border-radius: 100%;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  
  .input-text {
    color: var(--color-input-text);
    top: calc(290 * var(--unit));
    left: calc(600 * var(--unit));
    font-size: calc(5 * var(--unit));
    mix-blend-mode: lighten;
    opacity: 0.7;
    font-family: 'helvetica';
  }
'''

# Combine HTML and CSS
monitor_html = f'''
<html>
<head>
<style>
{css_content}
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
{html_content}
</body>
</html>
'''

# Set height for the component
st.components.v1.html(monitor_html, height=380)


st.write("It's the first day of your new role as a Data Engineer in the Macrodata Refinement section at the ABS. 'It's restricted down there --like CPI', you overheard someone say. 'What do they actually do?' you enquire. 'Something to do with numbers, I heard... no one really knows.' You figure this sounds like most teams that work at the ABS, so you enter the lift, press the button and then .....")
st.write("... The lift door opens. 'Where am I...?' you wonder. 'Hang on... who am I...?' Ahead are several colleagues working at what look like retro 90s style monitors. 'Your job is to find the mysterious number patterns', says someone who appears to be your new section director. 'They may make you feel weird'.") 
st.write("Sitting down at your new desk, you examine the screen and stare at the array of numbers before you. Suddenly, you notice that the three rows in the top corner contain equal sums. Doing some further mental math, the three columns and diagonals also sum to the same number. It's a magic square! You click in the middle of the 3x3 magic square and it turns green! Points seem to be added to a tally on screen. One of your new colleagues exclaims excitedly, 'It took me 3 weeks to find my first pattern! How did you do it?' You just chuckle and ask 'Do we have access to an IDE with Python on these workstations?'")
st.divider()
st.write("Welcome to the seventh iteration of the Data Engineers' Challenge! This month - we have Macrodata Refinement: a tribute to the popular TV Show - Severance.")
st.write("**Difficulty**: Medium")
st.write("**Coding Skills Required**: Python, working with arrays/matrices in NumPy, algorithm design for search & array traversal, conditional logic")
st.write("**Other Skills**: Understanding of magic squares and creative problem solving")
st.divider()
st.audio("assets/audio/mdr.wav", format="audio/wav", autoplay=False)
url = "https://notebooklm.google.com/"
st.write("Macrodata Refinement as featured on the [Deep Dive Podcast](%s)" %url)
st.divider()



st.subheader("Challenge Details")
"The Data Engineers' Challenge #7 revolves around Magic Square Detection in a NumPy array. This challenge will be contested by entrants who submit functions in Python containing search strategy logic."
"""In the Magic Square Detection challenge:
- Develop search strategies navigate through a partially revealed grid and find hidden magic squares
- Ensure your search algorithm can handle grids of different sizes (10x10, 20x20 and 30x30), different quantities of magic squares, and different search step limits. 
- You will be awarded points for each magic square found, as well as an efficiency bonus that rewards completing the challenge with fewer moves, and a completion bonus that rewards complete detection of all magic squares. 
"""


st.subheader("Function Requirements")
st.write("Example Strategy:")
code = '''
def magic_square_search_strategy(grid, window_coords):
    """
    Custom search strategy to find magic squares in a partially revealed grid
    Args:
        grid: 2D numpy array with NaN for unexplored cells and inf for known magic squares. You can use isnan() and isinf() to check for these values.
        window_coords: Tuple containing window coordinates ((min_row, min_col), (max_row, max_col))
    Returns:
        str: Direction to move next ('up', 'down', 'left', 'right')
    """
    import numpy as np
    
    # Extract window coordinates
    (min_row, min_col), (max_row, max_col) = window_coords
    
    # Get current window dimensions and center
    window_height = max_row - min_row + 1
    window_width = max_col - min_col + 1
    center_row = min_row + window_height // 2
    center_col = min_col + window_width // 2
    
    # Get number of rows and columns in the grid
    rows, cols = grid.shape
    
    # Your search logic goes here
    
    # Return a direction to move in
    return 'down'
'''
st.code(code, language='python')

### Important Properties
st.markdown("""
Function requirements:
- Your function should accept a grid parameter and a window_coords parameter
- It should return a direction to move in ('up', 'down', 'left', 'right')
- Magic squares are 3x3 grids or 5x5 grids where the sum of the numbers in each row, column, and diagonal are the same. If the centre of your search window crosses the centre of a magic squares, it registers as found.
- Unexplored areas are represented by NaNs in your NumPy array and known magic squares are represented by Infinity (inf). You can use isnan() and isinf() to check for these values in the grid.
- Enable logging to view detailed logs in the developer console of your browser.
""")

# Define challenge dates
# Countdown timer

aest = timezone('Australia/Sydney')
submission_close_date = aest.localize(datetime.datetime(2025, 4, 3, 23, 59, 59))
submission_run_date = aest.localize(datetime.datetime(2025, 4, 4, 15, 0, 0))

current_time = datetime.datetime.now(aest)
remaining_time = submission_close_date - current_time

# Format dates for display
close_date_str = submission_close_date.strftime("%A, %d/%m at %I:%M %p AEDT")
run_date_str = submission_run_date.strftime("%A, %d/%m at %I:%M %p AEDT")

st.divider()

st.write(f"""The challenge submission will close on {close_date_str}. The game will be run and broadcast on Teams on {run_date_str}. Good luck!
""")




st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #7")
if remaining_time.total_seconds() > 0:
    if remaining_time.days == 1:
        st.sidebar.write(f"Submissions close in {remaining_time.days} day, {remaining_time.seconds // 3600} hours and "
                     f"{(remaining_time.seconds // 60) % 60} minutes.")
    else:
        st.sidebar.write(f"Submissions close in {remaining_time.days} days, {remaining_time.seconds // 3600} hours and "
                     f"{(remaining_time.seconds // 60) % 60} minutes.")
else:
    st.sidebar.write("Submissions Closed")

# Submission form

if remaining_time.total_seconds() > 0:
    st.subheader("Submit your code")
    name = st.text_input("Name", placeholder="Enter your name with format First Name + Surname Initial, i.e. Mark S")
    #emoji = st.text_input("Emoji", placeholder="Paste your emoji here")
    email = st.text_input("Email (optional: Be notified of and invited to future challenges)", help="Get notified of new challenges and get invited to results livestreams")
    function_code = st.text_area("Function Code (Paste your Python code here)", placeholder=code)

    if st.button("Submit"):
        if name and function_code:
            num_entrants = len(st.session_state.entrants)
            worksheet.update_cell(num_entrants + 1, 1, name)
            #worksheet.update_cell(num_entrants + 1, 4, emoji)
            if email:
                worksheet.update_cell(num_entrants + 1, 2, email)
            worksheet.update_cell(num_entrants + 1, 3, function_code)
            st.success("Submission successful!")

        else:
            st.error("Please provide both name and function code.")
else:
    st.header("Submissions are now closed.")


# Display current entrants
st.sidebar.divider()
st.sidebar.header("Current Entrants")
for entrant in st.session_state.entrants:
    st.sidebar.markdown(
        f"<div style='display: flex; align-items: center; gap: 8px;'>"
        f"<div style='font-size: 16px'>{entrant}</div>"
        f"</div>", 
        unsafe_allow_html=True
    )
# Contact
st.sidebar.divider()
st.sidebar.header("Contact")
st.sidebar.write("Jono Sheahan")