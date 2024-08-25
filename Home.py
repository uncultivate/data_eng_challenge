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
worksheet = sh.get_worksheet(1)
entrants = worksheet.col_values(1)
st.session_state.entrants = entrants

st.title("Data Engineers' Coding Challenge #3: The UpLift Challenge")

# Challenge description
c1, c2 = st.columns(2)
with c1:
    st.write("""
    Management have just announced that a new regional departmental office is being established. Following negotiations with the developers of the new site, it has emerged that there is an elevator discount of 10% on offer if the building's lift logic is created internally, rather than being outsourced to the elevator company.   

    Given the cost savings, ABS Data Engineers have been assigned the UpLift Challenge - to create a function that most efficiently delivers people through the new building!         
    ⏬🚻⏫""")
with c2:
    st.image('assets/img/lift.jpg', width=330)

st.subheader("The Challenge Rules")
url = "https://github.com/uncultivate/elevator-master"
st.write("1. Mission: Each contestant will submit ONE function that determines how the building's elevator should behave, based on several parameters.")
st.write("2. Simulation: Contestants should first access and run the [elevator simulation code repo](%s). This repo contains code to generate simulated building entries & exits, as well as simulation code to run your function, and visualise results" % url)
st.write("3. Challenge parameters: Test your function with a variety of parameters. The challenge will be run three times with different time windows, numbers of people and numbers of floors.")
st.write("4. Objective: The contestant with the lowest average time across the three runs will be declared the winner.")
st.write("5. Example function: There is an example 'baseline_algorithm' included in the run_lifts notebook. Make sure your function can outperform this!")

st.subheader("Function Requirements")
st.write("Test your function using a local jupyter notebooks instance (can enable animations) or in Google Colab (cannot enable animations). Once you are satisfied, submit your code below.") 

st.subheader("Submission Template")
st.write("Below is a template you can use to create your function. Replace the placeholder logic with your strategy.")

code = """def baseline_algorithm(timestamp, elev_pop, floor_population, floors, elevator_floor, t_floor):
    # Simple logic: If the lift is at the bottom floor, head upwards. If the lift is at the 
    top floor, head back down. If in the middle, use the previous direction

    if elevator_floor == 1:
        return floors
    elif elevator_floor == floors:
        return 1

    return t_floor"""
st.code(code, language='python')

st.write("""Your task is to write a Python function that meets the specified requirements. 
The challenge submission will close on Thursday, 05/09 at 11:59 PM AEST. The game will be run and broadcast on Teams on Friday, 06/09 at 3 PM AEST. Good luck!
""")

# Countdown timer
aest = timezone('Australia/Sydney')
submission_close_date = aest.localize(datetime.datetime(2024, 9, 5, 23, 59, 59))
current_time = datetime.datetime.now(aest)
remaining_time = submission_close_date - current_time

st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #3")
if remaining_time.total_seconds() > 0:
    st.sidebar.write(f"Submissions close in {remaining_time.days} days, {remaining_time.seconds // 3600} hours and "
                     f"{(remaining_time.seconds // 60) % 60} minutes.")
else:
    st.sidebar.write("Submissions Closed")

# Submission form
placeholder1 = """def baseline_algorithm(timestamp, elev_pop, floor_population, floors, elevator_floor, t_floor):
    # Simple logic: If the lift is at the bottom floor, head upwards. If the lift is at the 
    top floor, head back down. If in the middle, use the previous direction

    if elevator_floor == 1:
        return floors
    elif elevator_floor == floors:
        return 1

    return t_floor"""
if remaining_time.total_seconds() > 0:
    st.subheader("Submit your code")
    name = st.text_input("Name")
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