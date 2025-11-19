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
worksheet = sh.get_worksheet(7)
entrants = worksheet.col_values(1)
emojis = worksheet.col_values(4)
st.session_state.entrants = entrants
st.session_state.emojis = emojis


st.header("Data Engineers' Coding Challenge #8")
st.title("Scrooge's Bonus")



st.write("""It's one year on from the events of A Christmas Carol. Spooked and chastened by the visits from the Ghosts, Scrooge's miserly behaviour has been tempered, but not extinguished. Old habits die hard! As Christmas approaches, Scrooge considers whether Christmas turkeys for Bob Cratchit and the other staff are worth the cost. Will this help improve productivity? Or will his employees take advantage of his generosity?
""")
st.write("""Meanwhile, Scrooge's staff are weighing up the situation from a different perspective. Will their hard work be rewarded with a succulent Christmas Turkey? Or will they be left to starve?
""")
st.image("assets/img/image.png", width=500)
st.divider()
st.write("Welcome to the eighth iteration of the Data Engineers' Challenge! This month - we have Scrooge's Bonus: a tribute to the classic tale - A Christmas Carol.")
st.write("**Difficulty**: Easy")
st.write("**Coding Skills Required**: Python, pandas")
st.write("**Other Skills**: Game theory and strategy")
st.divider()
st.audio("assets/audio/scrooges_bonus.m4a", format="audio/m4a", autoplay=False)
url = "https://notebooklm.google.com/"
st.write("Scrooge's Bonus as featured on the [Deep Dive Podcast](%s)" %url)
st.divider()



st.subheader("Challenge Details")
"""Scrooge's Bonus is based on the gift-exchange game (also known as the gift exchange dilemma), a common economic game theory model introduced by George Akerlof and Janet Yellen to simulate reciprocity in labor relations. It serves as a valuable tool for understanding the principal-agent problem in labor economics.

While the simplest form of the general gift-exchange game typically involves only two players, the Scrooge's Bonus game, which is a themed implementation of the gift-exchange dilemma, uses a multi-player format for the ABS Data Engineers' Challenge. The game proceeds sequentially:

1. Scrooge's Move (The Gift): Scrooge first decides whether to award a bonus (the "turkey") or withhold a bonus.
2. Employee's Move (The Reciprocation): Employees then individually decide whether to reciprocate the bonus choice with a higher level of effort (work harder) or a lower level of effort.
This sequence continues for a number of rounds.

The theory suggests that if Scrooge offers a higher salary, employees are more inclined to reciprocate with greater effort, leading to mutually beneficial outcomes. 
"""

st.subheader("Scoring points")
"""This game will award a 'Scrooge' winner and an 'employee' winner, based on the submissions that score the highest number of points over x number of rounds. 
"""
st.write("""Payoff Matrix (Scrooge, employee)

- (turkey, high): (2, 2)
- (turkey, low): (0, 3)
- (no_turkey, high): (3, 0)
- (no_turkey, low): (1, 1)
""")

st.subheader("Challenge Repo")
st.write("You can find the challenge repo [here](https://github.com/uncultivate/xmas-bonus). Try the sample functions and write your own before submitting.")

st.subheader("Function Requirements")
st.write("You can choose to submit a function for Scrooge's decision and a function for an employee's decision, or simply submit a single function for either Scrooge or an employee.")
st.write("Example Strategy:")
code = '''
def stingy_scrooge(history: pd.DataFrame) -> str:
    """
    Scrooge doesn't take long to go back to his miserly ways.
    Args:
        history: pd.DataFrame containing the history of the game
    Returns:
        str: 'turkey' if Scrooge awards a bonus, 'no_turkey' if Scrooge withholds a bonus
    """
    if history.empty:
      return "turkey"
    
    # Scrooge gives up on bonuses after the first round
    return 'no_turkey'
'''
st.code(code, language='python')

code = '''def opportunistic_employee(history: pd.DataFrame) -> str:
    """Work hard only when the previous round included a turkey."""
    if history.empty:
        return "high"
    return "high" if history.iloc[-1]["scrooge_action"] == "turkey" else "low"
'''
st.code(code, language='python')


### Important Properties
st.markdown("""
Function requirements:
Your function receives a view of past rounds as a pandas DataFrame.

History passed to Scrooge strategies (columns: `round`, `scrooge_action`, `high_effort`, `low_effort`):

| round | scrooge_action | high_effort | low_effort |
|------:|-----------------|------------:|-----------:|
| 1     | turkey          | 2           | 0          |
| 2     | no_turkey       | 1           | 1          |
| 3     | no_turkey       | 0           | 2          |

History passed to Employee strategies (columns: `round`, `scrooge_action`, `my_action`, `high_effort`, `low_effort`):

| round | scrooge_action | my_action | high_effort | low_effort |
|------:|-----------------|-----------|------------:|-----------:|
| 1     | turkey          | high      | 2           | 0          |
| 2     | no_turkey       | high      | 1           | 1          |
| 3     | no_turkey       | low       | 0           | 2          |

""")

# Define challenge dates
# Countdown timer

aedt = timezone('Australia/Sydney')
submission_close_date = aedt.localize(datetime.datetime(2025, 12, 4, 23, 59, 59))
submission_run_date = aedt.localize(datetime.datetime(2025, 12, 5, 15, 0, 0))

current_time = datetime.datetime.now(aedt)
remaining_time = submission_close_date - current_time

# Format dates for display
close_date_str = submission_close_date.strftime("%A, %d/%m at %I:%M %p AEDT")
run_date_str = submission_run_date.strftime("%A, %d/%m at %I:%M %p AEDT")

st.divider()

st.write(f"""The challenge submission will close on {close_date_str}. The game will be run and broadcast on Teams on {run_date_str}. Good luck!
""")




st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #8")
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
    name = st.text_input("Name", placeholder="Enter your name")
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