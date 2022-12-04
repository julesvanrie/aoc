import streamlit as st
import requests
import os, time
from datetime import datetime

st.title("AOC Interface")

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

from solve1 import solve

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

# st.write(lines)

if len(lines) > 1:
    one, two = solve(lines)

    st.subheader("Solutions to the puzzles")
    st.markdown(f"The result for part one is *{one}*.")
    st.markdown(f"The result for part two is *{two}*.")
    st.markdown("\n")

    if session_cookie:
        st.subheader("Answers from the AOC website for the first part")
        url_answer = f"https://adventofcode.com/{year}/day/{day}/answer"
        data_one = {'level': '1', 'answer': f'{one}'}
        data_two = {'level': '2', 'answer': f'{two}'}

        result_one = requests.post(url=url_answer,
                                   data=data_one,
                                   cookies=cookies,
                                   headers=headers)

        if "That's the" in result_one.text:
            st.write("Congratulations. You solved puzzle one...")

        if "That's not the right answer." in result_one.text:
            st.write("Oops. Seems to be the wrong answer.")

        if "Did you already complete it?" in result_one.text:
            st.write("Did you already complete this puzzle?")

        with st.expander("Open to see full response."):
            st.code(result_one.text)

        st.subheader("Answers from the AOC website for the second part")

        with st.spinner("Please wait 10 seconds before we submit part two..."):
            time.sleep(10)

        result_two = requests.post(url=url_answer,
                                   data=data_two,
                                   cookies=cookies,
                                   headers=headers)

        if "That's the" in result_two.text:
            st.write("Congratulations. You solved puzzle two...")

        if "That's not the right answer." in result_two.text:
            st.write("Oops. Seems to be the wrong answer.")

        if "You don't seem to be solving the right level." in result_two.text:
            st.write("Oops. Submit the first part before the second.")

        if "Did you already complete it?" in result_two.text:
            st.write("Did you already complete this puzzle?")

        with st.expander("Open to see full response."):
            st.code(result_two.text)
