import streamlit as st
import requests
import os, time
from datetime import datetime

st.title("AOC Interface")


#########################
## Obtaining user info ##
#########################

today = datetime.now().day
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("Choose year:", ["2022","2021","2020"], index=0)
with col2:
    if int(year) == datetime.now().year:
        days = [f"{day}" for day in range(1,today+1)]
    else:
        days = [f"{day}" for day in range(1,26)]
    day = st.selectbox("Choose day:", reversed(days), index=0)

st.columns(1)

session_cookie = st.text_input(label="[Optional] Your session cookie (for automatic retrieval and answering):").strip()


url = f"https://adventofcode.com/{year}/day/{day}/input"
st.write(f"Go get your puzzle input here, and copy the input: {url}")

if session_cookie:
    headers = {'User-Agent': 'https://github.com/julesvanrie/aocsl by jules@vanrie.be'}
    cookies = {'session': session_cookie}

    result = requests.get(url,
                          cookies=cookies,
                          headers=headers)
    # st.markdown(result)
    lines = result.text.strip().split('\n')
else:
    lines = st.text_area("Copy the contents of your input file in here and press Ctrl+Enter:").split('\n')


#########################
## Solve the puzzle    ##
#########################


from solve1 import solve

if len(lines) > 1:
    one, two = solve(lines)

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

            st.subheader(f"Answers from the AOC website for the {part['ord']} part")

            data = {'level': part['level'], 'answer': part['answer']}
            # data_two = {'level': '2', 'answer': f'{two}'}

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
