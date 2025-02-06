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
worksheet = sh.get_worksheet(5)
entrants = worksheet.col_values(1)
emojis = worksheet.col_values(4)
st.session_state.entrants = entrants
st.session_state.emojis = emojis


st.header("Data Engineers' Coding Challenge #6")
st.title("Dollar Auction")

# Challenge description
st.write("""
    An exciting announcement appears one day in Newspoint: 'Dollar coins are being commissioned by the Mint to commemorate ANDII Release 1!' You read on. 'Unfortunately GIVING the coins to staff would breach APS values, but they will be auctioned off next Friday afternoon.'   
""")

st.image('assets/img/dollar1.png')
st.write("Welcome to the sixth iteration of the Data Engineers' Challenge! This month - we have the Dollar Auction game, a game theory experiment that demonstrates how rational decision-making can lead to seemingly irrational outcomes.")
st.write("**Difficulty**: Easy")
st.write("**Coding Skills Required**: Python, functions, pandas DataFrames, conditional statements")
st.write("**Other Skills**: Strategic thinking and creative problem solving")
st.divider()
st.audio("assets/audio/dollar_auction_deep_dive.wav", format="audio/wav", autoplay=False)
url = "https://notebooklm.google.com/"
st.write("Dollar Auction as featured on the [Deep Dive Podcast](%s)" %url)
st.divider()



st.subheader("Challenge Details")
"The Data Engineers' Challenge #6 revolves around a game called the Dollar Auction. The auction will be contested by entrants who submit functions in Python containing bidding logic (either bid or pass)."
"""In the Dollar Auction game:
- A \$1 coin is auctioned off
- Players can bid in increments of \$0.05
- The highest bidder wins the dollar, but both the highest AND second-highest bidders must pay their bids
- Each player starts with \$2
- There will be multiple dollar auctions occurring with different combinations of players
"""
"""You can create new bidding strategies by defining functions that take three parameters: 
- num_players: Total number of players in the auction
- bid_history: DataFrame containing previous bids with columns 'player' and 'bid'
- money: Current amount of money available to the player
"""


st.subheader("Function Requirements")
st.write("Example Strategy:")
code = '''
    def my_strategy(num_players, bid_history, money):
        import x, y, z # Import any packages you wish to use inside your function (submit early if non-standard)
        current_bid = bid_history.iloc[-1]['bid']
        if current_bid < 0.50: # Only bid if current bid is under 50 cents
                return current_bid + 0.05
        return False

'''
st.code(code, language='python')

### Important Properties
st.markdown("""
Return values:
- Return a float to place a bid (must be higher than current bid and a multiple of $0.05)
- Return False to pass
- Bids cannot exceed player's available money
""")

st.subheader("Access code repo")
st.write("Highly recommended to check this out before submitting. Contains the full game code and example classes.")

    
repo_url = "https://github.com/uncultivate/dollar-auction"

st.link_button("Access code repo", repo_url)


# Define challenge dates
# Countdown timer

aest = timezone('Australia/Sydney')
submission_close_date = aest.localize(datetime.datetime(2025, 2, 13, 23, 59, 59))
submission_run_date = aest.localize(datetime.datetime(2025, 2, 14, 15, 0, 0))

current_time = datetime.datetime.now(aest)
remaining_time = submission_close_date - current_time

# Format dates for display
close_date_str = submission_close_date.strftime("%A, %d/%m at %I:%M %p ADST")
run_date_str = submission_run_date.strftime("%A, %d/%m at %I:%M %p ADST")

st.divider()

st.write(f"""The challenge submission will close on {close_date_str}. The game will be run and broadcast on Teams on {run_date_str}. Good luck!
""")




st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #6")
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
placeholder1 = '''
    def my_strategy(num_players, bid_history, money):
        import x, y, z # Import any packages you wish to use inside your function (submit early if non-standard)
        current_bid = bid_history.iloc[-1]['bid']
        if current_bid < 0.50: # Only bid if current bid is under 50 cents
                return current_bid + 0.05
        return False

'''

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