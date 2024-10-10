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
worksheet = sh.get_worksheet(3)
entrants = worksheet.col_values(1)
st.session_state.entrants = entrants

st.title("Data Engineers' Coding Challenge #4: The Beast from 3 East")

# Challenge description
st.write("""
    It is late in the ABS Canberra Office one Friday evening, where the Data Engineers are all working overtime. Suddenly, the power goes out and there is a crash as a large shape crashes through the glass door of the skybridge.   
""")

st.image('assets/img/beast.jpg', width=704)
st.write("A huge beast has escaped from confinement by Home Affairs on level 3 to wreak havoc and now stalks the terrified data engineer team as they weigh up their options. Taking on the beast single-handed is not an option. Can they evade the beast until it loses interest and leaves? Will it leave once its hunger is satiated?")
st.divider()
st.audio("assets/audio/monster_hunt_deep_dive.wav", format="audio/wav", autoplay=False)
url = "https://notebooklm.google.com/"
st.write("The Beast from 3 East featured on the [Deep Dive Podcast](%s)" %url)
st.divider()



st.subheader("Challenge Details")
"1. Game grid: The challenge will take place on a grid of size (width * height), given as a tuple of integers."
"2. Entities: Each data engineer will be represented by an emoji on the game board that bears their name and follows their function's logic. The beast will be represented by a 👹 emoji. If the beast reaches the same grid space as an engineer, they will become a zombie, represented by a 🧟 emoji, and the entity logic will follow that of the beast."
"3. Objective: Survive as long as possible! The game will continue until a pre-determined time limit, OR until there is only 1 engineer remaining."
"4. Scoring: The challenge will be played a total of three times to ensure that results are not determined entirely by luck! The first engineer to become a zombie will receive 1 point, the second will receive 2 and so on. Any engineers remaining at end game will receive a bonus 3 points."
"5. Movement: The challenge is turn based with each engineer able to move one grid-space per turn (up, down, left, right). The beast will start slow but gradually pick up the pace and will eventually move one EXTRA space every five turns. Zombies move slower, moving once every two turns. Note: Multiple entities may occupy the same space at once"
"6. Detection Radius: Engineers have full visibility over the office (the game board) and are given the positions of themselves, plus all the other engineers and beast/zombies. The beast and any zombies have a detection radius of 5, calculated using the Euclidean distance between entities"

st.subheader("Function Requirements")
st.write("1. Parameters: Your function will receive the following inputs:")
st.markdown("""
- `self_pos` (Position): The current position of Alice on the grid, represented as a tuple (x, y).
- `beast_positions` (List[Position]): A list of tuples, each representing the position of a beast/zombie (x, y). The position of the beast is always at the first index position in the list. 
- `other_engineers` (List[Position]): A list of tuples, each representing the position of another engineer (x, y). This list may be empty if no other engineers are present.
- `grid_size` (Tuple[int, int]): A tuple representing the dimensions of the grid (width, height).
""")
st.write("2. Suggested logic:")
st.markdown("""
- Step 1: Code a helper function to determine if a move is valid (i.e. always within the grid boundaries)
- Step 2: Implement logic to move your engineer away from the beast/zombies
- Step 3 (Optional): Consider how you could use the positions of other engineers to your advantage
""")

st.write("3. Returns:")
st.markdown("""
- Direction: The direction in which Alice should move. The possible directions are:
  - 'up' (move to the position above)
  - 'right' (move to the right)
  - 'down' (move to the position below)
  - 'left' (move to the left)
  - None (stay in place if no valid move or no need to move)
""")



st.subheader("Submission Template")
st.write("Below is a template you can use to create your function. Replace the placeholder logic with your strategy.")

code = """
Position = Tuple[int, int]
Direction = Optional[str]

def engineer_ai(self_pos: Position, beast_positions: List[Position], other_engineers: List[Position], grid_size: Tuple[int, int]) -> Direction:
    # Implement movement logic here

    # Or stumble blindly around the office...
    direction = random.choice(['up', 'down', 'left', 'right'])
    return direction"""
st.code(code, language='python')

# Define challenge dates
# Countdown timer

aest = timezone('Australia/Sydney')
submission_close_date = aest.localize(datetime.datetime(2024, 10, 24, 23, 59, 59))
submission_run_date = aest.localize(datetime.datetime(2024, 10, 25, 15, 0, 0))

current_time = datetime.datetime.now(aest)
remaining_time = submission_close_date - current_time

# Format dates for display
close_date_str = submission_close_date.strftime("%A, %d/%m at %I:%M %p ADST")
run_date_str = submission_run_date.strftime("%A, %d/%m at %I:%M %p ADST")

st.write(f"""Your task is to write a Python function that meets the specified requirements. 

The challenge submission will close on {close_date_str}. The game will be run and broadcast on Teams on {run_date_str}. Good luck!
""")




st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #4")
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
placeholder1 = """def engineer_ai(self_pos: Position, beast_positions: List[Position], other_engineers: List[Position], grid_size: Tuple[int, int]) -> Direction:
    # Implement movement logic here

    # Or stumble blindly around the office...
    direction = random.choice(['up', 'down', 'left', 'right'])
    return direction"""

if remaining_time.total_seconds() > 0:
    st.subheader("Submit your code")
    name = st.text_input("Name", placeholder="Short and sweet please!")
    email = st.text_input("Email (optional)", help="Get notified of new challenges and get invited to results livestreams")
    function_code = st.text_area("Function Code (Paste your Python code here)", placeholder=placeholder1)

    if st.button("Submit"):
        if name and function_code:
            num_entrants = len(st.session_state.entrants)
            worksheet.update_cell(num_entrants + 1, 1, name)
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
    st.sidebar.write(f"- {entrant}")

# Contact
st.sidebar.divider()
st.sidebar.header("Contact")
st.sidebar.write("Jono Sheahan")