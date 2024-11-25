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
worksheet = sh.get_worksheet(4)
entrants = worksheet.col_values(1)
emojis = worksheet.col_values(4)
st.session_state.entrants = entrants
st.session_state.emojis = emojis


st.header("Data Engineers' Coding Challenge #5")
st.title("The Regifting Challenge")

# Challenge description
st.write("""
    It is late in the ABS Office on Christmas Eve, where the Data Engineers are all working overtime. Suddenly, there is a crash as a large brown sack crashes through the window and onto the office floor.   
""")

st.image('assets/img/sack.jpg')
st.write("The director tentatively approaches the sack and unlooses the cord. Gifts of all shapes and sizes spill out, the wrapping paper sparkling and colourful. One engineer looks sidewards - 'I take it these don't need to be entered on the departmental gifts registry, right?'. Eyes turn to the director. 'Finders keepers I say! Let's divide up the gifts amongst ourselves. If you're not happy with my proposal, the next person will get a go. Merry Christmas everyone!'")
st.divider()
st.audio("assets/audio/regifting_deep_dive.wav", format="audio/wav", autoplay=False)
url = "https://notebooklm.google.com/"
st.write("The Regifting Challenge featured on the [Deep Dive Podcast](%s)" %url)
st.divider()



st.subheader("Challenge Details")
"The Regifting Challenge is a Python implementation of a multiplayer gift distribution game where players propose and vote on how to distribute gifts. The game explores different strategic approaches to resource allocation and voting behaviour."
"""1. What is a round? Rounds consist of two parts:
    - Proposed distribution of 100 gifts by the director
    - Voting on the proposed distribution
"""
"2. Hierarchy: Each round has a director who proposes how to distribute 100 presents among all players. All players will have the chance to start as director, which means the number of rounds will be equal to the number of challenge entrants. The order of the other players is shuffled each round."
"3. Voting: All players (including the director) vote on the proposed distribution. The director holds the casting vote."
"4. Outcome: If majority accepts (≥50%), the distribution is implemented. If rejected, the director is eliminated (gets 0 presents) and the next player becomes director."
"""5. Game continues until either:
    - A distribution is accepted
    - Only one player remains (who gets all presents)"""


st.subheader("Class Requirements")
st.write("1. Every gifter class must inherit from the base Gifter class and implement two methods:")
code = '''class YourGifter(Gifter):
    def propose_distribution(self, num_gifts: int, num_gifters: int) -> list:
        """
        Create a proposed distribution of gifts. To be used when YOU are the director.
        
        Args:
            num_gifts: Total number of gifts to distribute
            num_gifters: Number of players still in the game
            
        Returns:
            list: Proposed distribution where index represents player position 
                 (0 is self, 1 is next player, etc.)
        """
        pass

    def vote(self, distribution: list, num_gifts: int, num_gifters: int) -> bool:
        """
        Vote on a proposed distribution.
        
        Args:
            distribution: Proposed distribution of gifts
            num_gifts: Total number of gifts
            num_gifters: Number of players still in game
            
        Returns:
            bool: True to accept, False to reject
        """
        pass
'''
st.code(code, language='python')

### Important Properties
st.markdown("""
Your gifter has access to:
- `self.name`: Your gifter's name (automatically assigned)
- `self.seniority`: Current position in the game (0 = director, updates each round)
""")

st.subheader("Access code repo")
st.write("Highly recommended to check this out before submitting. Contains the full game code and example classes.")

    
repo_url = "https://github.com/uncultivate/regifting"

st.link_button("Access code repo", repo_url)


# Define challenge dates
# Countdown timer

aest = timezone('Australia/Sydney')
submission_close_date = aest.localize(datetime.datetime(2024, 12, 5, 23, 59, 59))
submission_run_date = aest.localize(datetime.datetime(2024, 12, 6, 15, 0, 0))

current_time = datetime.datetime.now(aest)
remaining_time = submission_close_date - current_time

# Format dates for display
close_date_str = submission_close_date.strftime("%A, %d/%m at %I:%M %p ADST")
run_date_str = submission_run_date.strftime("%A, %d/%m at %I:%M %p ADST")

st.divider()

st.write(f"""The challenge submission will close on {close_date_str}. The game will be run and broadcast on Teams on {run_date_str}. Good luck!
""")




st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #5")
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
placeholder1 = '''class YourGifter(Gifter):
    def propose_distribution(self, num_gifts: int, num_gifters: int) -> list:
        """
        Create a proposed distribution of gifts. To be used when YOU are the director.
        
        Args:
            num_gifts: Total number of gifts to distribute
            num_gifters: Number of players still in the game
            
        Returns:
            list: Proposed distribution where index represents player position 
                 (0 is self, 1 is next player, etc.)
        """
        pass

    def vote(self, distribution: list, num_gifts: int, num_gifters: int) -> bool:
        """
        Vote on a proposed distribution.
        
        Args:
            distribution: Proposed distribution of gifts
            num_gifts: Total number of gifts
            num_gifters: Number of players still in game
            
        Returns:
            bool: True to accept, False to reject
        """
        pass'''

if remaining_time.total_seconds() > 0:
    st.subheader("Submit your code")
    name = st.text_input("Name", placeholder="Enter your name")
    emoji = st.text_input("Emoji", placeholder="Paste your emoji here")
    email = st.text_input("Email (optional)", help="Get notified of new challenges and get invited to results livestreams")
    function_code = st.text_area("Function Code (Paste your Python code here)", placeholder=placeholder1)

    if st.button("Submit"):
        if name and function_code:
            num_entrants = len(st.session_state.entrants)
            worksheet.update_cell(num_entrants + 1, 1, name)
            worksheet.update_cell(num_entrants + 1, 4, emoji)
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
for entrant, emoji in zip(st.session_state.entrants, st.session_state.emojis):
    st.sidebar.markdown(
        f"<div style='display: flex; align-items: center; gap: 8px;'>"
        f"<div style='font-size: 24px'>- {emoji}</div>"
        f"<div style='font-size: 16px'>{entrant}</div>"
        f"</div>", 
        unsafe_allow_html=True
    )
# Contact
st.sidebar.divider()
st.sidebar.header("Contact")
st.sidebar.write("Jono Sheahan")