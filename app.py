import streamlit as st
import requests
import os, time
from datetime import datetime
from importlib import import_module
from params import years, days, headers
from random import randint

st.title("AOC Interface")


#########################
## Obtaining user info ##
#########################

today = datetime.now().day
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("Choose year:", reversed(years.keys()), index=0)
with col2:
    if int(year) == datetime.now().year:
        this_day = min(25, datetime.now().day)
    options = list(days.keys())[this_day-1::-1]
    day = st.selectbox("Choose day:", options, index=0)

st.columns(1)

session_cookie = st.text_input(label="[Optional] Your session cookie (for automatic retrieval and answering):").strip()

url = f"https://adventofcode.com/{year}/day/{day}/input"
st.write(f"Go get your puzzle input here, and copy the input: {url}")

if session_cookie:
    cookies = {'session': session_cookie}
    result = requests.get(url,
                          cookies=cookies,
                          headers=headers)
    lines = result.text.strip('\n')
else:
    lines = st.text_area("Copy the contents of your input file in here and press Ctrl+Enter:").strip('\n')


#########################
## Solve the puzzle    ##
#########################

module_name = f'{years[year]}.{days[day]}.solve'
try:
    solver = import_module(module_name)
except:
    st.error(f"Solution solver not found. Ask Jules ;-).\n{module_name}")

if len(lines) > 1:
    one, two = solver.solve(lines)

    st.subheader("Solutions to the puzzles")
    st.markdown(f"The result for part one is *{one}*.")
    st.markdown(f"The result for part two is *{two}*.")
    st.markdown("\n")


#########################
## Submit to AOC site  ##
#########################


    if session_cookie:

        url_answer = f"https://adventofcode.com/{year}/day/{day}/answer"

        parts = [
            {
                'level': '1',
                'answer': str(one),
                'ord': 'first'
            },
            {
                'level': '2',
                'answer': str(two),
                'ord': 'second'
            },
        ]

        for part in parts:

            if st.button(f"Click to submit part {part['level']}"):

                st.subheader(f"Answers from the AOC website for the {part['ord']} part")

                data = {'level': part['level'], 'answer': part['answer']}

                part['result'] = requests.post(url=url_answer,
                                        data=data,
                                        cookies=cookies,
                                        headers=headers)

                if "That's the" in part['result'].text:
                    st.write(f"Congratulations. You solved the {part['ord']} puzzle...")

                if "That's not the right answer." in part['result'].text:
                    st.write("Oops. Seems to be the wrong answer.")

                if "Did you already complete it?" in part['result'].text:
                    st.write("Did you already complete this puzzle?")

                with st.expander("Open to see full response."):
                    st.code(part['result'].text)
