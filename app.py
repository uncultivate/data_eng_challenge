import streamlit as st
import datetime
import time
import pandas as pd
import textwrap
import inspect
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

st.title("Coding Challenge #2")

# Challenge description
c1, c2 = st.columns(2)
with c1:
    st.write("""
    Step right up and plant the seeds of your success with Tulip Coin! Who wouldn't want to invest in the next big thing that combines the rich history of 17th century Holland with the endless hype of the digital age? With its limited supply and radiant hues, Tulip Coin is your ticket to a blooming fortune! Join the garden of savvy investors who see the potential in this floral commodity on a rocket to the moon! 🌷💰""")
    st.markdown("[Tulip Mania on Wikipedia](https://en.wikipedia.org/wiki/Tulip_mania)")
with c2:
    st.image('assets/img/tulip_coin.jpg', width=270)

st.subheader("The Game Rules")
st.write("""
1. Mission: With starting capital of $1000, each contestant will submit ONE function that decides whether to 'buy', 'sell' or 'hold' based on the history of prices in previous transactions.
2. Duration: Contestants will be chosen every five seconds at random to make a trade. Trading will last for 1 hour.
3. Objective: The contestant with the highest total assets value at close wins! (total assets = dollars + tulip coins)
4. Mystery Entrants:
    - Three mystery contestants have been added to the roster. They are richer than you 💰💰💰""")

st.subheader("Function Requirements")
st.write("""Your function should take a single parameter: a pandas DataFrame containing the history of prices in previous transactions.

The DataFrame history will have the following columns:

- transaction (int): The transaction count (starting from 1)
- price_history (float): The history of prices at each transaction
- minutes_remaining (int): Time remaining until close
         
Your function should return a tuple with the following components: 
         - Transaction decision (str): 'buy', 'sell' or 'hold' and;
         - Decimal proportion (float): If 'buy', the proportion of your money to buy Tulip Coin, or if 'sell', the proportion of your Tulip Coins to sell. If hold, the proportion is disregarded.
         """)
st.subheader("Submission Template")
st.write("Below is a template you can use to create your function. Replace the placeholder logic with your strategy.")

code = """def my_strategy(history):
    # Example strategy: buy low sell high
    if not history.empty:
        # Implement your strategy based on the history DataFrame
        pass
    return 'buy', 0.2"""
st.code(code, language='python')

st.write("""Your task is to write a Python function that meets the specified requirements. 
The challenge submission will close on Thursday, 08/08 at 11:59 PM AEST. The game will be run and broadcast on Teams on Friday, 09/08 at 3 PM AEST. Good luck!
""")

# Countdown timer
aest = timezone('Australia/Sydney')
submission_close_date = aest.localize(datetime.datetime(2024, 8, 8, 23, 59, 59))
current_time = datetime.datetime.now(aest)
remaining_time = submission_close_date - current_time

st.sidebar.title("ABS Data Eng")
st.sidebar.header("Coding Challenge #2")
if remaining_time.total_seconds() > 0:
    st.sidebar.write(f"Submissions close in {remaining_time.days} days, {remaining_time.seconds // 3600} hours and "
                     f"{(remaining_time.seconds // 60) % 60} minutes.")
else:
    st.sidebar.write("Submissions Closed")

# Submission form
placeholder1 = """def buy_high_sell_low(history):
  if history['transactions'].iloc[-1] > history['transactions'].iloc[-2]:
    return 'buy', 0.35
  if history['transactions'].iloc[-1] < history['transactions'].iloc[-2]
    return 'sell', 0.35
  return 'hold', '0.0'"""
if remaining_time.total_seconds() > 0:
    st.subheader("Submit your code")
    name = st.text_input("Name")
    function_code = st.text_area("Function Code (Paste your Python code here)", placeholder=placeholder1)

    if st.button("Submit"):
        if name and function_code:
            num_entrants = len(st.session_state.entrants)
            worksheet.update_cell(num_entrants + 1, 1, name)
            worksheet.update_cell(num_entrants + 1, 2, function_code)
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

# Test function
def test_submitted_function(func_code):
    local_vars = {}
    exec(textwrap.dedent(func_code), {}, local_vars)
    functions = {name: obj for name, obj in local_vars.items() if inspect.isfunction(obj)}
    if functions:
        func_name, test_func = next(iter(functions.items()))
        try:
            # Create a sample DataFrame
            data = {
                'transaction': [1, 2, 3],
                'price_history': [0.1, 0.3, 0.2],
                'minutes_remaining': [30, 29, 29]
            }
            df = pd.DataFrame(data)
            
            # Run the function and check output
            result = test_func(df)
    
            # Check if the result is a tuple
            assert isinstance(result, tuple), "The result should be a tuple"
            
            # Check if the first element of the tuple is 'buy', 'sell', or 'hold'
            assert result[0] in ['buy', 'sell', 'hold'], "The first element should be 'buy', 'sell', or 'hold'"
            
            # Check if the second element of the tuple is a float
            assert isinstance(result[1], float), "The second element should be a float"
            
            # Check if the second element of the tuple is between 0.0 and 1.0
            assert 0.0 <= result[1] <= 1.0, "The second element should be between 0.0 and 1.0"
        except Exception as e:
            return f"Test case failed with function '{func_name}': {e}"
    else:
        return "No function found in the provided code."

# Test the submitted function
placeholder2 = """def always_buy(history):
  return 'buy', 0.15"""
st.subheader("Optional: Test Your Function")
test_code = st.text_area("Paste the function code you want to test", placeholder=placeholder2)
if st.button("Run Tests"):
    result = test_submitted_function(test_code)
    st.write(result)
