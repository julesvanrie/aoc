import os
import requests
from datetime import datetime
from params import headers


def submit(year: int = 0, day: int = 0, part: str ='', answer: str = '', session_cookie: str = '') -> tuple:
    """Submits answer to AOC site, and returns:
    - a summarized message on the result
    - the full html returned

    If no year or day provided, takes today.
    If no session cookie provided, checks env variable AOC_SESSION
    """
    if not year:
        year = datetime.now().year
    if not day:
        day = datetime.now().day
    if not session_cookie:
        session_cookie = os.getenv('AOC_SESSION', '')
    cookies = {'session': session_cookie}

    url_answer = f"https://adventofcode.com/{year}/day/{day}/answer"

    data = {'level': part['level'], 'answer': part['answer']}

    result = requests.post(url=url_answer,
                            data=data,
                            cookies=cookies,
                            headers=headers)

    if "That's the" in result.text:
        message = f"Congratulations. You solved the {part['ord']} puzzle..."
    if "That's not the right answer." in result.text:
        message = "Oops. Seems to be the wrong answer."
    if "Did you already complete it?" in result.text:
        message = "Did you already complete this puzzle?"

    return(message, result.text)
